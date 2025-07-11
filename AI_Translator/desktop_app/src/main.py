import tkinter as tk
from tkinter import ttk
from gtts import gTTS
from playsound import playsound
import os
import tempfile
import threading
import speech_recognition as sr
import subprocess
import requests
import time

def is_flask_running():
    try:
        requests.get("http://127.0.0.1:5000/")
        return True
    except:
        return False

if not is_flask_running():
    try:
        subprocess.Popen(["python", "C:/Users/chauh/OneDrive/Desktop/AI_Translator/AI_Translator/web_app/app.py"], shell=True)
        print("Starting Flask server...")
        time.sleep(3)
    except Exception as e:
        print(f"Failed to start Flask server: {e}")

root = tk.Tk()
root.title("AI Translator")
root.geometry("950x600")
root.configure(bg="#121212")

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

tone_options = ["neutral", "formal", "casual", "friendly"]
gender_options = ["neutral", "male", "female"]

FONT_BOX = ("Consolas", 11)
FONT_TEXT = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 10, "bold")
theme_mode = "dark"

class SquircleButton(tk.Canvas):
    def __init__(self, parent, text, command, color, width=100, height=40, corner_radius=20):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0)
        self.command = command
        self.color = color
        self.create_rounded_rect(0, 0, width, height, corner_radius, fill=color)
        self.create_text(width/2, height/2, text=text, font=FONT_TEXT, fill="white")
        self.bind("<Button-1>", self._on_click)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y2-r, x2, y2,
                  x2-r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y1+r, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def _on_click(self, event):
        self.command()

def toggle_theme():
    global theme_mode
    widgets = [root, input_box, output_box, text_frame, btn_frame, status_label]
    if theme_mode == "dark":
        for w in widgets:
            w.configure(bg="white")
        input_box.configure(fg="black", insertbackground="black")
        output_box.configure(fg="black", insertbackground="black")
        status_label.configure(fg="black")
        theme_mode = "light"
    else:
        for w in widgets:
            w.configure(bg="#121212")
        input_box.configure(bg="#1e1e1e", fg="white", insertbackground="white")
        output_box.configure(bg="#1e1e1e", fg="white", insertbackground="white")
        status_label.configure(fg="white")
        theme_mode = "dark"

def clear_text():
    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)
    status_label.config(text="Cleared")

def clear_placeholder(event):
    if input_box.get("1.0", tk.END).strip() == "Enter text here...":
        input_box.delete("1.0", tk.END)

def translate(event=None):
    src_text = input_box.get("1.0", tk.END).strip()
    if not src_text or src_text == "Enter text here...":
        status_label.config(text="Error: Enter text first")
        return
    try:
        status_label.config(text="Translating...")
        payload = {
            "text": src_text,
            "src": source_lang.get(),
            "tgt": target_lang.get(),
            "tone": tone_var.get(),
            "gender": gender_var.get()
        }
        res = requests.post("http://127.0.0.1:5000/translate", json=payload)
        result = res.json().get("translated", "Error: No translation received.")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, result)
        status_label.config(text="Translated")
    except Exception as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Error: {str(e)}")
        status_label.config(text="Translation Failed")

def swap_languages():
    src = source_lang.get()
    tgt = target_lang.get()
    source_lang.set(tgt)
    target_lang.set(src)
    status_label.config(text="Languages swapped")

def record_audio():
    def _record():
        try:
            status_label.config(text="Please speak now...")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)  # Better noise calibration
                audio = r.listen(source, timeout=5, phrase_time_limit=6)  # Limit speech

            lang_code = lang_map.get(source_lang.get(), "en")
            text = r.recognize_google(audio, language=lang_code)

            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, text.strip())  # Trim unwanted spaces
            status_label.config(text="Speech captured")
        except sr.WaitTimeoutError:
            status_label.config(text="No speech detected (timeout)")
        except sr.UnknownValueError:
            status_label.config(text="Could not understand audio")
        except sr.RequestError as e:
            status_label.config(text=f"API error: {str(e)}")
        except Exception as e:
            status_label.config(text=f"Mic error: {str(e)}")

    threading.Thread(target=_record, daemon=True).start()


def speak():
    def _speak():
        try:
            text = output_box.get("1.0", tk.END).strip()
            if not text:
                status_label.config(text="No text to speak")
                return
            lang_code = lang_map.get(target_lang.get(), "en")
            if "zh" in lang_code:
                lang_code = "zh"
            status_label.config(text="Speaking...")
            root.update_idletasks()
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
                temp_path = tf.name.replace("\\", "/")
                tts = gTTS(text=text, lang=lang_code)
                tts.save(temp_path)
            playsound(temp_path.replace("\\", "/"))
            os.remove(temp_path)
            status_label.config(text="Done speaking")
        except Exception as e:
            status_label.config(text=f"TTS Error: {str(e)}")

    threading.Thread(target=_speak, daemon=True).start()

