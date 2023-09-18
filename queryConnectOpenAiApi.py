from flask import Flask, request, jsonify
import faiss
import numpy as np
import pandas as pd
import requests
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)

# Load data and Faiss index
data = pd.read_excel('phone2.xlsx')
index = faiss.read_index('index.faiss')
title_vectors = np.load('title_vectors.npy')
load_dotenv()

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

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("OPENAI_KEY")}'
    }
    query_data = {
        "model": "text-embedding-ada-002",
        "input": [query]
    }
    response = requests.post('https://api.openai.com/v1/embeddings', headers=headers, json=query_data)
    response_data = response.json()
    query_vector = np.array(response_data['data'][0]['embedding'])

    k = 5
    distances, indices = index.search(np.array([query_vector]), k)
    matched_data = data.iloc[indices[0]]

    def replace_none_with_na(value):
        return '無' if pd.isnull(value) else value

    matched_data = matched_data.applymap(replace_none_with_na)
    top_results_str = json.dumps(json.loads(matched_data.to_json(orient='records')), ensure_ascii=False)

    api_endpoint = "https://api.openai.com/v1/chat/completions"
    response = requests.post(
        api_endpoint,
        headers={
            'Authorization': f'Bearer {os.getenv("OPENAI_KEY")}',
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "以下為json array 格式的參考資料: " + top_results_str},
                {"role": "assistant", "content": "您好，請問需要我為這些資料做什麼?"},
                {"role": "user", "content": "請根據提供的參考資料，回答以下問題應該要找哪一位人員回答:" + query
                                            + ",若資料沒有能夠回答問題請以下列字句回復: 目前尚無資料，請洽客服"}
            ],
            "temperature": 1,
            "top_p": 1,
            "n": 1
        }
    )

    if 'choices' in response.json():
        generated_response = response.json()["choices"][0]["message"]["content"]
    else:
        generated_response = "No response choices found."

    return jsonify({
        'matched_data': json.loads(top_results_str),
        'generated_response': generated_response
    })

if __name__ == '__main__':
    app.run(debug=True)
