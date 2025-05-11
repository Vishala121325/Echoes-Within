# 🌿 Echoes Within — A Time-Locked Memory Capsule App

**Echoes Within** is a peaceful, visually enchanting web app that allows you to create and seal your emotions, thoughts, and moments into digital memory capsules — each time-locked until you're ready to open them.

Whether it's a journal entry, a voice message, a heartfelt video, or a nostalgic image, this app provides a cozy, healing space to revisit your emotions when the time feels right.

## ✨ Features

- ⏳ **Time-Locked Capsules**  
  Write thoughts, attach media (images, videos, audio), and lock them with a future date.

- 🎨 **Enchanting Opening Animation**  
  A soothing forest-themed splash screen welcomes users to a serene journaling environment.

- 📦 **Export Capsule as ZIP**  
  Download any unlocked capsule (text + media) as a ZIP file, neatly bundled with:
  - User-given capsule name
  - Attached images, audio, and videos
  - Journal text as a `.txt` file

- 🔓 **Unlock with a Fade and Glow Effect**  
  Capsules fade in beautifully when their time arrives.

- 📁 **Media-Rich Capsules**  
  Support for uploading and saving photos, videos, and audio inside capsules.

- 🌿 **Floating Leaf Visuals**  
  Animated leaf effects add to the meditative vibe of the app.

## 🛠️ Tech Stack

- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Backend**: Python Flask
- **Media Handling**: HTML5 `<input>` for file uploads, Flask static file handling
- **Download Export**: Python `zipfile` module for packaging capsule content

## 📦 How to Run

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/echoes-within.git
   cd echoes-within
