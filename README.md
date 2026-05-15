# Kutuliza — AI-Powered Medical Triage Kiosk

> **"Kutuliza"** is Luganda for *"to help / to relieve."*

---

## Project Description

Kutuliza is a full-stack, AI-powered medical triage kiosk designed for Ugandan health facilities. A patient or community health worker speaks or types a complaint in a local language — Luganda, Runyankole, Ateso, Lugbara, or Acholi — and the system runs it through a four-step AI pipeline: it transcribes the audio (if needed), produces a concise English clinical summary for the attending nurse, translates that summary back into the patient's language, and finally reads the translation aloud so the patient understands their care plan. The entire pipeline is powered exclusively by [Sunbird AI](https://sunbird.ai) — no OpenAI, no Anthropic, no third-party LLMs. The UI is built as a full-screen touchscreen kiosk with colour-coded triage levels (green / yellow / red) that update in real time, and two built-in demo scenarios let reviewers see the system in action without needing an audio file.

---

## Architecture Overview

### System layers

```
┌──────────────────────────────────────────────────────────┐
│                 Browser / Kiosk Touchscreen               │
│       Next.js 14 (App Router) · Tailwind CSS · React      │
└───────────────────────────┬──────────────────────────────┘
                            │  HTTP  (JSON · multipart/form-data)
                            ▼
┌──────────────────────────────────────────────────────────┐
│               FastAPI Backend  (Python 3.11+)             │
│  app.py → backend/pipeline.py → backend/sunbird_client.py │
└───────────────────────────┬──────────────────────────────┘
                            │  HTTPS  (REST)
                            ▼
┌──────────────────────────────────────────────────────────┐
│                     Sunbird AI API                        │
│   POST /tasks/stt   ·  POST /tasks/sunflower_simple       │
│                     ·  POST /tasks/tts                    │
└──────────────────────────────────────────────────────────┘
```

### Pipeline — input to output

| Step | What happens | Sunbird endpoint |
|------|-------------|-----------------|
| **1 — Input** | User types text **or** uploads an audio file (MP3 / WAV / OGG / M4A / AAC, ≤ 5 min) | — |
| **2 — Transcribe** *(audio only)* | Audio is sent to Sunbird STT; a text transcript is returned | `POST /tasks/stt` |
| **3 — Summarise** | Typed text or transcript is sent to Sunflower with a zero-shot summarisation prompt; a concise English clinical summary is returned | `POST /tasks/sunflower_simple` |
| **4 — Translate** | The English summary is sent to Sunflower with a translation prompt; a local-language version is returned | `POST /tasks/sunflower_simple` |
| **5 — Synthesise speech** | The translated summary is converted to a WAV audio clip | `POST /tasks/tts` |
| **6 — Output** | The UI displays the transcript, English summary, translated summary, and an inline audio player | — |

### File structure

```
kutuliza/
├── app.py                          # FastAPI entry point — two routes + CORS
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .gitignore
│
├── backend/
│   ├── sunbird_client.py           # Thin wrapper around every Sunbird endpoint
│   └── pipeline.py                 # Step functions: transcribe / summarise / translate / tts
│
└── frontend/
    ├── package.json
    ├── next.config.js              # API proxy rewrite (/api/* → FastAPI)
    ├── tailwind.config.js
    ├── postcss.config.js
    └── src/
        ├── app/
        │   ├── layout.jsx
        │   ├── page.jsx            # Root kiosk page — assembles all panels
        │   └── globals.css
        ├── components/
        │   ├── TriageHeader.jsx    # Colour-coded status banner + live clock
        │   ├── InputPanel.jsx      # Text / audio input, language pickers
        │   ├── ClinicalPanel.jsx   # Transcript, summary, danger signs, audio player
        │   └── ActionBar.jsx       # Confirm triage · Print · Contact consultant
        ├── hooks/
        │   └── usePipeline.js      # All async pipeline state in one hook
        └── utils/
            ├── api.js              # fetch() wrappers + b64→Blob URL helper
            └── constants.js        # Language codes, triage configs, demo scenarios
```

---

## Local Setup

### Prerequisites

| Tool | Minimum version | Check |
|------|----------------|-------|
| Python | 3.11 | `python --version` |
| pip | 23 | `pip --version` |
| Node.js | 18 (LTS) | `node --version` |
| npm | 9 | `npm --version` |
| Git | any | `git --version` |

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/your-username/kutuliza.git
cd kutuliza
```

---

### Step 2 — Configure environment variables

```bash
# Root directory — backend token
cp .env.example .env
```

Open `.env` in any editor and replace the placeholder with your real Sunbird AI API token:

```dotenv
SUNBIRD_API_TOKEN=your_sunbird_api_token_here
FRONTEND_ORIGIN=http://localhost:3000
```

Then create the frontend environment file:

```bash
# This file is read by Next.js at build time
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
```

> **How to get a Sunbird AI API token:**
> 1. Go to [https://api.sunbird.ai](https://api.sunbird.ai) and sign up for a free account.
> 2. Open your **API Keys** dashboard and click **Generate new key**.
> 3. Copy the token and paste it into `.env` as shown above.
> 4. The free tier covers development and testing. Never commit the token to git — `.env` is already listed in `.gitignore`.

---

### Step 3 — Install and start the backend

```bash
# Create and activate a Python virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows PowerShell

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI development server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Verify it is running:

