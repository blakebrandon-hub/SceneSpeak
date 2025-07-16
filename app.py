from flask import Flask, render_template, request, jsonify
import requests
import base64
import os

from huggingface_hub import InferenceClient

# At top
client = InferenceClient(
    token=os.getenv("HF_TOKEN"),
    model="Salesforce/blip-image-captioning-large"
)

app = Flask(__name__)

# Optional: Set this to your actual Hugging Face API token
HUGGINGFACE_API_TOKEN = os.getenv("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
    "Content-Type": "application/octet-stream"
}

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/caption', methods=['POST'])
def caption():
    data = request.get_json()
    image_data = data.get('image_base64')

    if not image_data:
        return jsonify({'error': 'No image provided'}), 400

    image_bytes = base64.b64decode(image_data.split(",")[1])

    try:
        output = client.image_to_text(image_bytes)
        caption = output if isinstance(output, str) else output.get("generated_text", str(output))
        return jsonify({'caption': caption})
    except Exception as e:
        return jsonify({'error': 'Model error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
