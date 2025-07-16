from flask import Flask, render_template, request, jsonify
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
import base64, io, traceback

app = Flask(__name__)

# Load the captioning model (Vit-GPT2) once at startup
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/caption', methods=['POST'])
def caption():
    try:
        image_data = request.get_json().get('image_base64')
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400

        # Decode the image
        base64_str = image_data.split(",")[1]
        image = Image.open(io.BytesIO(base64.b64decode(base64_str))).convert("RGB")

        # Preprocess
        pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
        out = model.generate(pixel_values, max_length=16, num_beams=4)
        caption = tokenizer.decode(out[0], skip_special_tokens=True)

        return jsonify({'caption': caption})

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
