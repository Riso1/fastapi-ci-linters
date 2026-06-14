from datetime import datetime, UTC
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from .models import db, Client, Parking, ClientParking


bp = Blueprint('api', __name__)


@bp.get('/clients')
def get_clients():
    clients = Client.query.all()
    return jsonify([client.to_dict() for client in clients]), 200


@bp.get('/clients/<int:client_id>')
def get_client(client_id):
    client = db.session.get(Client, client_id)
    if client is None:
        return jsonify({'error': 'client not found'}), 404

    return jsonify(client.to_dict()), 200


@bp.post('/clients')
def create_client():
    data = request.get_json() or {}

    if not data.get('name') or not data.get('surname'):
        return jsonify({'error': 'name and surname are required'}), 400

    client = Client(
        name=data['name'],
        surname=data['surname'],
        credit_card=data.get('credit_card'),
        car_number=data.get('car_number'),
    )
    db.session.add(client)
    db.session.commit()

    return jsonify(client.to_dict()), 201


@bp.post('/parkings')
def create_parking():
    data = request.get_json() or {}

    if not data.get('address'):
        return jsonify({'error': 'address is required'}), 400

    count_places = data.get('count_places')
    if count_places is None or int(count_places) < 0:
        return jsonify({'error': 'count_places must be positive'}), 400

    count_available_places = data.get('count_available_places', count_places)

    parking = Parking(
        address=data['address'],
        opened=data.get('opened', True),
        count_places=count_places,
        count_available_places=count_available_places,
    )
    db.session.add(parking)
    db.session.commit()

    return jsonify(parking.to_dict()), 201


@bp.post('/client_parkings')
def enter_parking():
    data = request.get_json() or {}
    client_id = data.get('client_id')
    parking_id = data.get('parking_id')

    client = db.session.get(Client, client_id)
    parking = db.session.get(Parking, parking_id)

    if not client or not parking:
        return jsonify({'error': 'client or parking not found'}), 404

    if not parking.opened:
        return jsonify({'error': 'parking is closed'}), 400

    if parking.count_available_places <= 0:
        return jsonify({'error': 'no available places'}), 400

    parking_log = ClientParking(
        client_id=client.id,
        parking_id=parking.id,
        time_in=datetime.now(UTC),
    )
    parking.count_available_places -= 1

    db.session.add(parking_log)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'client already parked here'}), 400

    return jsonify(parking_log.to_dict()), 201


@bp.delete('/client_parkings')
def leave_parking():
    data = request.get_json() or {}
    client_id = data.get('client_id')
    parking_id = data.get('parking_id')

    parking_log = ClientParking.query.filter_by(
        client_id=client_id,
        parking_id=parking_id,
        time_out=None,
    ).first()

    if not parking_log:
        return jsonify({'error': 'active parking log not found'}), 404

    client = parking_log.client
    parking = parking_log.parking

    if not client.credit_card:
        return jsonify({'error': 'client has no credit card'}), 400

    parking_log.time_out = datetime.now(UTC)
    parking.count_available_places += 1

    db.session.commit()

    return jsonify(parking_log.to_dict()), 200
