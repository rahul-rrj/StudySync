// Maximum allowed value for the counters
const MAX_VALUE = 1e21; // 10^21 (Same as 10000000000000000000000)

// Function to safely retrieve a number from localStorage (handles null cases)
function getStoredCount(key) {
  return parseInt(localStorage.getItem(key), 10) || 0;
}

// Function to safely store a number in localStorage
function updateStoredCount(key, value) {
  if (value < MAX_VALUE) {
    localStorage.setItem(key, value.toString());
    document.getElementById(key).textContent = value.toLocaleString();
  }
}

// Get current counts (ensure they start at 0 if undefined)
let activeUsers = getStoredCount("activeUsers");
if (localStorage.getItem("activeUsers") === null) {
  activeUsers = 0; // Start at 0 on the first visit
}

let filesConverted = getStoredCount("filesConverted");
let onlineTools = getStoredCount("onlineTools");
let pdfsCreated = getStoredCount("pdfsCreated");

// ✅ **Increase Active Users Count ONLY on Page Load**
activeUsers++;
updateStoredCount("activeUsers", activeUsers);

// Function to increment counters when respective button is clicked
function setupButtonClickHandler(buttonId, counterKey) {
  document.getElementById(buttonId).addEventListener("click", () => {
    let count = getStoredCount(counterKey) + 1;
    updateStoredCount(counterKey, count);
  });
}

// ✅ **Set up buttons to manually increment respective counters**
setupButtonClickHandler("incrementFilesConverted", "filesConverted");
setupButtonClickHandler("incrementOnlineTools", "onlineTools");
setupButtonClickHandler("incrementPdfsCreated", "pdfsCreated");

// ✅ **Initialize counters with stored values**
updateStoredCount("filesConverted", filesConverted);
updateStoredCount("onlineTools", onlineTools);
updateStoredCount("pdfsCreated", pdfsCreated);
