from flask import Flask, render_template, request, redirect, url_for, Response

import asyncio
from .models import db, User, Order
from .extensions import db
from .utils import connect_sse, push_event
import asyncio
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"

db.init_app(app)

@app.route('/menu')
def menu():
    return render_template("menu.html")


@app.route('/order', methods=['GET', 'POST'])
@app.route('/order/<int:id>', methods=['GET'])
def order_view(id=None):
    if request.method == "POST":
        user_id = request.form.get('user_id')
        user = None

        if user_id:
            try:
                user_id = int(user_id)
                user = User.query.get(user_id)
            except ValueError:
                user = None

        if not user:
            user = User.query.filter_by(username="guest").first()
            if not user:
                new_user = User(username="guest", role="customer")
                new_user.set_password("pass123")
                db.session.add(new_user)
                db.session.commit()
                user = new_user

        order = Order(customer=user, status="confirmed")
        db.session.add(order)
        db.session.commit()

        q = connect_sse(order.id)
        asyncio.run(push_event(order.id, "Confirmed"))

        return render_template("track_order.html", order_id=order.id)
    
    if request.method == "GET" and id:
        order = Order.query.get_or_404(id)
        return render_template("track_order.html", order_id=order.id)
    
    return redirect(url_for("menu"))



@app.route('/sse/<int:order_id>')
def sse_stream(order_id):
    def event_stream():
        last_status = None
        while True:
            with app.app_context(): 
                order = Order.query.get(order_id)
                if not order:
                    yield "data: order not found\n\n"
                    break
                if order.status != last_status:
                    last_status = order.status
                    yield f"data: {order.status}\n\n"

                if last_status.lower() == "delivered":
                    break
            time.sleep(30)
    return Response(event_stream(), mimetype="text/event-stream")





@app.route('/order-status/<int:order_id>/', methods=['POST'])
def update_order_status_form(order_id):
    new_status = request.form.get("status")

    order = Order.query.get(order_id)

    order.status = new_status
    db.session.commit()  # triggers the SSE signal
    return redirect(url_for('show_order_status_form', order_id=order_id))


@app.route('/order-status/<int:order_id>/', methods=['GET'])
def show_order_status_form(order_id):
    order = Order.query.get(order_id)
    if not order:
        abort(404, description="Order not found")
    return render_template("status_update.html", order=order, order_id=order.id)


with app.app_context():
    db.create_all()
if __name__ == "__main__":
    app.run(debug=True, threaded=True)