"""
pipeline.py - Main processing pipeline for Kutuliza
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# FIXED: Direct imports (no 'backend.' prefix)
from backend.sunbird_client import SunbirdClient

load_dotenv()

# Initialize client
client = SunbirdClient()

# Constants
LANGUAGE_NAMES = {
    "lug": "Luganda",
    "nyn": "Runyankole",
    "ach": "Acholi",
    "teo": "Ateso",
    "lgg": "Lugbara",
}

MAX_AUDIO_SECONDS = 300  # 5 minutes


def step_transcribe(audio_path: Path, language: str = "lug"):
    """Speech to Text"""
    return client.transcribe(audio_path, language)


def step_summarise(text: str):
    """Clinical summary + triage using Sunflower LLM"""
    prompt = f"""You are a senior Ugandan triage nurse specializing in maternal and child health.
Patient said: "{text}"

Return in this format:
SUMMARY: [Clear English clinical summary]
DANGER SIGNS: [Any red flag symptoms]
TRIAGE: [Green / Yellow / Red]"""

    response = client.summarise(prompt)
    return response


def step_translate(text: str, target_language: str):
    """Translate summary to local language"""
    prompt = f"Translate the following clinical summary into natural spoken {target_language} (use simple, everyday language):\n\n{text}"
    return client.translate(prompt, target_language)


def step_tts(text: str, language: str):
    """Text to Speech"""
    return client.text_to_speech(text, language)