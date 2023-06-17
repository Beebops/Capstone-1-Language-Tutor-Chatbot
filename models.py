from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()
bcrypt = Bcrypt()


class Chat(db.Model):
    """Model of a user's chat"""

    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))

    language = db.Column(db.String(75), nullable=False)

    language_level = db.Column(db.String(15), nullable=False)

    chats_logs = db.relationship(
        "Message", backref="chat", cascade="all, delete-orphan"
    )

    @classmethod
    def create_chat(cls, user_id, language, language_level):
        """Create a new chat for a user"""
        chat = cls(user_id=user_id, language=language, language_level=language_level)
        db.session.add(chat)
        db.session.commit()
        return chat

    def delete_chat(self):
        """Delete the chat and its associated messages."""
        db.session.delete(self)
        db.session.commit()


class Message(db.Model):
    """Model of messages produced by either the user or assistant in a chat"""

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    role = db.Column(db.String(50), nullable=False)

    content = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id", ondelete="cascade"))

    @classmethod
    def create_message(cls, chat_id, role, content, timestamp):
        """Log a new message to a chat"""
        message = cls(chat_id=chat_id, role=role, content=content, timestamp=timestamp)
        db.session.add(message)
        db.session.commit()
        return message

    @classmethod
    def get_content_by_chat(cls, chat_id):
        """Retrieve all messages for a given chat id"""
        return cls.query.filter_by(chat_id=chat_id).all()


class User(UserMixin, db.Model):
    """User in the system"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(120), nullable=False, unique=True)

    email = db.Column(db.String(120), nullable=False, unique=True)

    password = db.Column(db.String(300), nullable=False)

    chats = db.relationship("Chat", backref="user", cascade="all, delete-orphan")

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    @classmethod
    def signup(cls, username, email, password):
        """Registers a new user
        Hashes password and adds user to the system
        """

        hashed_password = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(username=username, email=email, password=hashed_password)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user when username and password is inputted.

        Class method that searches for a user whose password matches the entered password, and returns the user object if there is a match.
        If password is incorrect or a user isn't found, returns False
        """
        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return user

        return False


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
