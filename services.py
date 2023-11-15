import json
import os
import faiss
import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv

# Load data and Faiss index
data = pd.read_excel('phone2.xlsx')
index = faiss.read_index('index.faiss')
title_vectors = np.load('title_vectors.npy')
load_dotenv()


def process_query(query):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("OPENAI_KEY_1")}'
    }
    query_data = {
        "model": "text-embedding-ada-002",
        "input": [query]
    }
    response = requests.post('https://api.openai.com/v1/embeddings', headers=headers, json=query_data)
    print(response.json())
    query_vector = np.array(response.json()['data'][0]['embedding'])

    k = 3
    distances, indices = index.search(np.array([query_vector]), k)
    matched_data = data.iloc[indices[0]]

    def replace_none_with_na(value):
        return '無' if pd.isnull(value) else value

    matched_data = matched_data.map(replace_none_with_na)
    top_results_str = json.dumps(json.loads(matched_data.to_json(orient='records')), ensure_ascii=False)

    api_endpoint = "https://api.openai.com/v1/chat/completions"
    system_prompt = os.getenv("SYSTEM_PROMPT")
    response = requests.post(
        api_endpoint,
        headers={
            'Authorization': f'Bearer {os.getenv("OPENAI_KEY_1")}',
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "以下為json array 格式的參考資料: " + top_results_str},
                {"role": "assistant", "content": "您好，請問需要我為這些資料做什麼?"},
                {"role": "user", "content": "請根據提供的參考資料，回答以下問題:" + query
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

    return {
        'matched_data': json.loads(top_results_str),
        'generated_response': generated_response
    }
