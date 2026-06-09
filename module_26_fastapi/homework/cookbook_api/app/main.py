from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
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
    description="Возвращает все рецепты, отсортированные по популярности."
)
async def get_recipes(session: AsyncSession = Depends(get_session)):
    query = select(Recipe).order_by(
        Recipe.views.desc(),
        Recipe.cooking_time.asc(),
    )
    result = await session.execute(query)
    return result.scalars().all()


@app.get(
    "/recipes/{recipe_id}",
    response_model=RecipeDetail,
    summary="Получить рецепт",
    description="Возвращает полную информацию о рецепте и увеличивает счётчик просмотров."
)
async def get_recipe(recipe_id: int, session: AsyncSession = Depends(get_session)):
    recipe = await session.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe.views += 1
    await session.commit()
    await session.refresh(recipe)

    return RecipeDetail(
        id=recipe.id,
        title=recipe.title,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients.split("\n"),
        description=recipe.description,
        views=recipe.views,
    )


@app.post(
    "/recipes",
    response_model=RecipeDetail,
    status_code=201,
    summary="Создать рецепт",
    description="Создаёт новый рецепт."
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
    await session.refresh(recipe)

    return RecipeDetail(
        id=recipe.id,
        title=recipe.title,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients.split("\n"),
        description=recipe.description,
        views=recipe.views,
    )