import json
from uuid import uuid4

from flask import Flask, request

app = Flask(__name__)

user_id_1 = uuid4().__str__()
user_id_2 = uuid4().__str__()
user_id_3 = uuid4().__str__()
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid4().__str__()
todo_2_id = uuid4().__str__()
todo_3_id = uuid4().__str__()
todo_4_id = uuid4().__str__()

# define internal data structures with example data
user_list = [
    {'id': user_id_1, 'name': 'Name1'},
    {'id': user_id_2, 'name': 'Name2'},
    {'id': user_id_3, 'name': 'Name3'},
]
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Liste 1'},
    {'id': todo_list_2_id, 'name': 'Liste 2'},
    {'id': todo_list_3_id, 'name': 'Liste 3'},
]
todos = [
    {'id': todo_1_id, 'name': 'I1L1', 'I2L1': '', 'list': todo_list_1_id, 'user': user_id_1},
    {'id': todo_2_id, 'name': 'I1L2', 'I2L2': '', 'list': todo_list_2_id, 'user': user_id_2},
    {'id': todo_3_id, 'name': 'I1L3', 'I2L3': '', 'list': todo_list_3_id, 'user': user_id_2},
    {'id': todo_3_id, 'name': 'I1L3', 'I1L3': '', 'list': todo_list_1_id, 'user': user_id_1},
]


def listExists(list_id):
    for list in todo_lists:
        if list['id'] == list_id:
            return True
    return False


@app.route('/todo-list/<list_id>', methods=['GET'])
def getTodolist(list_id):
    if not listExists(list_id):
        return 'list does not exists', 404
    entrys = []
    for entry in todos:
        if entry["list"] == list_id:
            entrys.append(entry)
    return entrys.__str__()


@app.route('/todo-list/<list_id>/entry', methods=['PUT'])
def addEntry(list_id):
    if not listExists(list_id):
        return 'list does not exists', 404
    data = request.get_json()
    try:
        data['name']
        data['description']
    except KeyError:
        return 'missing data', 404
    entry = {'id': uuid4().__str__(),
             'name': data['name'],
             'description': data['description'],
             'user': '0',
             'list': list_id
             }
    todos.append(entry)
    return entry, 200


@app.route('/todo-list/<list_id>', methods=['DELETE'])
def deleteTodolist(list_id):
    index = None
    for list in todo_lists:
        if list['id'] == list_id:
            index = todo_lists.index(list)
            break
    if index != None:
        todo_lists.pop(index)
        return '', 200
    return '', 404


@app.route('/todo-list', methods=['POST'])
def createTodolist():
    data = request.get_json()
    try:
        data['name']
    except KeyError:
        return 'missing data', 404
    todo_list = {'id': uuid4().__str__(),
                 'name': data['name'],
                 }
    todo_lists.append(todo_list)
    return todo_list, 200


@app.route('/todo-list/<list_id>/<entry_id>', methods=['PUT'])
def updateEntry(list_id, entry_id):
    if not listExists(list_id):
        return 'list does not exists', 404
    data = request.get_json()
    try:
        data['name']
        data['description']
    except KeyError:
        return 'missing data', 404
    for entry in todos:
        if entry['id'] == entry_id:
            if entry["list"] == list_id:
                entry['name'] = data['name']
                entry['description'] = data['description']
                todos.insert(todos.index(entry), entry)
                return entry, 200
    return 'entry not found', 404


@app.route('/user', methods=['GET'])
def getAllUsers():
    return json.loads(json.dumps(user_list.__str__())), 200


@app.route('/user', methods=['POST'])
def createUser():
    data = request.get_json()
    try:
        data['name']
    except KeyError:
        return 'missing data', 404
    user = {
        'id': uuid4().__str__(),
        'name': data['name']
    }
    user_list.append(user)
    return user


@app.route('/user/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    index = None
    for user in user_list:
        if user['id'] == user_id:
            index = user_list.index(user)
            break
    if index != None:
        user_list.pop(index)
        return '', 200
    return '', 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=1)
