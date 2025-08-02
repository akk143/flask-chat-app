from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

conversation_user = db.Table('conversation_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', secondary=conversation_user, backref='conversations')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender = db.relationship('User')
