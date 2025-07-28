# 📸 SceneSpeak

**SceneSpeak** is a browser-based image captioning tool that uses AI to describe what it sees — and reads it aloud using the Web Speech API.

Built with:
- 🧠 `Xenova/vit-gpt2-image-captioning` via [transformers.js](https://github.com/xenova/transformers.js)
- 🎨 Bootstrap 5 for a clean UI
- 🔊 Web Speech API for real-time voice output
- ⚡ No server required — runs entirely in the browser

---

## 🔧 How It Works

1. Upload an image  
2. AI generates a caption directly in the browser  
3. SceneSpeak speaks the caption out loud using your device’s voice engine

---

## 🚀 Live Demo

👉 [Try SceneSpeak](https://scenespeak-ef9b4e95cfe3.herokuapp.com/)

---

## 🔍 Model Notes

SceneSpeak uses [`Xenova/vit-gpt2-image-captioning`](https://huggingface.co/Xenova/vit-gpt2-image-captioning), a lightweight vision-to-text model converted for browser use via ONNX.

> 🧠 This model works best with simple, everyday objects — pets, people, vehicles, food, landscapes.

---

## 🗣️ Voice Feature

Captions are spoken using the **Web Speech API**, which works on:

- ✅ Chrome  
- ✅ Edge  
- ✅ Safari  
- ❌ Not supported in Firefox

---

## 🛡️ License

MIT — free to use, remix, and build on.
