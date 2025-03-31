// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const videoList = document.getElementById('videoList');
const mergeButton = document.getElementById('mergeButton');
const errorMessage = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');
const progressBar = document.querySelector('.progress');
const progress = document.querySelector('.progress-bar');

let selectedVideos = [];

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
    const files = Array.from(e.dataTransfer.files).filter(file => file.type.startsWith('video/'));
    handleFiles(files);
});

fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files).filter(file => file.type.startsWith('video/'));
    handleFiles(files);
});

function handleFiles(files) {
    if (files.length === 0) {
        showError('Please select valid video files');
        return;
    }

    selectedVideos = [...selectedVideos, ...files];
    updateVideoList();
    mergeButton.disabled = false;
    showSuccess(`Added ${files.length} video(s)`);
}

function updateVideoList() {
    videoList.innerHTML = '';
    selectedVideos.forEach((video, index) => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            ${video.name}
            <span class="badge bg-danger rounded-pill" style="cursor: pointer;" onclick="removeVideo(${index})">×</span>
        `;
        videoList.appendChild(li);
    });
}

function removeVideo(index) {
    selectedVideos.splice(index, 1);
    updateVideoList();
    if (selectedVideos.length === 0) {
        mergeButton.disabled = true;
    }
}

// Merge videos
mergeButton.addEventListener('click', async () => {
    if (selectedVideos.length < 2) {
        showError('Please select at least 2 videos to merge');
        return;
    }

    const formData = new FormData();
    selectedVideos.forEach((video, index) => {
        formData.append('videos', video);
    });

    showProcessing('Merging videos...');
    try {
        await makeApiCall('merge', formData, updateProcessingProgress);
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