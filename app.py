from flask import Flask, render_template, request, jsonify
import requests, traceback

app = Flask(__name__)

# Public space endpoint
SPACE_URL = "https://hf.space/embed/ovi054/image-to-prompt/run/predict"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/caption', methods=['POST'])
def caption():
    data = request.get_json()
    img = data.get('image_base64')
    if not img:
        return jsonify({'error': 'No image provided'}), 400

    try:
        # Send base64 image in JSON payload
        resp = requests.post(SPACE_URL, json={"data": [img]})
        print("Response:", resp.status_code, resp.text)

        if resp.status_code == 200:
            result = resp.json().get("data", [])
            caption = result[0] if result else "No caption returned"
            return jsonify({'caption': caption})
        else:
            return jsonify({'error': 'Space error', 'details': resp.text}), 500

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
