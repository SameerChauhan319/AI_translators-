🌐 AI-Powered Multilingual Translator
A web-based application that enables natural and context-aware text translation between multiple global and Indian languages using advanced LLMs (OpenAI GPT) and fallback translation services. It supports tone and gender-based customization, speech-to-text input, and text-to-speech output.

📌 Features
🔁 Multilingual Translation (English, Hindi, Marathi, Tamil, Telugu, Bengali, Gujarati, Kannada, Malayalam, Punjabi, Urdu, and more)

🧠 LLM-based Contextual Translation using OpenAI GPT (via prompt engineering)

🗣️ Speech-to-Text Input (via Web Speech API)

🔊 Text-to-Speech Output (via gTTS)

🎨 Light/Dark Theme Toggle

💾 Save Translated Output to .txt file

⚙️ Real-Time Auto Translation

🎚️ Tone & Gender Control in prompts

📦 Fallback Translation using MyMemory API

🛠️ Tech Stack
Frontend:
HTML5 + CSS3

JavaScript (Vanilla)

Web Speech API (Speech Recognition)

Backend:
Python 3.x

Flask

gTTS (Google Text-to-Speech)

OpenAI API (LLM Translation)

Deep Translator (MyMemory fallback)

📁 Project Structure
bash
Copy
Edit
AI_Translator/
│
├── web_app/
│   ├── app.py                  # Flask backend
│   ├── llm_translate.py        # OpenAI GPT integration
│   ├── mymemory_translate.py   # Fallback translation
│   ├── templates/
│   │   └── index.html          # Main frontend page
│   ├── static/
│   │   ├── style.css           # Styling
│   │   └── script.js           # Frontend logic
│   └── .env                    # Contains API keys (not committed)
│
├── desktop_app/
│   └── src/
│       └── main.py             # Tkinter GUI version
│
└── requirements.txt            # Python dependencies
⚙️ Installation & Setup
1. Clone the Repository

git clone https://github.com/your-username/AI_Translator.git

cd AI_Translator/web_app

2. Set Up a Virtual Environment

python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies

pip install -r requirements.txt

4. Set OpenAI API Key
Create a .env file in web_app/:

OPENAI_API_KEY=your_openai_api_key_here

5. Run the Flask Server

python app.py

💻 How to Use
Open your browser at: http://127.0.0.1:5000

Choose source and target languages.

Enter text or use 🎤 voice input.

Select tone and gender (optional).

Click Translate or wait for auto-translation.

Use Speak, Save, or Clear options as needed.

🧪 Testing
Translation: Tested across 15+ languages using OpenAI and fallback APIs.

Speech input: Works with modern browsers like Chrome.

TTS: Uses gTTS, supports most Indian languages.

🔐 Security Note
Do not commit .env with your API keys.
Use .gitignore to avoid exposing secrets.


👨‍💻 Author
Sam Chauhan
B.Sc. Computer Science | AI Project Developer
For inquiries: [Your Contact Email or GitHub Profile]