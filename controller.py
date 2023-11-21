# Python Flask code
from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_restful import Api, Resource
from services import process_query, query_closest
import os
import pandas as pd
from flasgger import Swagger

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
api = Api(app)
jwt = JWTManager(app)
swagger = Swagger(app)


@app.route('/index')
def index():
    data = pd.read_excel('phone2.xlsx')
    qa_list = []
    for _, row in data.iterrows():
        question = row['question']
        answer = row['answer']
        qa_list.append({'question': question, 'answer': answer})
    return render_template('index.html', qa_list=qa_list)


@app.route('/')
def login():
    return render_template('query.html')


@app.route('/login', methods=['POST'])
def show_login():
    """
     Show login
     ---
     consumes:
        - application/json
     parameters:
       - name: body
         in: body
         type: string
         required: true
         description: Account
         example: '{"account": "admin", "password": "2759"}'
     responses:
       200:
         description: Login successful
       401:
         description: Unauthorized
"""
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
    """
Handle user queries
---
tags:
  - Query
parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: Bearer token for authentication
  - name: query
    in: body
    required: true
    schema:
      type: object
      properties:
        query:
          type: string
          description: The user's query
responses:
  200:
    description: Successful response
    schema:
      type: object
      properties:
        generated_response:
          type: string
          description: The generated response
        matched_data:
          type: array
          items:
            type: object
            properties:
              answer:
                type: string
                description: The answer to the question:
                type: string
                description: The question asked
  401:
    description: Unauthorized
"""

    query = request.json['query']
    result = process_query(query)

    return jsonify(result)


@app.route('/query/closest', methods=['POST'])
def handle_query_closest():
    query = request.json['query']
    result = query_closest(query)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
