from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS  
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

ALLOWED_EXTENSIONS = {'pdf'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename, file_types):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in file_types

# Render different pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/merge-pdf-page')
def merge_page():
    return render_template('merge.html')

@app.route('/split-pdf-page')
def split_page():
    return render_template('split.html')

@app.route('/convert-pdf-page')
def convert_page():
    return render_template('convert.html')

# 📌 Merge PDFs
@app.route('/merge', methods=['POST'])
def merge_pdfs():
    if 'file' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    files = request.files.getlist('file')

    if len(files) == 1:
        return send_file(io.BytesIO(files[0].read()), download_name="merged.pdf", as_attachment=True)

    merger = PdfMerger()
    for file in files:
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            merger.append(io.BytesIO(file.read()))
        else:
            return jsonify({"error": "Invalid file format"}), 400

    output = io.BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)

    return send_file(output, download_name="merged.pdf", as_attachment=True)

# 📌 Split PDF
@app.route('/split', methods=['POST'])
def split_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not allowed_file(file.filename, ALLOWED_EXTENSIONS):
        return jsonify({"error": "Invalid file format"}), 400

    try:
        start = int(request.form.get('start', 1)) - 1
        end = int(request.form.get('end', 1))

        reader = PdfReader(io.BytesIO(file.read()))
        writer = PdfWriter()

        if start < 0 or end > len(reader.pages) or start >= end:
            return jsonify({"error": "Invalid page range!"}), 400

        for page in range(start, min(end, len(reader.pages))):
            writer.add_page(reader.pages[page])

        output = io.BytesIO()
        writer.write(output)
        writer.close()
        output.seek(0)

        return send_file(output, download_name="split.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📌 Convert Images to PDF
@app.route('/images-to-pdf', methods=['POST'])
def images_to_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No images uploaded"}), 400

    files = request.files.getlist('file')
    image_list = []

    for file in files:
        if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            image = Image.open(io.BytesIO(file.read()))
            if image.mode != "RGB":
                image = image.convert("RGB")
            image_list.append(image)
        else:
            return jsonify({"error": "Invalid image format"}), 400

    if not image_list:
        return jsonify({"error": "No valid images provided"}), 400

    output = io.BytesIO()
    image_list[0].save(output, format="PDF", save_all=True, append_images=image_list[1:])
    output.seek(0)

    return send_file(output, download_name="converted.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
