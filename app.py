from flask import Flask, render_template, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

# Optional: Set this to your actual Hugging Face API token
HUGGINGFACE_API_TOKEN = os.getenv("HF_TOKEN")

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

    try:
        # Remove base64 prefix and decode
        image_base64 = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_base64)

        # Send raw image bytes as payload
        response = requests.post(API_URL, headers=HEADERS, data=image_bytes)

        print("Response:", response.status_code, response.text)

        if response.status_code == 200:
            result = response.json()
            # Defensive parsing (API may return a list or dict)
            caption = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text")
            return jsonify({'caption': caption})
        else:
            return jsonify({'error': 'Model error', 'details': response.text}), 500

    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
