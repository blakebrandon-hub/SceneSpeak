const video = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const describeBtn = document.getElementById('describe-btn');
const statusText = document.getElementById('status');
const muteBtn = document.getElementById('toggle-sound');

let muted = false;

// 📷 Setup webcam
async function setupWebcam() {
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.srcObject = stream;
  return new Promise((resolve) => {
    video.onloadedmetadata = () => resolve(video);
  });
}

// 🔊 Speak text aloud
function speak(text) {
  if (muted) return;
  const utterance = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(utterance);
}

// 🖼️ Capture current frame as base64
function captureImage() {
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL('image/png'); // returns base64 string
}

// 📤 Send image to backend
async function describeScene() {
  const imageData = captureImage();
  statusText.textContent = "Describing scene...";

  const response = await fetch('/caption', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image_base64: imageData })
  });

  if (!response.ok) {
    statusText.textContent = "Error getting description.";
    return;
  }

  const data = await response.json();

  if (data.caption) {
    statusText.textContent = `Scene: ${data.caption}`;
    speak(data.caption);
  } else {
    statusText.textContent = "No caption returned.";
  }
}

// 🎛️ Mute button toggle
muteBtn.addEventListener('click', () => {
  muted = !muted;
  muteBtn.textContent = muted ? "Unmute" : "Mute";
});

// 🎬 Initialize
setupWebcam();
describeBtn.addEventListener('click', describeScene);