```
http://localhost:8000/api/health   →  {"status": "ok", "service": "kutuliza-api"}
http://localhost:8000/docs         →  Swagger UI (interactive API explorer)
```

---

### Step 4 — Install and start the frontend

Open a **second terminal** (keep the backend running in the first):

```bash
cd frontend
npm install
npm run dev
```

The kiosk UI is now available at:

```
http://localhost:3000
```

---

### Step 5 — Open the app

Navigate to `http://localhost:3000` in any modern browser. For a true kiosk experience on a 15-inch touchscreen, launch Chromium in app mode:

```bash
chromium-browser --kiosk --app=http://localhost:3000 --noerrdialogs --disable-infobars
```

---

## Environment Variables

### Backend — `.env` (root directory)

| Variable | Required | Description |
|----------|----------|-------------|
| `SUNBIRD_API_TOKEN` | ✅ Yes | Bearer token for all Sunbird AI API calls. Obtain from [api.sunbird.ai](https://api.sunbird.ai). |
| `FRONTEND_ORIGIN` | Optional | Allowed CORS origin for the frontend. Defaults to `http://localhost:3000`. Set to your production URL when deploying. |

### Frontend — `frontend/.env.local`

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | ✅ Yes | Base URL of the FastAPI backend. Must start with `NEXT_PUBLIC_` so Next.js exposes it to the browser. Defaults to `http://localhost:8000`. |

> **Security note:** `SUNBIRD_API_TOKEN` is only ever read server-side by FastAPI. It is never sent to or stored by the frontend.

---

## Usage

### Text input walkthrough

1. Open `http://localhost:3000`. The header shows **Awaiting Assessment** in grey.
2. The left panel defaults to **Text Input** mode. Type or paste any text — clinical notes, a patient complaint, or any paragraph.
3. Select the **target language** you want the summary translated into (e.g. *Luganda*).
4. Click **Run Pipeline →**.
5. The button changes to a spinner labelled *Processing…* while the backend calls Sunflower twice (summarise, then translate) and Sunbird TTS once.
6. Results appear on the right panel in sequence:
   - **Transcript** — empty (text mode bypasses STT)
   - **Nurse's Summary** — concise English clinical summary
   - **Translation** — summary in the chosen local language
   - **Audio player** — click play to hear the translated summary spoken aloud
7. The triage header turns **green** (Routine) once processing completes.
8. Click **✓ Confirm Triage** to log the decision, **🖨 Print Patient ID** to open the browser print dialog, or **↺ Reset** to clear the board.

---

### Audio input walkthrough

1. Click the **🎙 Audio Upload** tab in the left panel.
2. Select the **language spoken in the audio** (STT language picker).
3. Select the **target language** for the translated summary.
4. Click the dashed upload zone and choose an audio file (MP3, WAV, OGG, M4A, or AAC — maximum 5 minutes).
5. Click **Run Pipeline →**. The backend validates the file duration locally, then calls:
   - `POST /tasks/stt` → transcript
   - `POST /tasks/sunflower_simple` → English summary
   - `POST /tasks/sunflower_simple` → local-language translation
   - `POST /tasks/tts` → WAV audio
6. All four outputs appear in the right panel.

---

### Demo scenarios (no audio file needed)

Two built-in test scenarios let reviewers see the full UI in action instantly, with no API token required for the frontend animation:

**⚡ Test: Maternal Emergency**

Click this button in the action bar. The system:
- Simulates a Luganda-language patient report appearing word-by-word in the transcript box
- Shifts the header background to **red** with a pulsing border
- Populates the clinical panel with *"Maternal Emergency: Possible Preeclampsia"*, danger signs (severe headache, blurred vision, facial and peripheral oedema), and a Luganda translation
- Confirms triage level as **Emergency**

**⚡ Test: Paediatric Fever**

Same animation flow, but models a child with high fever, vomiting, and poor appetite — triage level resolves to **Priority** (yellow header).

> These demo scenarios use pre-written mock data and do not make any API calls. They are safe to run without a Sunbird API token.

---

### Screenshots

> **Reviewer note:** Replace the placeholders below with real screenshots once the app is deployed.

| State | Description |
|-------|-------------|
| ![Idle state](docs/screenshots/01-idle.png) | Default idle state — grey header, empty panels |
| ![Text input](docs/screenshots/02-text-input.png) | Text typed, language selected, ready to submit |
| ![Processing](docs/screenshots/03-processing.png) | Spinner active while pipeline runs |
| ![Results](docs/screenshots/04-results.png) | All four outputs displayed; audio player visible |
| ![Emergency demo](docs/screenshots/05-emergency.png) | Red header after Maternal Emergency test scenario |

---

## Deployed Link

> 🌐 **Live demo:** `https://kutuliza.vercel.app`
>
> _(Replace this URL with your actual deployed URL before submission. See the Deployment section below for step-by-step instructions.)_

---

## Deployment

### Backend — Railway (recommended)

Railway auto-detects Python projects and injects environment variables securely.

```bash
# Install the Railway CLI
npm install -g @railway/cli

# Log in and initialise the project
railway login
railway init

# Add your secret — Railway encrypts this at rest
railway variables set SUNBIRD_API_TOKEN=your_token_here
railway variables set FRONTEND_ORIGIN=https://your-frontend.vercel.app

# Deploy
railway up
```

Copy the public Railway URL (e.g. `https://kutuliza-production.up.railway.app`).

Alternatively, deploy to **Render** (free tier):
1. Push the repo to GitHub.
2. Create a new **Web Service** on [render.com](https://render.com).
3. Set **Build command:** `pip install -r requirements.txt`
4. Set **Start command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Add `SUNBIRD_API_TOKEN` under **Environment → Secret Files**.

---

### Frontend — Vercel (recommended)

```bash
cd frontend
npx vercel --prod
```

When prompted, set the environment variable:

```
NEXT_PUBLIC_API_URL = https://your-backend.up.railway.app
```

Or set it in the Vercel dashboard under **Project → Settings → Environment Variables**.

---

### Production gunicorn command (backend)

```bash
gunicorn app:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT:-8000} \
  --timeout 120
```

---

## Known Limitations

| Limitation | Detail |
|-----------|--------|
| **5-minute audio cap** | Audio files longer than 5 minutes are rejected with HTTP 422 before any API call is made. Sunbird's own STT limit is 10 minutes, but the app enforces 5 minutes per the project specification. |
| **English STT only for transcription into English** | The STT step accepts spoken Luganda, Runyankole, Ateso, Lugbara, Acholi, and English. The summarisation step always targets English as an intermediate language, so the chain is: local speech → English summary → local translation. Purely English-to-English pipelines work but are redundant. |
| **No real-time streaming** | The pipeline is a single blocking request; all four steps complete before any result is shown. A future improvement would stream each step result as it becomes available using Server-Sent Events. |
| **TTS for five languages only** | Text-to-Speech is available for Luganda, Runyankole, Ateso, Lugbara, and Acholi. English TTS is not currently offered by Sunbird, so `target_language` must be one of the five local languages. |
| **No persistent patient records** | Kutuliza does not store any patient data between sessions. Each page reload clears all results. Persistence would require a database and careful HIPAA/GDPR-equivalent compliance. |
| **Demo scenarios do not call the API** | The two built-in test scenarios (Maternal Emergency, Paediatric Fever) use hardcoded mock data and do not invoke Sunbird AI. They exist purely to demonstrate the UI state machine. |
| **Single-user, single-session** | The kiosk UI is designed for one patient at a time. There is no queue management, patient ID generation, or multi-session support. |
| **Audio format detection is MIME-based** | If a browser sends an incorrect MIME type for an audio file, the format check in `app.py` may pass or fail incorrectly. A more robust solution would use `python-magic` for byte-level detection. |
| **No HTTPS in local development** | The local FastAPI server runs on plain HTTP. Production deployments must sit behind a TLS-terminating reverse proxy or use a platform (Railway/Render/Heroku) that handles HTTPS automatically. |

---

## Sunbird AI API Reference

| Capability | Endpoint | Docs |
|-----------|----------|------|
| Speech-to-Text | `POST https://api.sunbird.ai/tasks/stt` | [docs.sunbird.ai/guides/speech-to-text](https://docs.sunbird.ai/guides/speech-to-text) |
| Summarise & Translate | `POST https://api.sunbird.ai/tasks/sunflower_simple` | [docs.sunbird.ai/guides/sunflower-chat](https://docs.sunbird.ai/guides/sunflower-chat) |
| Text-to-Speech | `POST https://api.sunbird.ai/tasks/tts` | [docs.sunbird.ai/guides/text-to-speech](https://docs.sunbird.ai/guides/text-to-speech) |
| Full reference | — | [docs.sunbird.ai/api-reference/introduction](https://docs.sunbird.ai/api-reference/introduction) |

---

## License

MIT © 2024 Kutuliza Contributors.
Sunbird AI is a product of [Sunbird AI Uganda](https://sunbird.ai) and is used here under their API terms of service.