from datetime import datetime, UTC
import pytest

from app.models import Client, Parking, ClientParking
from tests.factories import ClientFactory, ParkingFactory


@pytest.mark.parametrize('url', [
    '/clients',
    '/clients/1',
])
def test_get_methods(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_create_client(client, db):
    before_count = Client.query.count()

    response = client.post('/clients', json={
        'name': 'Petr',
        'surname': 'Ivanov',
        'credit_card': '5555 4444 3333 2222',
        'car_number': 'B222BB',
    })

    assert response.status_code == 201
    assert Client.query.count() == before_count + 1
    assert response.json['id'] is not None
    assert response.json['name'] == 'Petr'


def test_create_parking(client, db):
    before_count = Parking.query.count()

    response = client.post('/parkings', json={
        'address': 'Omsk, Mira 10',
        'opened': True,
        'count_places': 20,
        'count_available_places': 20,
    })

    assert response.status_code == 201
    assert Parking.query.count() == before_count + 1
    assert response.json['id'] is not None
    assert response.json['count_available_places'] == 20


@pytest.mark.parking
def test_enter_parking(client, db):
    new_client = Client(
        name='Alex',
        surname='Sidorov',
        credit_card='9999 8888 7777 6666',
        car_number='C333CC',
    )
    parking = Parking(
        address='Omsk, Test street 5',
        opened=True,
        count_places=5,
        count_available_places=5,
    )
    db.session.add_all([new_client, parking])
    db.session.commit()

    response = client.post('/client_parkings', json={
        'client_id': new_client.id,
        'parking_id': parking.id,
    })

    updated_parking = db.session.get(Parking, parking.id)
    parking_log = ClientParking.query.filter_by(
        client_id=new_client.id,
        parking_id=parking.id,
    ).first()

    assert response.status_code == 201
    assert updated_parking.opened is True
    assert updated_parking.count_available_places == 4
    assert parking_log.time_in is not None
    assert parking_log.time_out is None


@pytest.mark.parking
def test_leave_parking(client, db):
    new_client = Client(
        name='Oleg',
        surname='Smirnov',
        credit_card='0000 1111 2222 3333',
        car_number='D444DD',
    )
    parking = Parking(
        address='Omsk, Exit street 7',
        opened=True,
        count_places=3,
        count_available_places=2,
    )
    db.session.add_all([new_client, parking])
    db.session.commit()

    parking_log = ClientParking(
        client_id=new_client.id,
        parking_id=parking.id,
        time_in=datetime.now(UTC),
    )
    db.session.add(parking_log)
    db.session.commit()

    response = client.delete('/client_parkings', json={
        'client_id': new_client.id,
        'parking_id': parking.id,
    })

    updated_log = db.session.get(ClientParking, parking_log.id)
    updated_parking = db.session.get(Parking, parking.id)

    assert response.status_code == 200
    assert updated_parking.count_available_places == 3
    assert updated_log.time_out is not None
    assert updated_log.time_out >= updated_log.time_in
    assert new_client.credit_card is not None


def test_create_client_with_factory(client, db):
    before_count = Client.query.count()
    fake_client = ClientFactory()

    response = client.post('/clients', json={
        'name': fake_client.name,
        'surname': fake_client.surname,
        'credit_card': fake_client.credit_card,
        'car_number': fake_client.car_number,
    })

    assert response.status_code == 201
    assert Client.query.count() == before_count + 1
    assert response.json['id'] is not None


def test_create_parking_with_factory(client, db):
    before_count = Parking.query.count()
    fake_parking = ParkingFactory()

    response = client.post('/parkings', json={
        'address': fake_parking.address,
        'opened': fake_parking.opened,
        'count_places': fake_parking.count_places,
        'count_available_places': fake_parking.count_available_places,
    })

    assert response.status_code == 201
    assert Parking.query.count() == before_count + 1
    assert response.json['id'] is not None
