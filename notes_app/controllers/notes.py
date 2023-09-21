from notes_app import app
from flask import request, session, jsonify
from notes_app.models.note import Note


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
    Note.create_note(data)
    print(F"WE GET THIS {data}")
    return ""


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
