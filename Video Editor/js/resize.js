// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const videoPreview = document.getElementById('videoPreview');
const widthInput = document.getElementById('width');
const heightInput = document.getElementById('height');
const resizeButton = document.getElementById('resizeButton');
const errorMessage = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');
const progressBar = document.querySelector('.progress');
const progress = document.querySelector('.progress-bar');

let currentVideo = null;

// Drag and drop handlers
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

function handleFile(file) {
    const sizeValidation = validateFileSize(file);
    if (!sizeValidation.valid) {
        showError(sizeValidation.message);
        return;
    }

    const typeValidation = validateFileType(file, ['video/']);
    if (!typeValidation.valid) {
        showError(typeValidation.message);
        return;
    }

    const videoUrl = URL.createObjectURL(file);
    videoPreview.src = videoUrl;
    currentVideo = file;

    // Show file info
    const fileInfo = document.createElement('div');
    fileInfo.className = 'file-info';
    fileInfo.innerHTML = `
        <div>File: ${file.name}</div>
        <div class="file-size">Size: ${formatFileSize(file.size)}</div>
        <div class="file-type">Type: ${file.type}</div>
    `;
    videoPreview.parentNode.insertBefore(fileInfo, videoPreview.nextSibling);

    resizeButton.disabled = false;
    showSuccess('Video loaded successfully');
}

function setPresetDimensions(width, height) {
    widthInput.value = width;
    heightInput.value = height;
    validateResizeInputs();
}

// Dimension input validation
widthInput.addEventListener('input', validateResizeInputs);
heightInput.addEventListener('input', validateResizeInputs);

function validateResizeInputs() {
    const width = parseInt(widthInput.value);
    const height = parseInt(heightInput.value);
    
    if (width <= 0 || height <= 0) {
        showError('Dimensions must be positive numbers');
        resizeButton.disabled = true;
    } else {
        resizeButton.disabled = false;
        hideError();
    }
}

// Resize video
resizeButton.addEventListener('click', async () => {
    if (!currentVideo) {
        showError('Please select a video first');
        return;
    }

    const formData = new FormData();
    formData.append('video', currentVideo);
    formData.append('width', widthInput.value);
    formData.append('height', heightInput.value);

    showProcessing('Resizing video...');
    try {
        await makeApiCall('resize', formData, updateProcessingProgress);
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        hideProcessing();
    }
});

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    successMessage.style.display = 'none';
}

function showSuccess(message) {
    successMessage.textContent = message;
    successMessage.style.display = 'block';
    errorMessage.style.display = 'none';
}

function hideError() {
    errorMessage.style.display = 'none';
} 