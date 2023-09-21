from notes_app import app
from flask import redirect, request, session, jsonify
from notes_app.models.folder import Folder


@app.route("/create_folder", methods=['POST'])
def new_folder():
    data = {
        'name': request.form['name'],
        'user_id': session['user_id']
    }
    Folder.create_folder(data)
    print(data)
    return redirect('/home_page')


@app.route("/api/load_folders")
def get_raw_folders():
    user_id = session['user_id']
    data = {
        'user_id': user_id
    }
    return jsonify(Folder.get_all_folders_raw(data))
