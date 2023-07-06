import os
import openaiapi
from datetime import datetime
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    flash,
    redirect,
    url_for,
)
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    login_required,
    logout_user,
)
from forms import (
    login_form,
    registration_form,
    new_chat_form,
    title_chat_form,
)
from models import db, connect_db, User, Chat, Message

app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///capstone_language_tutor"
)

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


################# INDEX PAGE FOR LOGGED IN AND ANONYMOUS USERS #################


@app.route("/")
def index():
    """Display index page"""
    return render_template("index.html")


################# CHAT ROUTES #################


@app.route("/home", methods=["GET", "POST"])
@login_required
def new_chat():
    """Displays user's home page with form to create a new chat"""
    form = new_chat_form()

    if form.validate_on_submit():
        language = form.language.data
        language_level = form.language_level.data

        chat = Chat.create_chat(current_user.id, language, language_level)

        return redirect(url_for("chat_page", chat_id=chat.id))

    return render_template("new_chat.html", form=form)


@app.route("/chats/<int:user_id>")
@login_required
def display_chats(user_id):
    """Shows all of user's chats"""
    chats = Chat.get_chats_by_user(user_id)

    return render_template("chat_list.html", chats=chats)


@app.route("/edit/int:<chat_id>", methods=["GET", "POST"])
@login_required
def edit(chat_id):
    """Edit chat title"""
    chat = Chat.query.get(chat_id)
    form = title_chat_form()

    if form.validate_on_submit():
        title = form.title.data
        chat.chat_title = title
        db.session.commit()

        return redirect(url_for("display_chats", user_id=current_user.id))

    return render_template("chat_title.html", form=form)


@app.route("/chats/delete/<int:chat_id>", methods=["POST"])
@login_required
def delete_chat(chat_id):
    """Deletes a chat"""
    chat = Chat.query.get(chat_id)
    if chat:
        if chat.user_id == current_user.id:
            chat.delete_chat()
            flash("Chat deleted successfully", "success")
        else:
            flash("You do not have permission to delete this chat", "error")
    else:
        flash("Chat not found", "error")

    return redirect(url_for("display_chats", user_id=current_user.id))


@app.route("/chat/<int:chat_id>", methods=["GET", "POST"])
@login_required
def chat_page(chat_id):
    """Handles form to start a new chat with chat bot or returns the saved chat of the given chat_id"""
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

    chat_title = Chat.get_chat_title(chat_id)
    messages = Message.get_messages_by_chat(chat_id)
    return render_template(
        "chat.html", chat_id=chat_id, chat_title=chat_title, messages=messages
    )


################# USER LOGIN AND REGISTRATION ROUTES #################


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

        return redirect(url_for("index"))

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """shows and handles user login form"""

    form = login_form()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if not user:
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)

        return redirect("/")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    """Logs out user"""
    logout_user()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
