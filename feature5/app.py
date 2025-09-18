from flask import Flask, render_template, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, join_room, leave_room, emit
from .models import db, User, Chat, Message
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .extensions import db, jwt, bcrypt
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")
jwt.init_app(app)
bcrypt.init_app(app)

# websocket for realtime chat
@socketio.on('join')
def handle_join(data):
    chat_id = data['chat_id']
    room = f'chat_{chat_id}'
    join_room(room)

@socketio.on('typing')
def handle_typing(data):
    room = f'chat_{data["chat_id"]}'
    emit('typing', {
        'sender_name': data['sender_name'],
        'sender_id': data['sender_id'],
        'typing_status': data['typing_status']
    }, to=room, include_self=False)

@socketio.on('message')
def handle_message(data):
    chat_id = data['chat_id']
    sender_id = data['sender_id']
    content = data['message']

    message = Message(chat_id=chat_id, sender_id=sender_id, content=content)
    db.session.add(message)
    db.session.commit()

    room = f'chat_{chat_id}'
    emit('message', {
        'event_type': 'message',
        'sender_name': data['sender_name'],
        'sender_id': sender_id,
        'message': content
    }, to=room)


@jwt_required()
@app.route('/chat_room/<int:chat_id>/')
def chat_room(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.id).all()
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
    return render_template('chat.html', chat=chat, messages=messages, user=user)




# to handle users login and registration

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.form
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))

    session['access_token'] = access_token
    session['user_id'] = user.id 
    return jsonify(access_token=access_token)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    data = request.form
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "User already exists"}), 400

    new_user = User(
        username=data["username"],
        role=data.get("role", "customer"),
        phone_number=data.get("phone_number"),
        address=data.get("address"),
        payment_info=data.get("payment_info"),
    )
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


with app.app_context():
    db.create_all()
if __name__ == "__main__":
    app.run(debug=True, threaded=True)