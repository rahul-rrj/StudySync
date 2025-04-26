# SyncSphere - Professional File Management Platform

## Overview
SyncSphere is a comprehensive and collaboraive enabling group communication and platform that includes various tools for handling PDFs, images, videos, and AI-powered text processing.
## Prerequisites
- Python 3.8 or higher
- FFmpeg (required for video processing)

## Project Structure
- AI Tools: AI writing, grammar checking, and note-taking
- Image Tools: Format conversion, resizing, and background removal
- PDF Tools: Merging, splitting, and image-to-PDF conversion
- Video Tools: Video editing, trimming, and format conversion

## Installation

### 1. Python Dependencies
Install all required Python packages using pip:

```bash
pip install flask
pip install flask-cors
pip install Pillow
pip install PyPDF2
pip install fpdf
pip install ffmpeg-python
pip install werkzeug
pip install language-tool-python
pip install sumy
pip install transformers
pip install torch
pip install nltk
pip install wikipedia-api

### 2. External Dependencies FFmpeg Installation (for Video Processing)
- Windows:
  1. Download FFmpeg from the official website
  2. Add FFmpeg to system PATH


  ### 3. NLTK Data
After installing NLTK, download required data:

```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
 ```

```markdown
# SyncSphere - Professional File Management Platform

## Overview
SyncSphere is a comprehensive file management platform that includes various tools for handling PDFs, images, videos, and AI-powered text processing.

## Prerequisites
- Python 3.8 or higher
- FFmpeg (required for video processing)

## Project Structure
- AI Tools: AI writing, grammar checking, and note-taking
- Image Tools: Format conversion, resizing, and background removal
- PDF Tools: Merging, splitting, and image-to-PDF conversion
- Video Tools: Video editing, trimming, and format conversion

## Installation

### 1. Python Dependencies
Install all required Python packages using pip:

```bash
pip install flask
pip install flask-cors
pip install Pillow
pip install PyPDF2
pip install fpdf
pip install ffmpeg-python
pip install werkzeug
pip install language-tool-python
pip install sumy
pip install transformers
pip install torch
pip install nltk
pip install wikipedia-api
 ```
```

### 2. External Dependencies FFmpeg Installation (for Video Processing)
- Windows:
  1. Download FFmpeg from the official website
  2. Add FFmpeg to system PATH
### 3. NLTK Data
After installing NLTK, download required data:

```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
 ```

## Module-specific Dependencies
### 1. PDF Processing
- Flask
- PyPDF2
- FPDF
- Werkzeug
### 2. Image Processing
- Flask
- Pillow (PIL)
- Flask-CORS
### 3. Video Processing
- Flask
- ffmpeg-python
- Werkzeug
- Flask-CORS
### 4. AI Tools
- Flask
- language-tool-python
- sumy
- transformers
- torch
- nltk
- wikipedia-api
- Flask-CORS


## Browser Requirements
- Modern web browser with JavaScript enabled
- Support for HTML5 and CSS3
- Recommended browsers: Chrome, Firefox, Edge (latest versions)
## Frontend Dependencies
- Tailwind CSS (via CDN)
- Font Awesome 6.5.1 (via CDN)
- Google Fonts (Montserrat, Orbitron)
- Swiper JS (for sliders)
- AOS (Animate On Scroll library)
## Notes
- Ensure all Python dependencies are installed in your virtual environment
- FFmpeg must be properly installed and accessible from the system PATH for video processing
- Some features require active internet connection (AI tools, font loading)



This README provides a comprehensive overview of all dependencies required to run the SyncSphere platform. It includes both backend and frontend dependencies, as well as instructions for installation and setup.
