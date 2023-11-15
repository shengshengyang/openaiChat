# Python Flask code
from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from services import process_query
import os
import pandas as pd

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
jwt = JWTManager(app)


@app.route('/index')
def index():
    data = pd.read_excel('phone2.xlsx')
    qa_list = []
    for _, row in data.iterrows():
        question = row['question']
        answer = row['answer']
        qa_list.append({'question': question, 'answer': answer})
    return render_template('index.html', qa_list=qa_list)


@app.route('/login', methods=['POST'])
def login():
    expected_account = request.json.get('account', None)
    expected_password = request.json.get('password', None)

    if expected_account != os.getenv("ACCOUNT"):
        return jsonify({'error': 'account not found'}), 401

    if expected_password != os.getenv("PASSWORD"):
        return jsonify({'error': 'wrong password'}), 401

    access_token = create_access_token(identity=expected_account)
    print(expected_account + 'is login')
    return jsonify(access_token=access_token), 200


@app.route('/query', methods=['POST'])
@jwt_required()
def handle_query():
    query = request.json['query']
    result = process_query(query)

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
