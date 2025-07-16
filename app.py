from flask import Flask, render_template, request, jsonify
import base64, os, traceback, requests

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")
# Use blip2-flan-t5-xl, public inference endpoint
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip2-flan-t5-xl"

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
    img = data.get("image_base64")
    if not img:
        return jsonify({'error': 'No image provided'}), 400

    try:
        image_bytes = base64.b64decode(img.split(",",1)[1])
        response = requests.post(API_URL, headers=HEADERS, data=image_bytes)
        print("Response:", response.status_code, response.text)

        if response.status_code == 200:
            caption = response.json()[0].get("generated_text", "")
            return jsonify({'caption': caption})
        else:
            return jsonify({'error': 'Model error', 'details': response.text}), 500

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
