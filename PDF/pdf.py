from flask import Flask, render_template, request, jsonify, send_file
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from fpdf import FPDF
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

# Create necessary folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("pdf.html")

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    files = request.files.getlist('files')  # important: 'files' (plural) matches HTML form
    if not files:
        return jsonify({'error': 'No files provided'}), 400

    merger = PdfMerger()
    saved_files = []

    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        saved_files.append(filepath)
        merger.append(filepath)

    output_path = os.path.join(OUTPUT_FOLDER, 'merged.pdf')
    merger.write(output_path)
    merger.close()

    # Clean uploaded files
    for path in saved_files:
        os.remove(path)

    return send_file(output_path, as_attachment=True)

@app.route('/split', methods=['POST'])
def split_pdf():
    file = request.files.get('file')
    start = request.form.get('start')
    end = request.form.get('end')

    if not file or not start or not end:
        return jsonify({'error': 'File and page range are required'}), 400

    try:
        start, end = int(start), int(end)
    except ValueError:
        return jsonify({'error': 'Start and End must be integers'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    reader = PdfReader(filepath)
    writer = PdfWriter()

    if start < 1 or end > len(reader.pages) or start > end:
        return jsonify({'error': 'Invalid page range'}), 400

    for i in range(start - 1, end):
        writer.add_page(reader.pages[i])

    output_path = os.path.join(OUTPUT_FOLDER, 'split.pdf')
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    os.remove(filepath)

    return send_file(output_path, as_attachment=True)

@app.route('/images-to-pdf', methods=['POST'])
def images_to_pdf():
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No images provided'}), 400

    pdf = FPDF()
    saved_files = []

    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        saved_files.append(filepath)
        pdf.add_page()
        pdf.image(filepath, x=10, y=10, w=190)

    output_path = os.path.join(OUTPUT_FOLDER, 'images_to_pdf.pdf')
    pdf.output(output_path)

    # Clean uploaded files
    for path in saved_files:
        os.remove(path)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
