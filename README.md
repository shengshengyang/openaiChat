# openaiChat

### Prerequisites
Ensure you have the following installed on your machine:

- Python 3.x
- pip (Python package installer)

### Installation
1. Clone this repository to your local machine.
2. Install the necessary Python packages by running the following command in your terminal:
    ```commandline
    pip install -r requirements.txt
    ```
3. Depending on your device, install the appropriate version of the Faiss database:
    ```commandline
    For CPU version
    pip install faiss-cpu
    
    For GPU version
    pip install faiss-gpu
    ```
### Configuration
Input your OpenAI API key into the <span style="color:green"> .env</span> file:
```
OPENAI_KEY=<YOUR_API_KEY>
```