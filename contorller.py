from flask import Flask, request, jsonify
from services import process_query
import os

app = Flask(__name__)


@app.route('/query', methods=['POST'])
def handle_query():
    # Extract account and password from the request
    expected_account = request.json['account']
    expected_password = request.json['password']

    if expected_account != os.getenv("ACCOUNT"):
        return jsonify({'error': 'account not found'}), 401

    if expected_password != os.getenv("PASSWORD"):
        return jsonify({'error': 'wrong password'}), 401

    query = request.json['query']
    result = process_query(query)

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
