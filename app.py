from flask import Flask, jsonify, request


app = Flask(__name__)
app.secret_key = 'toNieJaBylamEwa'

from werkzeug.debug import DebuggedApplication
app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
app.debug = True

app_url = '/~parzysm1/apps/noteapp'

notes = [
    {
        'id': 1,
        'title': u'Lipa',
        'description': u'Rodzaj dlugowiecznych drzew nalezacy do podrodziny lipowatych. ', 
        'category': u'Cytat',
        'tag': u'jeden'
    },
    {
        'id': 2,
        'title': u'Pies',
        'description': u'Udomowiona forma wilka szarego, ssaka drapieznego z rodziny psowatych (Canidae), uznawana przez niektorych za podgatunek wilka.', 
        'category': u'Info',
        'tag': u'cztery'
    }
]

@app.route(app_url, methods=['GET'])
def get_notes():
    return jsonify({'notes': notes})

@app.route(app_url + '/note/<int:note_id>', methods=['GET'])
def get_note(note_id):

    for note in notes:
        print note['id'] 
        if note['id'] == note_id:
            thisnote = note

    if len(thisnote) == 0:
        abort(418)
    return jsonify({'note': thisnote})
    
@app.route(app_url + '/note', methods=['POST'])
def create_note():
    if not request.json or not 'title' or not 'description' in request.json:
        abort(400)
    note = {
        'id': notes[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json['description'],
        'category': request.json.get('category', "none"),
        'tag': request.json.get('tag', "none")
    }
    notes.append(note)
    return jsonify({'note': note}), 201

@app.route(app_url + '/note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    for note in notes:
        if note['id'] == note_id:
            thisnote = note
    if len(thisnote) == 0:
        abort(404)
    if thisnote['id'] < 3:
        abort(400) 
    notes.remove(thisnote)
    return jsonify({'result': True})

@app.route(app_url + '/note/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = [note for note in notes if note['id'] == note_id]
    if len(note) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'category' in request.json and type(request.json['category']) is not unicode:
        abort(400)
    if 'tag' in request.json and type(request.json['category']) is not unicode:
        abort(400)
    note[0]['title'] = request.json.get('title', task[0]['title'])
    note[0]['description'] = request.json.get('description', task[0]['description'])
    note[0]['category'] = request.json.get('category', task[0]['category'])
    note[0]['tag'] = request.json.get('tag', task[0]['tag'])
    return jsonify({'notes': note[0]})

@app.route(app_url + '/tag/<path:note_tag>', methods=['GET'])
def get_tag(note_tag):
    thisnotes = []
    print "note_tag note_tag note_tag note_tag note_tag note_tag" + note_tag
    for note in notes:
        if note['tag'] == note_tag:
            thisnotes.append(note)
    if len(thisnotes) == 0:
        abort(404)
    return jsonify({'notes': thisnotes})

@app.route(app_url + '/category/<path:note_category>', methods=['GET'])
def get_category(note_category):
    thisnotes = []
    for note in notes:
        if note['category'] == note_category:
            thisnotes.append(note)
    if len(thisnotes) == 0:
        abort(404)
    return jsonify({'notes': thisnotes})

@app.route(app_url + '/note/<int:note_id>', methods=['POST'])
def edit_note(note_id):
    print note_id
    if not request.json or not 'title' or not 'description' in request.json:
        abort(400)
    note = {
        'id': note_id,
        'title': request.json['title'],
        'description': request.json['description'],
        'category': request.json.get('category', "none"),
        'tag': request.json.get('tag', "none")
    }
    notes.append(note)
    return jsonify({'note': note}), 201