import os
import requests
from pathlib import Path
from typing import Dict, Any

class SunbirdClient:
    def __init__(self):
        self.token = os.getenv("SUNBIRD_API_TOKEN")
        if not self.token:
            raise ValueError("SUNBIRD_API_TOKEN not found in environment variables")
        self.base_url = "https://api.sunbird.ai"

    def _call(self, endpoint: str, json_data=None, files=None):
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}{endpoint}"

        if files:
            resp = requests.post(url, headers=headers, files=files)
        else:
            resp = requests.post(url, json=json_data, headers=headers)

        if resp.status_code != 200:
            raise Exception(f"Sunbird API error {resp.status_code}: {resp.text}")
        return resp.json()

    def transcribe(self, audio_path: Path, language: str = "lug"):
        with open(audio_path, "rb") as f:
            files = {"audio": (audio_path.name, f, "audio/mpeg")}
            result = self._call("/tasks/stt", files=files)
        return result.get("output", {}).get("text", "")

    def summarise(self, instruction: str):
        result = self._call("/tasks/sunflower_simple", {"instruction": instruction})
        return result.get("output", {}).get("content", "")

    def translate(self, instruction: str, target_lang: str):
        result = self._call("/tasks/sunflower_simple", {"instruction": instruction})
        return result.get("output", {}).get("content", "")

    def text_to_speech(self, text: str, language: str):
        speaker_map = {"lug": 248, "nyn": 243, "ach": 241, "teo": 242, "lgg": 245}
        speaker_id = speaker_map.get(language, 248)
        
        result = self._call("/tasks/tts", {"text": text[:500], "speaker_id": speaker_id})
        # Return audio bytes
        audio_url = result.get("output", {}).get("audio_url")
        if audio_url:
            resp = requests.get(audio_url)
            return resp.content
        return b""