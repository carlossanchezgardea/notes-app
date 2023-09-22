from notes_app import app
from flask import request, session, jsonify, redirect
from notes_app.models.note import Note
from notes_app.services.emails import EmailSender


@app.route("/create_note", methods=['POST'])
def new_note():
    data = {
        'dtype': 'user_gen',
        'title': request.form['title'],
        'description': request.form['description'],
        'body': request.form['body'],
        'user_id': session['user_id'],
        'folder_id': request.form['folder_id']
    }

    note_id = Note.create_note(data)
    return jsonify({'note_id': note_id})


@app.route("/api/load_notes")
def get_all_notes():
    folder_id = request.args.get('folder_id')
    session['folder_id'] = folder_id
    data = {
        'folder_id': session['folder_id']
    }
    return jsonify(Note.get_all_notes_raw(data))


@app.route("/api/load_single_note")
def get_single_note():
    user_id = session['user_id']
    note_id = request.args.get('note_id')
    data = {
        'id': note_id,
        'user_id': user_id
    }
    return jsonify(Note.get_one_note(data))


@app.route("/api/update_note", methods=['POST'])
def update_note():
    note_id = request.form.get('note_id')
    title = request.form.get('title')
    description = request.form.get('description')
    body = request.form.get('body')
    user_id = session['user_id']
    dtype = 'user_get'
    data = {
        'id': note_id,
        'user_id': user_id,
        'dtype': dtype,
        'title': title,
        'description': description,
        'body': body
    }
    Note.update_note(data)
    return 'should work?'


@app.route("/send_note", methods=['POST'])
def send_note():
    email = request.form.get('email')
    title = request.form.get('title')
    description = request.form.get('description')
    body = request.form.get('body')

    EmailSender.send_requested_note(email, title, description, body)

    return redirect("/home_page")
