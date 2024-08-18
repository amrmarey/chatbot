from flask import Flask, request, jsonify, send_from_directory
from transformers import pipeline

app = Flask(__name__)

# Load the model and tokenizer from Hugging Face
model = pipeline("text-generation", model="gpt2")

def query_local_model(prompt):
    # Generate text using the local model
    response = model(prompt, max_length=150, num_return_sequences=1)
    return response[0]['generated_text']

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Generate a response using the local model
    bot_response = query_local_model(user_message)
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
