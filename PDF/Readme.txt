To run your Flask PDF manager on your system, follow these steps:

---

## **1️⃣ Install Python and Required Libraries**
Ensure you have Python installed (preferably Python 3.8+). You can check by running:

```sh
python --version
```

or

```sh
python3 --version
```

If not installed, download it from [python.org](https://www.python.org/).

### **Install Required Libraries**
Navigate to your project folder and install dependencies using:

```sh
pip install flask flask-cors pypdf2 pillow
```

---

## **2️⃣ Run the Flask Server**
Save your `app.py` file in a project directory. Open a terminal in that directory and run:

```sh
python app.py
```

or

```sh
python3 app.py
```

If everything is correct, you should see output like:

```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

---

## **3️⃣ Open the Web App**
- Save your **HTML file** in the same folder (e.g., `index.html`).
- Open `index.html` in a **web browser**.

---

## **4️⃣ Testing**
- **Merge PDFs**: Upload multiple PDFs and check if they merge correctly.
- **Split PDF**: Upload a single PDF and provide a start & end page range.
- **Convert Images to PDF**: Upload image files to test conversion.

---

## **5️⃣ Troubleshooting**
### **Port Already in Use?**
If you see an error about the port, try running:

```sh
python app.py --port 5001
```

Then access it at `http://127.0.0.1:5001/`.

### **CORS Errors?**
If you face cross-origin issues while accessing from a different domain, ensure `flask_cors` is properly installed and added:

```sh
pip install flask-cors
```

Let me know if you face any issues! 🚀