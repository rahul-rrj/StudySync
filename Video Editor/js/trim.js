// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const videoPreview = document.getElementById('videoPreview');
const startTimeInput = document.getElementById('startTime');
const endTimeInput = document.getElementById('endTime');
const trimButton = document.getElementById('trimButton');
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

    trimButton.disabled = false;
    showSuccess('Video loaded successfully');
}

// Time input validation
startTimeInput.addEventListener('input', validateTimeInputs);
endTimeInput.addEventListener('input', validateTimeInputs);

function validateTimeInputs() {
    const start = parseFloat(startTimeInput.value);
    const end = parseFloat(endTimeInput.value);
    
    if (start >= end || start < 0) {
        showError('Invalid time range');
        trimButton.disabled = true;
    } else {
        trimButton.disabled = false;
        hideError();
    }
}

// Trim video
trimButton.addEventListener('click', async () => {
    if (!currentVideo) {
        showError('Please select a video first');
        return;
    }

    const formData = new FormData();
    formData.append('video', currentVideo);
    formData.append('start_time', startTimeInput.value);
    formData.append('end_time', endTimeInput.value);

    showProcessing('Trimming video...');
    try {
        await makeApiCall('trim', formData, updateProcessingProgress);
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