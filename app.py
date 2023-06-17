import os
import openai
import openaiapi
from datetime import datetime
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    login_required,
    logout_user,
)
from forms import login_form, registration_form, new_chat_form
from models import db, connect_db, User, Chat, Message

app = Flask(__name__)

app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone_language_tutor"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = os.environ.get("LANGUAGE_TUTOR_SECRET_KEY")

toolbar = DebugToolbarExtension(app)
login_manager = LoginManager(app)

connect_db(app)
app.app_context().push()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """Displays user's home page with list of saved chats and form to create a new chat"""
    form = new_chat_form()

    if form.validate_on_submit():
        language = form.language.data
        language_level = form.language_level.data

        chat = Chat.create_chat(current_user.id, language, language_level)
        return redirect(url_for("chat_page", chat_id=chat.id, form=form))

    return render_template("user_home.html", form=form)


@app.route("/chat/<int:chat_id>", methods=["GET", "POST"])
@login_required
def chat_page(chat_id):
    if request.method == "POST":
        # Get the user's prompt input and save it as new message in db
        data = request.get_json()
        prompt = data["prompt"]
        Message.create_message(
            chat_id,
            role="User",
            content=prompt,
            timestamp=datetime.utcnow(),
        )

        # Retrieve the language and language level from the Chat model
        chat = Chat.query.get(chat_id)
        language = chat.language
        language_level = chat.language_level

        # Call the API and create a new message log in db
        assistant_message = openaiapi.generate_chat_response(
            prompt, language, language_level
        )
        response = {"assistant_message": assistant_message}
        Message.create_message(
            chat_id,
            role="Assistant",
            content=response["assistant_message"],
            timestamp=datetime.utcnow(),
        )

        return jsonify(response), 200

    return render_template("chat.html", chat_id=chat_id)


################# USER LOGIN AND REGISTRATION #################


@app.route("/signup", methods=["GET", "POST"])
def signup_user():
    """shows and handles new user registration form"""
    form = registration_form()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User.signup(username, email, password)
        db.session.commit()

        login_user(user)
        flash("You are now logged in!", "success")
        return redirect(url_for("home"))

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """shows and handles user login form"""

    form = login_form()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            flash("You are now logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are now logged out!", "success")

    return redirect(url_for("index"))


################# HOME PAGES FOR LOGGED IN AND ANONYMOUS USERS #################


@app.route("/")
def index():
    """Display index page"""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
