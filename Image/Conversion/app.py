from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
ALLOWED_OUTPUT_FORMATS = {'png', 'jpg', 'jpeg', 'webp', 'gif', 'svg', 'abif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@app.route('/convert-format', methods=['POST'])
def convert_format():
    if 'file' not in request.files or 'format' not in request.form:
        return jsonify({"error": "Missing file or format"}), 400

    file = request.files['file']
    target_format = request.form['format'].lower()

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid image format"}), 400

    if target_format not in ALLOWED_OUTPUT_FORMATS:
        return jsonify({"error": "Invalid target format"}), 400

    try:
        input_image = Image.open(io.BytesIO(file.read()))

        # Convert "jpg" to "JPEG" (Pillow requires "JPEG")
        if target_format == "jpg":
            target_format = "JPEG"

        # SVG & ABIF Handling
        if target_format == "svg":
            return jsonify({"error": "SVG format is not supported for saving"}), 400
        if target_format == "abif":
            return jsonify({"error": "ABIF format is not supported"}), 400

        output_bytes = io.BytesIO()
        input_image.save(output_bytes, format=target_format.upper())  
        output_bytes.seek(0)

        return send_file(output_bytes, mimetype=f"image/{target_format.lower()}", download_name=f"converted-image.{target_format.lower()}", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
