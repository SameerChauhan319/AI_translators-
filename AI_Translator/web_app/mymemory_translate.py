import requests

def mymemory_translate(text, src_lang_code, tgt_lang_code):
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"{src_lang_code}|{tgt_lang_code}"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if "responseData" in data and "translatedText" in data["responseData"]:
            return data["responseData"]["translatedText"]
        else:
            return "Error: Translation failed."

    except Exception as e:
        return f"Error using MyMemory: {str(e)}"