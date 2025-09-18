from flask import Flask, request, jsonify, render_template
from .extensions import db, jwt, bcrypt
from .models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"

db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)


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

@app.route("/login", methods=["GET", "POST"])
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


@app.route("/profile", methods=["GET", "POST"])
@jwt_required()
def profile():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if request.method == "POST":
        user.phone_number = request.form.get("phone_number", user.phone_number)
        user.address = request.form.get("address", user.address)
        user.payment_info = request.form.get("payment_info", user.payment_info)
        db.session.commit()
        return "Profile updated successfully"

    # GET request: show HTML form
    return render_template("profile.html", user=user)  # optional: pass user for pre-filling


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
