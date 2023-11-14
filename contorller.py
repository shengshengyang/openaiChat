# Python Flask code
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from services import process_query
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
jwt = JWTManager(app)


@app.route('/login', methods=['POST'])
def login():
    expected_account = request.json.get('account', None)
    expected_password = request.json.get('password', None)

    if expected_account != os.getenv("ACCOUNT"):
        return jsonify({'error': 'account not found'}), 401

    if expected_password != os.getenv("PASSWORD"):
        return jsonify({'error': 'wrong password'}), 401

    access_token = create_access_token(identity=expected_account)
    return jsonify(access_token=access_token), 200


@app.route('/query', methods=['POST'])
@jwt_required()
def handle_query():
    query = request.json['query']
    result = process_query(query)

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
