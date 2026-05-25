from flask import Flask, jsonify, request
from models import init_db, get_available_rooms, add_room, get_room_by_id, mark_room_as_booked

app = Flask(__name__)

@app.route("/room", methods=["GET"])
def get_room():
    guest_num = request.args.get("guestsNum")

    if guest_num is not None:
        int_guest_num = int(guest_num)
        result = get_available_rooms(int_guest_num)
    else:
        result = get_available_rooms()

    rooms = []
    for room in result:
        rooms.append({
            "roomId": room[0],
            "floor": room[1],
            "guestNum": room[2],
            "beds": room[3],
            "price": room[4],
        })

    return jsonify({"rooms": rooms})

@app.route("/add-room", methods=["POST"])
def add_new_room():
    data = request.get_json()
    floor = data["floor"]
    beds = data["beds"]
    guest_num = data["guestNum"]
    price = data["price"]

    add_room(floor, beds, guest_num, price)

    result = get_available_rooms()
    rooms = []
    for room in result:
        rooms.append({
            "roomId": room[0],
            "floor": room[1],
            "guestNum": room[2],
            "beds": room[3],
            "price": room[4],
        })
    return jsonify({"rooms": rooms})

@app.route("/booking", methods=["POST"])
def booking():
    json_file = request.get_json()
    room_id = json_file["roomId"]
    booking_dates = json_file["bookingDates"]
    first_name = json_file["firstName"]
    last_name = json_file["lastName"]

    room = get_room_by_id(room_id)

    if room is None:
        return jsonify({"error": "Room not found"}), 404

    if room[5] == 1:
        return jsonify({"error": "Room already booked"}), 409

    mark_room_as_booked(room_id)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
