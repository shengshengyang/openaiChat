import os
import pandas as pd
import requests
import faiss
import numpy as np
from dotenv import load_dotenv

def clean_and_reinput(data_path, index_path, vectors_path):
    # Delete existing index and vectors files if they exist
    if os.path.exists(index_path):
        os.remove(index_path)
    if os.path.exists(vectors_path):
        os.remove(vectors_path)

    print("clean all the index and data")

    # Initialize index and title_vectors to None
    index = None
    title_vectors = None

    try:
        # Read data from Excel file
        data = pd.read_excel(data_path)

        # Vectorize the titles
        title_vectors = []
        for _, row in data.iterrows():
            # Get the title text
            title = row['title']

            # Prepare the request payload
            payload = {
                "model": "text-embedding-ada-002",
                "input": [title]
            }

            # Set the headers with the API key
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            # Send the request to the OpenAI API
            response = requests.post("https://api.openai.com/v1/embeddings", headers=headers, json=payload)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the vector embedding from the response
                embedding = response.json()['data'][0]['embedding']
                print(embedding)
                # Add the embedding to the title_vectors list
                title_vectors.append(embedding)
            else:
                raise Exception(f"Request failed with status code {response.status_code}")

        # Convert title_vectors to a NumPy array
        title_vectors = np.array(title_vectors)

        # Initialize Faiss index
        index = faiss.IndexFlatL2(title_vectors.shape[1])

        # Add title vectors to the index
        index.add(title_vectors)

        # Save the index and title vectors to files
        faiss.write_index(index, index_path)
        np.save(vectors_path, title_vectors)

        print("Data cleaning and re-input successful.")
    except Exception as e:
        print("Error occurred during data cleaning and re-input:", str(e))

    return index, title_vectors


# Example usage
load_dotenv()
data_path = 'phone2.xlsx'
index_path = 'index.faiss'
vectors_path = 'title_vectors.npy'
api_key = os.getenv("OPENAI_KEY")

index, title_vectors = clean_and_reinput(data_path, index_path, vectors_path)
