import io
from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
from PIL import Image

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  # Enable CORS for frontend requests

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resize', methods=['POST'])
def resize_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        image_file = request.files['image']
        width = int(request.form.get('width', 800))
        height = int(request.form.get('height', 600))

        # Open the image
        img = Image.open(image_file)

        # Resize the image
        resized_img = img.resize((width, height), Image.LANCZOS)

        # Prepare the image buffer
        img_buffer = io.BytesIO()
        img_format = img.format or "JPEG"  # Default to JPEG if format is missing
        resized_img.save(img_buffer, format=img_format)
        img_buffer.seek(0)

        # Return the resized image
        return send_file(img_buffer, mimetype=f'image/{img_format.lower()}')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
