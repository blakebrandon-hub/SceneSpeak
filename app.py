from flask import Flask, render_template, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

# Optional: Set this to your actual Hugging Face API token
HUGGINGFACE_API_TOKEN = "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" # or replace with your token directly

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/caption', methods=['POST'])
def caption():
    data = request.get_json()
    image_data = data.get('image_base64')

    if not image_data:
        return jsonify({'error': 'No image provided'}), 400

    # Remove header (e.g. "data:image/png;base64,...")
    image_base64 = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_base64)

    response = requests.post(API_URL, headers=HEADERS, files={"file": image_bytes})
    
    if response.status_code == 200:
        caption = response.json()[0]["generated_text"]
        return jsonify({'caption': caption})
    else:
        return jsonify({'error': 'Model error', 'details': response.text}), 500

if __name__ == '__main__':
    app.run(debug=True)
