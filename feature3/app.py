from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit
from .extensions import socketio
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio.init_app(app, cors_allowed_origins="*")

@app.route('/tracking-order-location/<int:order_id>')
def track_location(order_id):
    return render_template("track_location.html", order_id=order_id)

@app.route('/send-driver-location/<int:order_id>')
def send_driver_location(order_id):
    return render_template("send_location.html", order_id=order_id)

# websocket 
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('join')
def on_join(data):
    order_id = data['order_id']
    room = f"order_{order_id}"
    role = data.get('role', 'customer')
    join_room(room) 
    print(f"{role} joined room {room}")

@socketio.on('send_location')
def handle_send_location(data):
    order_id = data['order_id']
    lon = data['lon']
    lat = data['lat']
    room = f"order_{order_id}"

    socketio.emit('receive_location', {'lon': lon, 'lat': lat}, room=room)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    socketio.run(app, debug=True)
