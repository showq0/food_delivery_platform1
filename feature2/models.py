from datetime import datetime
from .extensions import db, bcrypt

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='confirmed')

    customer = db.relationship('User', foreign_keys=[customer_id], backref='orders')
    driver = db.relationship('User', foreign_keys=[driver_id], backref='orders_as_driver')

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    CUSTOMER = 'customer'
    DRIVER = 'driver'
    AGENT = 'agent'
    ROLE_CHOICES = [CUSTOMER, DRIVER, AGENT]

    role = db.Column(db.String(20), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.Text, nullable=True)
    payment_info = db.Column(db.String(50), nullable=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "phone_number": self.phone_number,
            "address": self.address,
            "payment_info": self.payment_info,
        }
