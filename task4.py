from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    "1": {"name": "Alice", "email": "alice@example.com"},
    "2": {"name": "Bob", "email": "bob@example.com"}
}
next_user_id = 3 

@app.route('/')
def home():
    return "Welcome to the User Management API! Use /users to manage users."

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    global next_user_id
    data = request.json
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"message": "Name and email are required"}), 400

    new_user_id = str(next_user_id)
    users[new_user_id] = {"name": data['name'], "email": data['email']}
    next_user_id += 1
    return jsonify({"message": "User created successfully", "user_id": new_user_id, "user": users[new_user_id]}), 201

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    if not data:
        return jsonify({"message": "No data provided for update"}), 400

    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']

    return jsonify({"message": "User updated successfully", "user": user})

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)