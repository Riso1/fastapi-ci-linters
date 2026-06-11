from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base, engine, get_session
from app.models import Recipe
from app.schemas import RecipeCreate, RecipeDetail, RecipeList


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Cookbook API",
    description="API для приложения кулинарной книги",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get(
    "/recipes",
    response_model=list[RecipeList],
    summary="Получить список рецептов",
    description=(
        "Возвращает список рецептов с пагинацией. "
        "Время приготовления указано в минутах. "
        "Рецепты сортируются по количеству просмотров по убыванию. "
        "Если просмотры совпадают, сначала показываются рецепты с меньшим временем приготовления."
    ),
)
async def get_recipes(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
):
    query = (
        select(Recipe)
        .order_by(Recipe.views.desc(), Recipe.cooking_time.asc())
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(query)
    return result.scalars().all()


@app.get(
    "/recipes/{recipe_id}",
    response_model=RecipeDetail,
    summary="Получить детальную информацию о рецепте",
    description=(
        "Возвращает полную информацию о рецепте. "
        "Время приготовления указано в минутах. "
        "При открытии рецепта счётчик просмотров увеличивается атомарно."
    ),
)
async def get_recipe(recipe_id: int, session: AsyncSession = Depends(get_session)):
    recipe = await session.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    await session.execute(
        update(Recipe)
        .where(Recipe.id == recipe_id)
        .values(views=Recipe.views + 1)
    )
    await session.commit()

    recipe.views += 1
    ingredients = recipe.ingredients.split("\n") if recipe.ingredients else []

    return RecipeDetail(
        id=recipe.id,
        title=recipe.title,
        cooking_time=recipe.cooking_time,
        ingredients=ingredients,
        description=recipe.description,
        views=recipe.views,
    )


@app.post(
    "/recipes",
    response_model=RecipeDetail,
    status_code=201,
    summary="Создать рецепт",
    description=(
        "Создаёт новый рецепт. "
        "Время приготовления передаётся в минутах."
    ),
)
async def create_recipe(
    recipe_data: RecipeCreate,
    session: AsyncSession = Depends(get_session),
):
    recipe = Recipe(
        title=recipe_data.title,
        cooking_time=recipe_data.cooking_time,
        ingredients="\n".join(recipe_data.ingredients),
        description=recipe_data.description,
        views=0,
    )

    session.add(recipe)
    await session.commit()

    ingredients = recipe.ingredients.split("\n") if recipe.ingredients else []

    return RecipeDetail(
        id=recipe.id,
        title=recipe.title,
        cooking_time=recipe.cooking_time,
        ingredients=ingredients,
        description=recipe.description,
        views=recipe.views,
    )