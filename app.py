import os

from flask import Flask, render_template, flash, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    login_required,
    logout_user,
)
from forms import login_form, registration_form, new_chat_form
from models import db, connect_db, User, Chat, Chat_log

app = Flask(__name__)

app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///ai_language_tutor"
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

    user_chats = Chat.query.filter_by(user_id=current_user.id).all()

    form = new_chat_form()

    if form.validate_on_submit():
        language = form.language.data
        language_level = form.language_level.data

        chat = Chat.create_chat(current_user.id, language, language_level)

        return redirect(url_for("chat_page", chat_id=chat.id))

    return render_template("user_home.html", form=form, user_chats=user_chats)


@app.route("/chat/<int:chat_id>", methods=["GET", "POST"])
@login_required
def chat_page(chat_id):
    """Displays a chat and updates its messages"""

    # Need to add form that submits user input to OpenAI API and generates response

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
