from pydantic import BaseModel, Field


class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    cooking_time: int = Field(..., gt=0)
    ingredients: list[str] = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class RecipeList(BaseModel):
    id: int
    title: str
    views: int
    cooking_time: int

    class Config:
        from_attributes = True


class RecipeDetail(BaseModel):
    id: int
    title: str
    cooking_time: int
    ingredients: list[str]
    description: str
    views: int

    class Config:
        from_attributes = True