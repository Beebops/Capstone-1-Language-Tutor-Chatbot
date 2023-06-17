from datetime import datetime
from flask_bcrypt import Bcrypt
from models import db, Chat, Message, User
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone_language_tutor"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt = Bcrypt(app)


def drop_tables():
    with app.app_context():
        db.reflect()
        db.drop_all()


def create_tables():
    with app.app_context():
        db.create_all()


def seed_database():
    with app.app_context():
        drop_tables()
        create_tables()

        # Create users
        user1 = User.signup("user1", "user1@example.com", "password1")
        user2 = User.signup("user2", "user2@example.com", "password2")

        # Create chats
        chat1 = Chat.create_chat(user1.id, "English", "Intermediate")
        chat2 = Chat.create_chat(user2.id, "Spanish", "Advanced")

        # Create messages
        message1 = Message.create_message(chat1.id, "User", "Hello", datetime.utcnow())
        message2 = Message.create_message(
            chat1.id, "Assistant", "Hi there!", datetime.utcnow()
        )
        message3 = Message.create_message(chat2.id, "User", "Hola", datetime.utcnow())
        message4 = Message.create_message(
            chat2.id, "Assistant", "¡Hola!", datetime.utcnow()
        )

        db.session.commit()

        print("Database seeded successfully.")


if __name__ == "__main__":
    seed_database()
