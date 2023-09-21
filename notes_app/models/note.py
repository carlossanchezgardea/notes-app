from notes_app.config.mysqlconnection import connectToMySQL
from notes_app import app, DATABASE


class Note:
    def __init__(self, data):
        self.id = data['id']
        self.dtype = data['dtype']
        self.title = data['title']
        self.description = data['description']
        self.body = data['body']
        self.user_id = data['user_id']
        self.folder_id = data['folder_id']

    @classmethod
    def get_all_notes(cls):
        query = "SELECT * FROM notes"
        results = connectToMySQL(DATABASE).query_db(query)
        notes = []
        for note in results:
            notes.append(cls(note))

        return notes

    @classmethod
    def get_all_notes_raw(cls, data):
        query = "SELECT * FROM notes WHERE folder_id = %(folder_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_folder_notes(cls, data):
        query = "SELECT * FROM notes WHERE folder_id = %(folder_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        notes = []
        if results:
            for note in results:
                notes.append(cls(note))

            return notes
        else:
            notes = []
            return notes

    @classmethod
    def create_note(cls, data):
        query = '''
        INSERT INTO notes (dtype, title, description, body, user_id, folder_id)
        VALUES ("user_get", %(title)s, %(description)s, %(body)s, %(user_id)s, %(folder_id)s);
        '''
        note_id = connectToMySQL(DATABASE).query_db(query, data)
        return note_id

    @classmethod
    def get_one_note(cls, data):
        query = "SELECT * FROM notes WHERE id = %(id)s and user_id = %(user_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return results[0]
        else:
            return "No note found"


# info = {
#     'id': 35,
#     'user_id': 5
# }
#
# note_check = Note.get_one_note(info)
# print(note_check.title)