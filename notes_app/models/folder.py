from notes_app.config.mysqlconnection import connectToMySQL
from notes_app import app, DATABASE
from notes_app.models.note import Note


class Folder:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.notes = []

    @classmethod
    def get_all_folders(cls, user_id):
        query = "SELECT * FROM folders where user_id = %(user_id)s"
        results = connectToMySQL(DATABASE).query_db(query, user_id)
        folders = []

        for folder_data in results:
            new_folder = cls(folder_data)
            folders.append(new_folder)

            # Query to get all notes belonging to this folder
            note_query = "SELECT * FROM notes WHERE folder_id = %(id)s ORDER BY created_at DESC;"
            data = {'id': new_folder.id}
            note_results = connectToMySQL(DATABASE).query_db(note_query, data)

            # Attach notes to folder
            for note in note_results:
                new_folder.notes.append(Note(note))

        return folders

    @classmethod
    def get_all_folders_raw(cls, user_id):
        query = "SELECT * FROM folders where user_id = %(user_id)s"
        results = connectToMySQL(DATABASE).query_db(query, user_id)
        return results

    @classmethod
    def create_folder(cls, data):
        query = '''
        INSERT INTO folders (name, user_id)
        VALUES (%(name)s, %(user_id)s);
        '''
        folder_id = connectToMySQL(DATABASE).query_db(query, data)
        return folder_id


