from unittest import TestCase
import os
from flask import g

from flask import url_for
from openaiapi import generate_chat_response
from app import app, db
from models import connect_db, User, Chat, Message
from forms import (
    login_form,
    registration_form,
    new_chat_form,
    title_chat_form,
)

os.environ["DATABASE_URL"] = "postgresql:///capstone_language_tutor_testing_db"

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql:///capstone_language_tutor_testing_db"
app.config["SQLALCHEMY_ECHO"] = False
app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]


class AppTests(TestCase):
    def setUp(self):
        with app.app_context():
            app.config["SERVER_NAME"] = "localhost.localdomain"
            db.create_all()
            # Create a test user for authentication
            user = User.signup(
                username="testuser",
                email="testuser@example.com",
                password="password",
            )
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_index(self):
        with app.test_client() as client:
            response = client.get("/")

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                '<h1 class="display-1">ChatMentor</h1>', response.data.decode()
            )

    def test_signup_user(self):
        with self.client as client:
            # Send a POST request to route with user input
            response = client.post(
                "/signup_user",
                data={
                    "username": "testuser",
                    "email": "testuser@example.com",
                    "password": "password",
                    "password_copy": "password",
                },
                follow_redirects=True,
            )

            # Check if user is redirected to index page
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.request.path, "/")

        # ensures that the user was created/saved in the database with correct username and email
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "testuser@example.com")

        with self.client.session_transaction() as session:
            self.assertEqual(session["_user_id"], str(user.id))

    def test_login(self):
        # Send a POST request to route with valid credentials
        with app.test_client() as client:
            response = client.post(
                "/login",
                data={"username": "testuser", "password": "password"},
                follow_redirects=True,
            )

            # Check if user is redirected to index page
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.request.path, "/")

        # Check if user is logged in
        with client.session_transaction() as session:
            self.assertEqual(session["_user_id"], "1")

    def test_login_invalid_credentials(self):
        # Send a POST request to the route with invalid credentials
        with app.test_client() as client:
            response = client.post(
                "/login",
                data={"username": "testuser", "password": "wrongpassword"},
                follow_redirects=True,
            )

        # Check if the user is not authenticated
        with client.session_transaction() as session:
            self.assertNotIn("_user_id", session)

        # Check if the flash message is displayed
        self.assertIn("Invalid username or password", response.data.decode("utf-8"))
