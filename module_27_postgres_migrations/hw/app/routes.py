import random

import requests
from flask import Blueprint, request

from app import db
from app.models import Coffee, User

bp = Blueprint("main", __name__)

_seed_done = False


def coffee_to_dict(coffee):
    return {
        "id": coffee.id,
        "title": coffee.title,
        "category": coffee.category,
        "description": coffee.description,
        "reviews": coffee.reviews,
    }


def user_to_dict(user):
    return {
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "patronomic": user.patronomic,
        "address": user.address,
        "coffee": coffee_to_dict(user.coffee) if user.coffee else None,
    }


@bp.before_app_request
def seed_data():
    global _seed_done

    if _seed_done:
        return

    _seed_done = True

    if User.query.first():
        return

    coffee_response = requests.get(
        "https://dummyjson.com/products/search?q=coffee",
        timeout=10,
    )
    coffee_data = coffee_response.json()["products"][0]

    coffee = Coffee(
        title=coffee_data["title"],
        category=coffee_data["category"],
        description=coffee_data["description"],
        reviews=[review["comment"] for review in coffee_data.get("reviews", [])],
    )

    db.session.add(coffee)
    db.session.commit()

    users_response = requests.get(
        "https://dummyjson.com/users?limit=10",
        timeout=10,
    )
    users_data = users_response.json()["users"]

    for item in users_data:
        user = User(
            name=item["firstName"],
            surname=item["lastName"],
            patronomic=None,
            address=item["address"],
            coffee_id=coffee.id,
        )
        db.session.add(user)

    db.session.commit()


@bp.route("/")
def index():
    return {"message": "Flask app is running"}


@bp.route("/users", methods=["POST"])
def add_user():
    data = request.get_json() or {}

    coffee = Coffee.query.order_by(db.func.random()).first()

    user = User(
        name=data.get("name", f"User{random.randint(1, 1000)}"),
        surname=data.get("surname"),
        patronomic=data.get("patronomic"),
        address=data.get("address", {}),
        coffee_id=coffee.id if coffee else None,
    )

    db.session.add(user)
    db.session.commit()

    return user_to_dict(user), 201


@bp.route("/coffee/search")
def search_coffee():
    title = request.args.get("title", "")

    query = db.text("""
        SELECT *
        FROM coffee
        WHERE to_tsvector('english', title) @@ plainto_tsquery('english', :title)
    """)

    result = db.session.execute(query, {"title": title}).mappings().all()

    return [dict(row) for row in result]


@bp.route("/coffee/reviews/unique")
def unique_reviews():
    query = db.text("""
        SELECT DISTINCT unnest(reviews) AS review
        FROM coffee
    """)

    result = db.session.execute(query).mappings().all()

    return [row["review"] for row in result]


@bp.route("/users/by-country")
def users_by_country():
    country = request.args.get("country", "")

    users = User.query.filter(
        User.address["country"].astext == country
    ).all()

    return [user_to_dict(user) for user in users]