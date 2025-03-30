# 🌍 Medical Translator App 🏥

## 📝 Overview
The **Medical Translator App** is a Flask-based web application that enables real-time medical translation across multiple languages. Users can 🎤 record audio, 📝 transcribe it into text, 🌎 translate the transcription into a selected language, and 🔊 play back the translated text as speech. This solution bridges language barriers in healthcare settings, making it easier for medical professionals to communicate with patients who speak different languages.

## 🚀 Features
- 🎙 **Record audio** directly from the browser
- 📝 **Transcribe speech** using **OpenAI Whisper**
- 🌎 **Translate** transcribed text into multiple languages using **Google Translator**
- 🔊 **Convert text to speech** using **gTTS**
- 💻 **Modern, responsive web interface** with intuitive controls
- 🌐 **Support for 10+ languages** including Spanish, French, German, Chinese, Japanese, Korean, Arabic, Hindi, Portuguese, and Russian
- 📋 **Copy to clipboard** functionality for both original and translated text
- 🔄 **Real-time status updates** during processing

## 🛠 Technologies Used
- 🏗 **Flask** (Web Framework)
- 🗣 **OpenAI Whisper** (Speech-to-Text)
- 🌍 **Google Translator API** (Text Translation)
- 🎵 **gTTS** (Text-to-Speech)
- 🎨 **JavaScript** (Frontend Functionality)
- 🖌 **HTML & CSS** (UI Design)
- 🎧 **Web Audio API** (Audio Recording)
- ☁️ **Azure App Service** (Deployment)

## 📥 Installation & Setup
### 📌 Prerequisites
- Python 3.12 or later
- pip (Python package manager)
- FFmpeg (required for audio processing)
- Git (optional, for cloning the repository)

### 📌 Steps to Run Locally
```bash
# 🛠 Clone the repository (or download and extract the ZIP file)
git clone https://github.com/rafednaeem/Medical-translator-App.git
cd medical-translator

# 🏗 Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate

# 📦 Install dependencies
pip install -r requirements.txt

# 🚀 Run the Flask app
python app.py
```

### 🌐 Access the App
Once the application is running, open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

## 📋 Usage Instructions
1. 🔤 Select the **source language** (or leave as auto-detect)
2. 🔤 Choose the **target language** for translation
3. 🎙 Click **Start Recording** and speak clearly
4. ⏹ Click **Stop** when finished speaking
5. ⏳ Wait for processing (transcription and translation)
6. 🔊 Click **Speak** to hear the translated text
7. 📋 Use the copy buttons to copy text to your clipboard

## 🔧 Troubleshooting
- Ensure your microphone is connected and working properly
- Allow microphone access when prompted by your browser
- If translation fails, try again with shorter phrases
- Check console logs for detailed error messages
