from flask import Flask
from .models import db


def create_app(test_config=None):
    """Фабрика приложения. Настройки можно подменять в тестах."""
    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite:///parking.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app
