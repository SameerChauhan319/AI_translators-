window.onload = () => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "light") {
    document.body.classList.add("light-theme");
  }
};

const langMap =  {
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


const speechLangMap = {
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

function translateText() {
  const translateBtn = document.getElementById("translateBtn");
  const spinner = document.getElementById("spinner");

  const text = document.getElementById("inputText").value;
  const src = document.getElementById("sourceLang").value;
  const tgt = document.getElementById("targetLang").value;
  const tone = document.getElementById("tone").value;
  const gender = document.getElementById("gender").value;

  spinner.style.display = "inline";
  translateBtn.disabled = true;
  translateBtn.innerText = "Translating...";

  fetch("/translate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, src, tgt, tone, gender })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("outputText").value = data.translated;
    })
    .catch(err => {
      document.getElementById("outputText").value = "Translation failed: " + err.message;
    })
    .finally(() => {
      spinner.style.display = "none";
      translateBtn.disabled = false;
      translateBtn.innerText = "Translate";
    });
}

function speakOutput() {
  const text = document.getElementById("outputText").value;
  const selectedLang = document.getElementById("targetLang").value;
  const lang = langMap[selectedLang] || "en";  // ✅ Fix: Use lang code

  if (!text.trim()) {
    alert("No text to speak.");
    return;
  }

  fetch("/speak", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, lang })
  })
    .then(res => res.blob())
    .then(blob => {
      const audio = new Audio(URL.createObjectURL(blob));
      audio.play();
    })
    .catch(err => alert("TTS failed: " + err.message));
}

function speakInput() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  const selectedLang = document.getElementById("sourceLang").value;
  recognition.lang = speechLangMap[selectedLang] || "en-US";

  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.start();

  recognition.onresult = function (event) {
    const spokenText = event.results[0][0].transcript;
    document.getElementById("inputText").value = spokenText;
    translateText();
  };

  recognition.onerror = function (event) {
    alert("Speech recognition error: " + event.error);
  };
}

function saveText() {
  const text = document.getElementById("outputText").value;
  if (!text.trim()) {
    alert("Nothing to save!");
    return;
  }

  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "translation.txt";
  link.click();
}

function clearText() {
  document.getElementById("inputText").value = "";
  document.getElementById("outputText").value = "";
}

function toggleTheme() {
  const body = document.body;
  body.classList.toggle("light-theme");

  const isLight = body.classList.contains("light-theme");
  localStorage.setItem("theme", isLight ? "light" : "dark");
}

document.addEventListener("DOMContentLoaded", () => {
  let debounceTimer;
  const inputBox = document.getElementById("inputText");

  inputBox.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const text = inputBox.value.trim();
      if (text) translateText();
    }, 500); 
  });
});