from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS  
from PIL import Image
import io
from rembg import remove  # Import background remover

app = Flask(__name__)  # ✅ Fix: Corrected `__name__`
CORS(app)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@app.route("/")
def home():
    return render_template("bremover.html")
# 📌 Remove Background from Image
@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'file' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['file']
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid image format"}), 400

    try:
        input_image = Image.open(io.BytesIO(file.read()))
        output_image = remove(input_image)  # Remove background

        output_bytes = io.BytesIO()
        output_image.save(output_bytes, format="PNG")  # Ensure output is PNG
        output_bytes.seek(0)

        return send_file(output_bytes, mimetype="image/png", download_name="no-bg.png", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
