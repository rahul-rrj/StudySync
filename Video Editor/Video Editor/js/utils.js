// Utility functions shared across all tools

// API Configuration
const API_CONFIG = {
    baseUrl: window.location.hostname === 'localhost' ? 'http://localhost:5000' : 'http://' + window.location.hostname + ':5000',
    timeout: 300000 // 5 minutes timeout
};

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function validateFileSize(file) {
    const maxSize = 500 * 1024 * 1024; // 500MB
    if (file.size > maxSize) {
        return {
            valid: false,
            message: `File size exceeds 500MB limit. Your file: ${formatFileSize(file.size)}`
        };
    }
    return { valid: true };
}

function validateFileType(file, allowedTypes) {
    if (!allowedTypes.some(type => file.type.startsWith(type))) {
        return {
            valid: false,
            message: `Invalid file type. Allowed types: ${allowedTypes.join(', ')}`
        };
    }
    return { valid: true };
}

function showProcessing(message = 'Processing your video...') {
    const overlay = document.getElementById('processingOverlay');
    if (overlay) {
        const messageEl = overlay.querySelector('.processing-message');
        if (messageEl) {
            messageEl.textContent = message;
        }
        overlay.style.display = 'flex';
    }
}

function hideProcessing() {
    const overlay = document.getElementById('processingOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

function updateProcessingProgress(progress) {
    const progressBar = document.querySelector('.processing-progress-bar');
    if (progressBar) {
        progressBar.style.width = `${progress}%`;
    }
}

function showRetryButton() {
    const retryButton = document.getElementById('retryButton');
    if (retryButton) {
        retryButton.style.display = 'block';
    }
}

function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }
    const successMessage = document.getElementById('successMessage');
    if (successMessage) {
        successMessage.style.display = 'none';
    }
}

function showSuccess(message) {
    const successMessage = document.getElementById('successMessage');
    if (successMessage) {
        successMessage.textContent = message;
        successMessage.style.display = 'block';
    }
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
        errorMessage.style.display = 'none';
    }
}

function handleNetworkError(error) {
    console.error('Network Error:', error);
    if (!navigator.onLine) {
        showError('No internet connection. Please check your connection and try again.');
    } else {
        showError('Network error. Please try again. If the problem persists, check if the server is running.');
    }
    hideProcessing();
    showRetryButton();
}

async function makeApiCall(endpoint, formData, onProgress) {
    try {
        showProcessing('Processing your video...');
        
        // Create an AbortController for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);

        const response = await fetch(`${API_CONFIG.baseUrl}/${endpoint}`, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json',
            },
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: 'Unknown error occurred' }));
            throw new Error(errorData.error || `Server error: ${response.status}`);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${endpoint}_video.mp4`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showSuccess(`${endpoint} completed successfully!`);
        if (onProgress) onProgress(100);
    } catch (error) {
        console.error('API Error:', error);
        if (error.name === 'AbortError') {
            showError('Request timed out. Please try again.');
        } else {
            handleNetworkError(error);
        }
        throw error;
    } finally {
        hideProcessing();
    }
}

// Add network status monitoring
window.addEventListener('online', () => {
    const retryButton = document.getElementById('retryButton');
    if (retryButton) {
        retryButton.style.display = 'none';
    }
});

window.addEventListener('offline', () => {
    showError('No internet connection. Please check your connection and try again.');
    showRetryButton();
}); 