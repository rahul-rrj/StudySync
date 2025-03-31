# Video Editor API

This project is a Flask-based API for video editing tasks such as resizing, trimming, merging, removing audio, and extracting audio from videos. It uses FFmpeg for video processing and provides endpoints for each operation.

## Python Libraries Used

### Standard Libraries
- **os**: For file and directory operations.
- **tempfile**: For creating temporary directories and files.
- **subprocess**: For running external processes (used for FFmpeg).
- **time**: For adding delays during file removal retries.
- **io**: For handling in-memory file operations.
- **shutil**: For cleaning up temporary directories.

### Third-Party Libraries
- **Flask**: A lightweight WSGI web application framework for building the API.
- **Flask-CORS**: For enabling Cross-Origin Resource Sharing (CORS) to allow requests from different origins.
- **Werkzeug**: For utilities like `secure_filename` to handle file uploads securely.
- **ffmpeg-python**: A Python wrapper for FFmpeg, used for video and audio processing.

### External Tools
- **FFmpeg**: A command-line tool for video and audio processing. This is not a Python library but is required for the project to function.

## Installation

1. Install the required Python libraries using pip:

   ```bash
   pip install flask flask-cors werkzeug ffmpeg-python