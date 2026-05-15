import pathlib

content = '''import os, base64, tempfile, mimetypes
from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from backend.pipeline import step_transcribe, step_summarise, step_translate, step_tts, LANGUAGE_NAMES, MAX_AUDIO_SECONDS

app = FastAPI(title="Kutuliza")

pathlib.Path("static").mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SUPPORTED_AUDIO_MIMES = {"audio/mpeg","audio/mp3","audio/wav","audio/wave","audio/ogg","audio/m4a","audio/aac","audio/x-m4a"}
SUPPORTED_LANGUAGES = set(LANGUAGE_NAMES.keys())

def _audio_duration(path):
    try:
        import mutagen
        audio = mutagen.File(str(path))
        if audio and audio.info:
            return audio.info.length
    except Exception:
        pass
    return None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "kutuliza-api"}

class TextRequest(BaseModel):
    text: str
    target_language: str = "lug"

@app.post("/api/process/text")
async def process_text(body: TextRequest):
    if not body.text.strip():
        raise HTTPException(422, "Text input cannot be empty.")
    if body.target_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(422, f"Unsupported language.")
    try:
        summary     = step_summarise(body.text)
        translation = step_translate(summary, body.target_language)
        audio_bytes = step_tts(translation, body.target_language)
    except Exception as e:
        raise HTTPException(502, f"Sunbird API error: {e}")
    return JSONResponse({
        "transcript": None,
        "source_text": body.text,
        "summary": summary,
        "translation": translation,
        "audio_b64": base64.b64encode(audio_bytes).decode(),
        "target_language": body.target_language,
        "target_language_name": LANGUAGE_NAMES[body.target_language],
    })

@app.post("/api/process/audio")
async def process_audio(
    audio: UploadFile = File(...),
    stt_language: str = Form("lug"),
    target_language: str = Form("lug"),
):
    if target_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(422, "Unsupported target language.")
    suffix = Path(audio.filename or "audio.mp3").suffix or ".mp3"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await audio.read())
        tmp_path = Path(tmp.name)
    try:
        duration = _audio_duration(tmp_path)
        if duration and duration > MAX_AUDIO_SECONDS:
            raise HTTPException(422, f"Audio is {duration/60:.1f} min. Max is 5 minutes.")
        transcript  = step_transcribe(tmp_path, stt_language)
        summary     = step_summarise(transcript)
        translation = step_translate(summary, target_language)
        audio_bytes = step_tts(translation, target_language)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(502, f"Sunbird API error: {e}")
    finally:
        tmp_path.unlink(missing_ok=True)
    return JSONResponse({
        "transcript": transcript,
        "source_text": transcript,
        "summary": summary,
        "translation": translation,
        "audio_b64": base64.b64encode(audio_bytes).decode(),
        "target_language": target_language,
        "target_language_name": LANGUAGE_NAMES[target_language],
    })
'''

pathlib.Path("app.py").write_text(content, encoding="utf-8")
print("app.py written!")