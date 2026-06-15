from pydantic import BaseModel, ConfigDict, Field, field_validator


class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    cooking_time: int = Field(..., gt=0, description="Время приготовления в минутах")
    ingredients: list[str] = Field(..., min_length=1)
    description: str = Field(..., min_length=1)

    @field_validator("ingredients")
    @classmethod
    def validate_ingredients(cls, ingredients):
        cleaned_ingredients = []

        for ingredient in ingredients:
            ingredient = ingredient.strip()
            if ingredient:
                cleaned_ingredients.append(ingredient)

        if not cleaned_ingredients:
            raise ValueError("Ingredients list cannot be empty")

        return cleaned_ingredients


class RecipeList(BaseModel):
    id: int
    title: str
    views: int
    cooking_time: int = Field(..., description="Время приготовления в минутах")

    model_config = ConfigDict(from_attributes=True)


class RecipeDetail(BaseModel):
    id: int
    title: str
    cooking_time: int = Field(..., description="Время приготовления в минутах")
    ingredients: list[str]
    description: str
    views: int

    model_config = ConfigDict(from_attributes=True)
