from flask import Flask, render_template, request, jsonify
import base64
import os
import traceback

from huggingface_hub import InferenceClient

app = Flask(__name__)

# Initialize the Hugging Face Inference Client with your token
client = InferenceClient(token=os.getenv("HF_TOKEN"))

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
        image_bytes = base64.b64decode(image_data.split(",")[1])

        # Don't specify model — InferenceClient chooses for you
        output = client.image_to_text(image_bytes)
        caption = output if isinstance(output, str) else output.get("generated_text", str(output))

        return jsonify({'caption': caption})
    except Exception as e:
        print("Error:", str(e))
        traceback.print_exc()
        return jsonify({'error': 'Model error', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
