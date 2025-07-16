from flask import Flask, render_template, request, jsonify
import base64
import os
import traceback
import requests

app = Flask(__name__)

# Hugging Face model endpoint and token
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/octet-stream"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/caption', methods=['POST'])
def caption():
    data = request.get_json()
    image_data = data.get('image_base64')

    if not image_data:
        return jsonify({'error': 'No image provided'}), 400

    try:
        # Strip base64 header and decode image
        image_bytes = base64.b64decode(image_data.split(",")[1])

        # Call Hugging Face model endpoint
        response = requests.post(API_URL, headers=HEADERS, data=image_bytes)

        print("Response:", response.status_code, response.text)

        if response.status_code == 200:
            result = response.json()
            caption = result[0]["generated_text"]
            return jsonify({'caption': caption})
        else:
            return jsonify({'error': 'Model error', 'details': response.text}), 500

    except Exception as e:
        print("Error:", str(e))
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
