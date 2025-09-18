from .extensions import db, bcrypt
from datetime import datetime

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    customer = db.relationship('User', foreign_keys=[customer_id], backref='customer_chats')
    agent = db.relationship('User', foreign_keys=[agent_id], backref='agent_chats')

    __table_args__ = (
        db.UniqueConstraint('agent_id', 'customer_id', name='unique_agent_customer'),
    )

    def __repr__(self):
        return f"<Chat {self.id} between {self.customer.username} and {self.agent.username}>"


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    chat = db.relationship('Chat', backref='messages')
    sender = db.relationship('User', backref='sent_messages')


    def __repr__(self):
        return f"<Message: {self.content}>"
    


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