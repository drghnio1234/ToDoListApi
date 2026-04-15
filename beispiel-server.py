import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = str(uuid.uuid4())
todo_list_2_id = str(uuid.uuid4())
todo_list_3_id = str(uuid.uuid4())
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# define endpoint for getting and deleting existing todo lists and posting entries to existing todo lists
@app.route('/list/<list_id>', methods=['GET', 'DELETE', 'POST'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list'] == list_id])
    elif request.method == 'DELETE':
        # delete list with given id
        print(f'Deleting todo list {list_item['name']}')
        todo_lists.remove(list_item)
        return '', 200
    elif request.method == 'POST':
        # make JSON from POST data (even if content type is not set correctly)
        new_todo = request.get_json(force=True)
        print(f'Got new todo to be added: {format(new_todo)} under the list {list_item['name']}')
        # create id for new list, save it and return the list with id
        new_todo['id'] = uuid.uuid4()
        new_todo['list'] = list_id
        todos.append(new_todo)
        return jsonify(new_todo), 200

# define endpoint for adding a new list
@app.route('/list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print(f'Got new list to be added: {format(new_list)}')
    # create id for new list, save it and return the list with id
    new_list['id'] = uuid.uuid4()
    todo_lists.append(new_list)
    return jsonify(new_list), 200


# define endpoint for getting all lists
@app.route('/lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists)

@app.route('/todos/<todo_id>', methods=['PATCH', 'DELETE'])
def handle_todo(todo_id):
    todo_item = None
    for t in todos:
        if str(t['id']) == todo_id:
            todo_item = t
            break
    if not todo_item:
        abort(404)
    if request.method == 'PATCH':
        # make JSON from POST data (even if content type is not set correctly)
        updated_todo = request.get_json(force=True)
        print(f'Got update for todo {todo_item['name']}: {format(updated_todo)}')
        # update the existing todo item with the new values
        for i in updated_todo:
            todo_item[i] = updated_todo[i]
        return jsonify(todo_item), 200
    elif request.method == 'DELETE':
        print(f'Deleting todo {todo_item['name']}')
        todos.remove(todo_item)
        return '', 200

if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
