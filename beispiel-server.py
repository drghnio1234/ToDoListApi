import uuid 

from flask import Flask, request, jsonify, abort


# Initialize Server
app = Flask(__name__)

# unique IDs
todo_list_1_id = str(uuid.uuid4())
todo_list_2_id = str(uuid.uuid4())
todo_list_3_id = str(uuid.uuid4())
todo_1_id = str(uuid.uuid4())
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

# Example Data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list_id': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list_id': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list_id': todo_list_3_id},
    {'id': todo_4_id, 'name': 'Eier', 'description': '', 'list_id': todo_list_1_id},
]

# Add Headers, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Error Handling
def error(message, code):
    return jsonify({"message": message}), code

@app.errorhandler(500)
def internal_error():
    return error("Serverfehler", 500)

# Define Endpoints
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE', 'POST'])
def handle_list(list_id):
    list_item = next((l for l in todo_lists if l['id'] == list_id), None)
    if not list_item:
        return error("Liste nicht gefunden", 404)
    if request.method == 'GET':
        print(f"Getting entries for list {list_item['name']}")
        entries = [i for i in todos if i['list_id'] == list_id]
        return jsonify(entries), 200
    if request.method == 'DELETE':
        print(f"Deleting todo list {list_item['name']}")
        todo_lists.remove(list_item)
        return '', 204
    if request.method == 'POST':
        new_todo = request.get_json(force=True)
        if not new_todo or "name" not in new_todo or "description" not in new_todo:
            return error("Ungueltige Daten", 406)
        print(f"Adding new todo to list {list_item['name']}")
        new_todo['id'] = str(uuid.uuid4())
        new_todo['list_id'] = list_id
        todos.append(new_todo)
        return jsonify(new_todo), 201

@app.route('/todo-list', methods=['POST'])
def add_new_list():
    new_list = request.get_json(force=True)
    if not new_list or "name" not in new_list:
        return error("Ungueltige Daten", 406)
    print(f"Adding new todo list {new_list['name']}")
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)
    return jsonify(new_list), 201

@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    print("Getting all todo lists")
    return jsonify(todo_lists), 200

@app.route('/entry/<entry_id>', methods=['PATCH', 'DELETE'])
def handle_todo(entry_id):
    todo_item = next((t for t in todos if str(t['id']) == entry_id), None)
    if not todo_item:
        return error("Eintrag nicht gefunden", 404)
    if request.method == 'PATCH':
        updated = request.get_json(force=True)
        allowed = {"name", "description"}
        if not updated:
            return error("Ungueltige Daten", 406)
        if not any(k in allowed for k in updated):
            return error("Ungueltige Daten", 406)
        print(f"Updating todo {todo_item['name']}")
        for key in updated:
            if key in ["name", "description"]:
                todo_item[key] = updated[key]
        return jsonify(todo_item), 200
    if request.method == 'DELETE':
        print(f"Deleting todo {todo_item['name']}")
        todos.remove(todo_item)
        return '', 204

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)