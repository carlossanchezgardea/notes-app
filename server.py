from notes_app import app
from notes_app.controllers import folders
from notes_app.controllers import users
from notes_app.controllers import notes

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9000)
