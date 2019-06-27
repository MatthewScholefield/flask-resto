from flask import Flask
from uuid import uuid4
from werkzeug.exceptions import NotFound

from flask_resto import Api

app = Flask(__name__)
api = Api(app)

notes = {}  # In practice, use a database


class Note:
    def create(self):
        note = {
            'title': api.json['title'],
            'description': api.json['description'],
            'uuid': str(uuid4())
        }
        notes[note['uuid']] = note
        return note

    def delete(self, uuid):
        Note.get_note(uuid)
        del notes[uuid]

    def get(self, uuid):
        return Note.get_note(uuid)

    def get_all(self):
        return notes

    def update(self, uuid):
        note = Note.get_note(uuid)
        note.update(api.json)
        return note

    @staticmethod
    def get_note(uuid):
        note = notes.get(uuid)
        if not note:
            raise NotFound(uuid)
        return note


api.resources = {
    '/v1': {
        '/note': {
            'POST': Note.create,
            'GET': Note.get_all,
            '/<uuid>': {
                'GET': Note.get,
                'PATCH': Note.update,
                'DELETE': Note.delete
            }
        }
    }
}

if __name__ == '__main__':
    app.run()
