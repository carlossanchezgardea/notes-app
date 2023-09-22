from notes_app import app
from flask import render_template, redirect, request, session, flash
from notes_app.models.user import User
from notes_app.models.folder import Folder
from notes_app.models.note import Note
from flask_bcrypt import Bcrypt
from notes_app.services.emails import EmailSender
from notes_app.controllers import notes

bcrypt = Bcrypt(app)


@app.route("/")
def login_redirect():
    if 'user_id' in session:
        return redirect("/home_page")
    else:
        return redirect("/log_in")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create_account", methods=['POST'])
def create_account():
    password_hash = bcrypt.generate_password_hash(request.form['password'].strip())

    file = request.files['profile_img']
    if not file:
        img_url = None
    else:
        img_url = User.upload_img_s3(file, request.form)

    data = {
        'first_name': request.form['first_name'].strip(),
        'last_name': request.form['last_name'].strip(),
        'phone_number': request.form['phone_number'].strip(),
        'email': request.form['email'].strip(),
        'password': password_hash,
        'confirm_password': request.form['confirm_password'].strip(),
        'profile_img': img_url
    }
    session['data'] = data
    if not User.validate_new_user(data):
        print("validation failed")
        return redirect("/")
    else:
        print(data)
        print("validation passed")
        print(session['data']['first_name'])
        return render_template("verify_registration.html")


@app.route("/create_user", methods=['POST'])
def confirm_user():
    data = session['data']
    user_id = User.create_new_user(data)
    session['user_id'] = user_id
    EmailSender.send_welcome_email(session['data']['email'], session['data']['first_name'])
    if not user_id:
        return redirect("/create_account")
    else:
        print(data)
        print(user_id)
        return redirect("/home_page")


@app.route("/home_page")
def home_page():
    if not 'user_id' in session:
        return redirect("/")
    else:
        data = {'user_id': session['user_id']}
        folders = Folder.get_all_folders(data)
        notes = Note.get_all_notes()
        return render_template("home_screen.html", folders=folders, notes=notes)


@app.route("/log_in")
def log_in():
    return render_template("log_in.html")


@app.route("/log_user", methods=["POST"])
def log_user():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }

    if not User.log_in_check(data):
        return redirect("/log_in")
    else:
        session['user_id'] = User.log_in_check(data)
        return redirect("/home_page")


@app.route("/log_out", methods=["POST"])
def log_out():
    session.clear()
    return redirect("/")



