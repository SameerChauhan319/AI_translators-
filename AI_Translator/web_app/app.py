from flask import Flask, request, jsonify, send_file, render_template
from gtts import gTTS
import tempfile
import os
from llm_translate import llm_translate
from mymemory_translate import mymemory_translate

app = Flask(__name__, template_folder="templates", static_folder="static")

lang_map = {
    "English 🇬🇧": "en",
    "Hindi 🇮🇳": "hi",
    "Marathi 🇮🇳": "mr",
    "Tamil 🇮🇳": "ta",
    "Telugu 🇮🇳": "te",
    "Bengali 🇮🇳": "bn",
    "Gujarati 🇮🇳": "gu",
    "Kannada 🇮🇳": "kn",
    "Malayalam 🇮🇳": "ml",
    "Punjabi 🇮🇳": "pa",
    "Urdu 🇮🇳": "ur",
    "Spanish 🇪🇸": "Spanish",
    "French 🇫🇷": "French",
    "German 🇩🇪": "German",
    "Italian 🇮🇹": "Italian",
    "Chinese 🇨🇳": "Simplified Chinese",
    "Japanese 🇯🇵": "Japanese"
}

code_map = {
    "English 🇬🇧": "en",
    "Hindi 🇮🇳": "hi",
    "Marathi 🇮🇳": "mr-IN",
    "Tamil 🇮🇳": "ta-IN",
    "Telugu 🇮🇳": "te-IN",
    "Bengali 🇮🇳": "bn-IN",
    "Gujarati 🇮🇳": "gu-IN",
    "Kannada 🇮🇳": "kn-IN",
    "Malayalam 🇮🇳": "ml-IN",
    "Punjabi 🇮🇳": "pa-IN",
    "Urdu 🇮🇳": "ur-IN",
    "Spanish 🇪🇸": "es",
    "French 🇫🇷": "fr",
    "German 🇩🇪": "de",
    "Italian 🇮🇹": "it",
    "Chinese 🇨🇳": "zh",
    "Japanese 🇯🇵": "ja"
}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.json
        text = str(data.get("text", "")).strip()
        src = lang_map.get(data.get("src"), "English")
        tgt = lang_map.get(data.get("tgt"), "English")

        if not text:
            return jsonify({"translated": "Error: No input text provided."})

        # Clean and simple LLM prompt (no tone/gender)
        prompt = (
            f"Translate the following text from {src} to {tgt}. "
            f"Output should be fully in {tgt} only. "
            f"Do not include any words from {src}.\n\n"
            f"Text:\n{text}"
        )

        try:
            result = llm_translate(prompt)
        except Exception as e:
            # Fallback to MyMemory
            src_code = code_map.get(data.get("src"), "en")
            tgt_code = code_map.get(data.get("tgt"), "en")
            result = mymemory_translate(text, src_code, tgt_code)

        return jsonify({"translated": result})

    except Exception as e:
        return jsonify({"translated": f"Error: {str(e)}"})


@app.route("/speak", methods=["POST"])
def speak():
    try:
        data = request.json
        text = data.get("text", "").strip()
        lang = data.get("lang", "en")

        if not text:
            return "TTS failed: No text to speak.", 400

        if "zh" in lang:
            lang = "zh"

        tts = gTTS(text=text, lang=lang)
        path = os.path.join(tempfile.gettempdir(), "tts_output.mp3")
        tts.save(path)

        return send_file(path, mimetype="audio/mpeg")

    except Exception as e:
        return f"TTS failed: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)