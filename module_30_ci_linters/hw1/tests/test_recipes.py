from fastapi.testclient import TestClient

from app.main import app


def test_create_recipe():
    with TestClient(app) as client:
        response = client.post(
            "/recipes",
            json={
                "title": "Тестовый рецепт",
                "cooking_time": 15,
                "ingredients": ["Ингредиент 1", "Ингредиент 2"],
                "description": "Описание тестового рецепта",
            },
        )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Тестовый рецепт"
    assert data["cooking_time"] == 15
    assert data["ingredients"] == ["Ингредиент 1", "Ингредиент 2"]
    assert data["views"] == 0


def test_get_recipes():
    with TestClient(app) as client:
        response = client.get("/recipes")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_recipe_increases_views():
    with TestClient(app) as client:
        create_response = client.post(
            "/recipes",
            json={
                "title": "Рецепт для просмотров",
                "cooking_time": 20,
                "ingredients": ["Мука", "Вода"],
                "description": "Описание рецепта",
            },
        )

        recipe_id = create_response.json()["id"]

        first_response = client.get(f"/recipes/{recipe_id}")
        second_response = client.get(f"/recipes/{recipe_id}")

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert second_response.json()["views"] == first_response.json()["views"] + 1


def test_empty_ingredient_is_not_allowed():
    with TestClient(app) as client:
        response = client.post(
            "/recipes",
            json={
                "title": "Плохой рецепт",
                "cooking_time": 10,
                "ingredients": ["   "],
                "description": "Описание",
            },
        )

    assert response.status_code == 422
