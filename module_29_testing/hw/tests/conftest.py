from datetime import datetime, timedelta, UTC
import pytest

from app import create_app
from app.models import db as _db, Client, Parking, ClientParking


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        _db.create_all()

        client = Client(
            name='Ivan',
            surname='Petrov',
            credit_card='1234 5678 9000 1111',
            car_number='A111AA',
        )
        parking = Parking(
            address='Omsk, Lenina 1',
            opened=True,
            count_places=10,
            count_available_places=9,
        )
        _db.session.add_all([client, parking])
        _db.session.commit()

        parking_log = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in=datetime.now(UTC) - timedelta(hours=1),
            time_out=datetime.now(UTC),
        )
        _db.session.add(parking_log)
        _db.session.commit()

        yield app

        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db
