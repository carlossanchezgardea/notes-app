from flask import Flask

DATABASE = 'notes_app'

app = Flask(__name__)

app.secret_key = 'secret'