font_size = 11
def toggle_font_size(action):
    global font_size
    if action == "+" and font_size < 20:
        font_size += 1
    elif action == "-" and font_size > 8:
        font_size -= 1
    elif action == "reset":
        font_size = 11
    input_box.configure(font=("Consolas", font_size))
    output_box.configure(font=("Consolas", font_size))
    status_label.config(text=f"Font size: {font_size}")

# GUI Layout
text_frame = tk.Frame(root, bg="#121212")
text_frame.pack(pady=10, fill="both", expand=True)

input_section = tk.Frame(text_frame, bg="#121212")
input_section.grid(row=0, column=0, padx=10, sticky="nsew")
text_frame.grid_columnconfigure(0, weight=1)

input_scroll = tk.Scrollbar(input_section)
input_scroll.pack(side="right", fill="y")

input_box = tk.Text(input_section, height=15, wrap="word", yscrollcommand=input_scroll.set,
                    width=40, bg="#1e1e1e", fg="white", font=FONT_BOX, insertbackground="white")
input_box.insert("1.0", "Enter text here...")
input_box.bind("<FocusIn>", clear_placeholder)
input_box.pack(expand=True, fill="both")
input_scroll.config(command=input_box.yview)

# Options Frame
options_frame = tk.Frame(input_section, bg="#121212")
options_frame.pack(pady=(5, 0))

from_label = tk.Label(options_frame, text="From", font=FONT_LABEL, bg="#121212", fg="white")
from_label.pack(anchor="w")
source_lang = ttk.Combobox(options_frame, values=list(lang_map.keys()), font=FONT_TEXT, width=38)
source_lang.set("English 🇬🇧")
source_lang.pack()

tone_label = tk.Label(options_frame, text="Tone", font=FONT_LABEL, bg="#121212", fg="white")
tone_label.pack(anchor="w", pady=(6, 2))
tone_var = tk.StringVar(value="neutral")
tone_menu = ttk.Combobox(options_frame, values=tone_options, textvariable=tone_var, font=FONT_TEXT, width=38)
tone_menu.pack()

gender_label = tk.Label(options_frame, text="Gender", font=FONT_LABEL, bg="#121212", fg="white")
gender_label.pack(anchor="w", pady=(6, 2))
gender_var = tk.StringVar(value="neutral")
gender_menu = ttk.Combobox(options_frame, values=gender_options, textvariable=gender_var, font=FONT_TEXT, width=38)
gender_menu.pack()

mic_btn = SquircleButton(options_frame, "🎤 Speak Input", record_audio, "#5bc0de", width=120)
mic_btn.pack(pady=10)

middle_section = tk.Frame(text_frame, bg="#121212")
middle_section.grid(row=0, column=1, padx=10, sticky="n")

translate_btn = SquircleButton(middle_section, "Translate", translate, "#2e8b57", width=100, height=50)
translate_btn.pack(pady=(0, 10))

swap_btn = SquircleButton(middle_section, "↔ Swap", swap_languages, "#5bc0de", width=100)
swap_btn.pack()

output_section = tk.Frame(text_frame, bg="#121212")
output_section.grid(row=0, column=2, padx=10, sticky="nsew")
text_frame.grid_columnconfigure(2, weight=1)

output_scroll = tk.Scrollbar(output_section)
output_scroll.pack(side="right", fill="y")

output_box = tk.Text(output_section, height=15, wrap="word", yscrollcommand=output_scroll.set,
                     width=40, bg="#1e1e1e", fg="white", font=FONT_BOX, insertbackground="white")
output_box.pack(expand=True, fill="both")
output_scroll.config(command=output_box.yview)

to_label = tk.Label(output_section, text="To", font=FONT_LABEL, bg="#121212", fg="white")
to_label.pack(pady=(8, 2))

target_lang = ttk.Combobox(output_section, values=list(lang_map.keys()), font=FONT_TEXT, width=38)
target_lang.set("Spanish 🇪🇸")
target_lang.pack()

btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack(pady=10)

buttons = [
    ("Clear", clear_text, "#d9534f"),
    ("Theme", toggle_theme, "#0275d8"),
    ("Zoom+", lambda: toggle_font_size("+"), "#6c757d"),
    ("Reset", lambda: toggle_font_size("reset"), "#6c757d"),
    ("Zoom-", lambda: toggle_font_size("-"), "#6c757d"),
    ("Speak", speak, "#5cb85c")
]

for i, (text, cmd, color) in enumerate(buttons):
    btn = SquircleButton(btn_frame, text, cmd, color, width=80)
    btn.grid(row=0, column=i, padx=5)

status_label = tk.Label(root, text="Ready", anchor="w", font=FONT_TEXT, bg="#121212", fg="white")
status_label.pack(side="bottom", fill="x")

root.bind("<Control-plus>", lambda e: toggle_font_size("+"))
root.bind("<Control-minus>", lambda e: toggle_font_size("-"))
root.bind("<Control-equal>", lambda e: toggle_font_size("+"))
root.bind("<Return>", lambda e: translate())

root.mainloop()
