"""
create_html.py
Run this from your kutuliza root folder:
    python create_html.py
"""
import pathlib

# Create templates folder
pathlib.Path("templates").mkdir(exist_ok=True)
pathlib.Path("static").mkdir(exist_ok=True)
print("Folders ready...")

# ── Write index.html ──────────────────────────────────────────────────────────
html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Kutuliza - AI Medical Triage</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',sans-serif;background:#e2e8f0;height:100vh;display:flex;flex-direction:column;overflow:hidden}
#header{display:flex;align-items:center;justify-content:space-between;padding:14px 28px;border-bottom:4px solid #94a3b8;background:#f1f5f9;transition:all 0.5s;flex-shrink:0}
#header.green{background:#dcfce7;border-color:#16a34a}
#header.yellow{background:#fef9c3;border-color:#ca8a04}
#header.red{background:#fee2e2;border-color:#dc2626;animation:pb 1.2s infinite}
@keyframes pb{0%,100%{border-color:#dc2626}50%{border-color:#fca5a5}}
.logo{display:flex;align-items:center;gap:14px}
.logo-icon{width:44px;height:44px;border-radius:10px;background:#64748b;display:flex;align-items:center;justify-content:center;font-size:22px;color:white;transition:background 0.5s}
#header.green .logo-icon{background:#16a34a}
#header.yellow .logo-icon{background:#ca8a04}
#header.red .logo-icon{background:#dc2626}
.logo h1{font-size:22px;font-weight:800;color:#0f172a}
.logo p{font-size:11px;color:#64748b;letter-spacing:1px;text-transform:uppercase}
.tbadge{display:flex;flex-direction:column;align-items:center;gap:4px}
.tbadge>span{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:1px}
.pill{display:flex;align-items:center;gap:8px;background:white;border:2px solid #94a3b8;border-radius:8px;padding:8px 20px;font-weight:800;font-size:16px;transition:border-color 0.5s}
#header.green .pill{border-color:#16a34a}
#header.yellow .pill{border-color:#ca8a04}
#header.red .pill{border-color:#dc2626}
.dot{width:12px;height:12px;border-radius:50%;background:#94a3b8;transition:background 0.5s}
#header.green .dot{background:#16a34a}
#header.yellow .dot{background:#ca8a04}
#header.red .dot{background:#dc2626;animation:pd 1s infinite}
@keyframes pd{0%,100%{opacity:1}50%{opacity:0.3}}
.clk{text-align:right}
.clk .time{font-size:20px;font-weight:700;font-family:monospace;color:#0f172a}
.clk .st{font-size:12px;color:#64748b;margin-top:2px}
#main{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:16px;min-height:0}
.panel{background:white;border-radius:16px;border:1px solid #e2e8f0;padding:20px;display:flex;flex-direction:column;gap:14px;overflow-y:auto}
.ptitle{font-size:11px;font-weight:700;color:#94a3b8;letter-spacing:1.5px;text-transform:uppercase}
.mtoggle{display:flex;border-radius:10px;overflow:hidden;border:1px solid #e2e8f0;background:#f1f5f9}
.mbtn{flex:1;padding:10px 0;border:none;background:transparent;font-weight:600;font-size:14px;cursor:pointer;color:#64748b}
.mbtn.active{background:white;color:#0f172a;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.fl{font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:1px;display:block;margin-bottom:5px}
select,textarea{width:100%;padding:10px 12px;border-radius:8px;border:1px solid #e2e8f0;font-size:14px;font-family:inherit;color:#0f172a;background:white;outline:none}
textarea{resize:none;font-family:'Courier New',monospace;line-height:1.6;min-height:140px;flex:1}
#azone{flex:1;min-height:120px;border:2px dashed #cbd5e1;border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;background:#f8fafc;gap:8px;transition:all 0.2s}
#azone:hover,#azone.drag{border-color:#3b82f6;background:#eff6ff}
#azone.has{border-color:#3b82f6;background:#eff6ff}
#azone .zi{font-size:32px}
#azone .zt{font-size:13px;font-weight:600;color:#64748b}
#azone.has .zt{color:#2563eb}
#azone .zh{font-size:11px;color:#94a3b8}
#fi{display:none}
.btn{padding:14px 20px;border-radius:12px;border:none;font-weight:700;font-size:15px;cursor:pointer;font-family:inherit;transition:all 0.2s}
.bp{background:#2563eb;color:white;width:100%}
.bp:hover:not(:disabled){background:#1d4ed8}
.bp:disabled{background:#e2e8f0;color:#94a3b8;cursor:not-allowed}
.bo{background:white;color:#475569;border:2px solid #e2e8f0;font-size:14px;padding:12px 18px}
.bo:hover:not(:disabled){background:#f8fafc}
.ba{padding:14px 22px;border-radius:12px;border:none;font-weight:700;font-size:15px;cursor:pointer;font-family:inherit;background:#475569;color:white;transition:all 0.2s}
.ba:hover:not(:disabled){background:#334155}
.ba:disabled{background:#e2e8f0;color:#94a3b8;cursor:not-allowed}
.ebox{background:#fee2e2;border:1px solid #fca5a5;border-radius:10px;padding:12px}
.ebox strong{color:#dc2626;font-size:13px;display:block;margin-bottom:4px}
.ebox span{color:#b91c1c;font-size:13px}
.sec{background:#f8fafc;border-radius:10px;border:1px solid #e2e8f0;padding:14px;margin-bottom:4px}
.sh{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.st2{font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:1px}
.sb{font-size:13px;color:#334155;line-height:1.7}
.sb.mono{font-family:'Courier New',monospace;white-space:pre-wrap}
.sb.empty{color:#cbd5e1;font-style:italic}
.lbdg{font-size:11px;font-weight:700;color:#dc2626;animation:pd 1s infinite}
.dh{font-size:11px;font-weight:700;color:#dc2626;margin:10px 0 6px;text-transform:uppercase}
.ds{display:flex;align-items:center;gap:8px;background:#fee2e2;border:1px solid #fca5a5;border-radius:8px;padding:6px 10px;margin-bottom:4px}
.dd{width:8px;height:8px;border-radius:50%;background:#dc2626;flex-shrink:0}
.ds span{font-size:13px;color:#b91c1c}
.ap{background:#0f172a;border-radius:12px;padding:12px 16px}
.al{font-size:11px;color:#64748b;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px}
audio{width:100%;height:36px}
#abar{background:white;border-top:2px solid #e2e8f0;padding:12px 20px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;flex-shrink:0}
.dl{font-size:11px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:1px;margin-right:4px}
.spc{margin-left:auto;display:flex;gap:10px}
.spin{display:inline-block;width:16px;height:16px;border:2px solid rgba(255,255,255,.3);border-top-color:white;border-radius:50%;animation:spin .7s linear infinite;margin-right:8px;vertical-align:middle}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>

<div id="header">
  <div class="logo">
    <div class="logo-icon">&#10010;</div>
    <div><h1>Kutuliza</h1><p>AI Medical Triage &middot; Uganda</p></div>
  </div>
  <div class="tbadge">
    <span>Triage Level</span>
    <div class="pill"><div class="dot"></div><span id="tlabel">Awaiting Assessment</span></div>
  </div>
  <div class="clk">
    <div class="time" id="clock">--:--:--</div>
    <div class="st" id="stxt">Ready</div>
  </div>
</div>

<div id="main">
  <div class="panel">
    <div class="ptitle">Patient Input</div>
    <div class="mtoggle">
      <button class="mbtn active" id="btm" onclick="setMode('text')">&#9997; Text Input</button>
      <button class="mbtn" id="bam" onclick="setMode('audio')">&#127908; Audio Upload</button>
    </div>
    <div>
      <label class="fl">Translate summary into</label>
      <select id="tl">
        <option value="lug">Luganda</option>
        <option value="nyn">Runyankole</option>
        <option value="teo">Ateso</option>
        <option value="lgg">Lugbara</option>
        <option value="ach">Acholi</option>
      </select>
    </div>
    <div id="tsec" style="display:flex;flex-direction:column;gap:14px;flex:1">
      <textarea id="ti" placeholder="Type or paste patient complaint here..."></textarea>
    </div>
    <div id="asec" style="display:none;flex-direction:column;gap:14px;flex:1">
      <div>
        <label class="fl">Audio spoken in</label>
        <select id="sl">
          <option value="eng">English</option>
          <option value="lug">Luganda</option>
          <option value="nyn">Runyankole</option>
          <option value="teo">Ateso</option>
          <option value="lgg">Lugbara</option>
          <option value="ach">Acholi</option>
        </select>
      </div>
      <div id="azone"
           onclick="document.getElementById('fi').click()"
           ondragover="event.preventDefault();this.classList.add('drag')"
           ondragleave="this.classList.remove('drag')"
           ondrop="doDrop(event)">
        <div class="zi">&#127908;</div>
        <div class="zt" id="zt">Click to upload audio file</div>
        <div class="zh">MP3 &middot; WAV &middot; OGG &middot; M4A &middot; AAC &mdash; max 5 minutes</div>
        <input type="file" id="fi" accept="audio/*" onchange="doFile(this)">
      </div>
    </div>
    <button class="btn bp" id="rb" onclick="runPipeline()" disabled>Run Pipeline &rarr;</button>
    <div class="ebox" id="eb" style="display:none">
      <strong>&#9888; Error</strong>
      <span id="em"></span>
    </div>
  </div>

  <div class="panel">
    <div class="ptitle">Clinical Analysis</div>
    <div class="sec">
      <div class="sh">
        <span class="st2">Live Transcript</span>
        <span class="lbdg" id="lbdg" style="display:none">&#9679; LISTENING</span>
      </div>
      <div class="sb mono empty" id="trb">Transcript will appear here...</div>
    </div>
    <div class="sec">
      <div class="sh"><span class="st2" id="smtitle">Nurse's Summary</span></div>
      <div class="sb empty" id="smb">Clinical summary will appear here...</div>
      <div id="db" style="display:none"></div>
    </div>
    <div class="sec">
      <div class="sh"><span class="st2" id="trtitle">Translation</span></div>
      <div class="sb empty" id="trn">Translated summary will appear here...</div>
    </div>
    <div class="ap" id="apbox" style="display:none">
      <div class="al" id="albl">&#128266; Synthesised Speech</div>
      <audio id="apl" controls></audio>
    </div>
  </div>
</div>

<div id="abar">
  <span class="dl">Demo</span>
  <button class="btn bo" onclick="runScenario('preeclampsia')">&#9889; Test: Maternal Emergency</button>
  <button class="btn bo" onclick="runScenario('malaria')">&#9889; Test: Paediatric Fever</button>
  <button class="btn bo" id="rstbtn" onclick="resetAll()" style="display:none">&#8635; Reset</button>
  <div class="spc">
    <button class="btn ba" id="cfmbtn" onclick="confirmTriage()" disabled>&#10003; Confirm Triage</button>
    <button class="btn ba" id="prtbtn" onclick="window.print()" disabled>&#128424; Print Patient ID</button>
    <button class="btn ba" id="cslbtn" onclick="contactConsultant()" disabled>&#128222; Contact Consultant</button>
  </div>
</div>

<script>
var mode='text', selFile=null, aurl=null;

var SC = {
  preeclampsia: {
    lv:'red', lb:'Emergency',
    lines:[
      'Nnyabo, omwana wange afumba nnyo...',
      'Alina obukambwe obungi mu maaso...',
      'Ebyenyi ebinafu bingi mu bigere n\u2019emikono...',
      'N\u2019okulaba kubi nnyo, n\u2019omutwe ogukoma.'
    ],
    tr:'Nnyabo, omwana wange afumba nnyo, alina obukambwe mu maaso, ebyenyi ebinafu mu bigere n\u2019emikono, n\u2019okulaba kubi, n\u2019omutwe ogukoma.',
    sm:'Patient reports severe headache, blurred vision, and significant oedema in the face, hands, and feet. Symptoms are consistent with a hypertensive emergency in pregnancy.',
    tt:'Maternal Emergency: Possible Preeclampsia',
    dg:['Severe headache','Blurred / disturbed vision','Facial and peripheral oedema','Possible hypertension'],
    tn:'Omulwadde alaga omutwe ogukoma nnyo, okulaba kubi, n\u2019ebyenyi ebinafu mu maaso, emikono n\u2019ebigere.',
    ln:'Luganda'
  },
  malaria: {
    lv:'yellow', lb:'Priority',
    lines:[
      'Omwana wange afite omusujja mungi...',
      'Yaayogera enjura nyinshi...',
      'N\u2019okurya akayirwa.'
    ],
    tr:'Omwana wange afite omusujja mungi, yaayogera enjura nyinshi, n\u2019okurya akayirwa.',
    sm:'Child presents with high fever, multiple vomiting episodes, and loss of appetite. Symptoms suggest possible malaria or acute infection.',
    tt:'Paediatric Priority: Possible Malaria',
    dg:['High fever (>38.5\u00b0C suspected)','Repeated vomiting','Poor feeding / appetite loss'],
    tn:'Omwana afite omusujja mungi, yayogera enjura nyinshi kandi taribwa kirungi.',
    ln:'Runyankole'
  }
};

function tick() {
  document.getElementById('clock').textContent =
    new Date().toLocaleTimeString('en-UG',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
}
setInterval(tick, 1000); tick();

function setMode(m) {
  mode = m;
  document.getElementById('btm').classList.toggle('active', m==='text');
  document.getElementById('bam').classList.toggle('active', m==='audio');
  document.getElementById('tsec').style.display = m==='text' ? 'flex' : 'none';
  document.getElementById('asec').style.display = m==='audio' ? 'flex' : 'none';
  updBtn();
}

function doFile(i) {
  selFile = i.files[0];
  if (!selFile) return;
  document.getElementById('azone').classList.add('has');
  document.getElementById('zt').textContent = selFile.name;
  updBtn();
}

function doDrop(e) {
  e.preventDefault();
  document.getElementById('azone').classList.remove('drag');
  selFile = e.dataTransfer.files[0];
  if (!selFile) return;
  document.getElementById('azone').classList.add('has');
  document.getElementById('zt').textContent = selFile.name;
  updBtn();
}

function updBtn() {
  var has = mode==='text'
    ? document.getElementById('ti').value.trim().length > 0
    : selFile !== null;
  document.getElementById('rb').disabled = !has;
}
document.getElementById('ti').addEventListener('input', updBtn);

function setTriage(lv, lb) {
  document.getElementById('header').className = lv;
  document.getElementById('tlabel').textContent = lb;
  var c = document.getElementById('cfmbtn');
  c.style.background = lv==='green' ? '#16a34a' : lv==='yellow' ? '#ca8a04' : lv==='red' ? '#dc2626' : '#64748b';
}

function setSt(t) { document.getElementById('stxt').textContent = t; }

function showTr(t) {
  var e = document.getElementById('trb');
  e.classList.remove('empty');
  e.textContent = t;
}

function showSm(t, tt, dg) {
  document.getElementById('smtitle').textContent = tt || "Nurse's Summary";
  var e = document.getElementById('smb');
  e.classList.remove('empty');
  e.textContent = t;
  var db = document.getElementById('db');
  if (dg && dg.length) {
    db.style.display = 'block';
    db.innerHTML = '<div class="dh">&#9888; Danger Signs Detected</div>' +
      dg.map(function(s){ return '<div class="ds"><div class="dd"></div><span>'+s+'</span></div>'; }).join('');
  } else {
    db.style.display = 'none';
  }
}

function showTn(t, ln) {
  document.getElementById('trtitle').textContent = ln ? 'Translation \u2014 ' + ln : 'Translation';
  var e = document.getElementById('trn');
  e.classList.remove('empty');
  e.textContent = t;
}

function showAu(b64, ln) {
  if (aurl) URL.revokeObjectURL(aurl);
  var bytes = new Uint8Array(atob(b64).split('').map(function(c){ return c.charCodeAt(0); }));
  var blob = new Blob([bytes], {type:'audio/wav'});
  aurl = URL.createObjectURL(blob);
  document.getElementById('apl').src = aurl;
  document.getElementById('albl').textContent = '\ud83d\udd0a Synthesised Speech \u2014 ' + (ln || '');
  document.getElementById('apbox').style.display = 'block';
}

function showErr(m) {
  document.getElementById('em').textContent = m;
  document.getElementById('eb').style.display = 'block';
}
function hideErr() { document.getElementById('eb').style.display = 'none'; }

function setDone(d) {
  ['cfmbtn','prtbtn','cslbtn'].forEach(function(id){ document.getElementById(id).disabled = !d; });
  document.getElementById('rstbtn').style.display = d ? 'inline-flex' : 'none';
}

function setBusy(b, lb) {
  var btn = document.getElementById('rb');
  btn.disabled = b;
  btn.innerHTML = b ? '<span class="spin"></span>' + (lb||'') : 'Run Pipeline &rarr;';
}

function resetAll() {
  setTriage('', 'Awaiting Assessment');
  setSt('Ready');
  setDone(false);
  hideErr();
  ['trb','smb','trn'].forEach(function(id){
    var e = document.getElementById(id);
    e.classList.add('empty');
  });
  document.getElementById('trb').textContent = 'Transcript will appear here...';
  document.getElementById('smb').textContent = 'Clinical summary will appear here...';
  document.getElementById('trn').textContent = 'Translated summary will appear here...';
  document.getElementById('smtitle').textContent = "Nurse's Summary";
  document.getElementById('trtitle').textContent = 'Translation';
  document.getElementById('db').style.display = 'none';
  document.getElementById('apbox').style.display = 'none';
  document.getElementById('lbdg').style.display = 'none';
  setBusy(false); updBtn();
}

async function runPipeline() {
  hideErr(); setBusy(true,'Processing...'); setSt('\u25cf Processing...'); setDone(false);
  var tl = document.getElementById('tl').value;
  try {
    var data;
    if (mode === 'text') {
      var text = document.getElementById('ti').value.trim();
      var res = await fetch('/api/process/text', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({text:text, target_language:tl})
      });
      if (!res.ok) { var err = await res.json().catch(function(){return{detail:res.statusText};}); throw new Error(err.detail||'Request failed.'); }
      data = await res.json();
    } else {
      var form = new FormData();
      form.append('audio', selFile);
      form.append('stt_language', document.getElementById('sl').value);
      form.append('target_language', tl);
      var res2 = await fetch('/api/process/audio', {method:'POST', body:form});
      if (!res2.ok) { var e2 = await res2.json().catch(function(){return{detail:res2.statusText};}); throw new Error(e2.detail||'Request failed.'); }
      data = await res2.json();
    }
    if (data.transcript) showTr(data.transcript);
    showSm(data.summary, 'Clinical Summary', []);
    showTn(data.translation, data.target_language_name);
    showAu(data.audio_b64, data.target_language_name);
    setTriage('green','Routine'); setSt('Assessment Complete'); setDone(true);
  } catch(err) {
    showErr(err.message); setSt('\u26a0 Error');
  } finally {
    setBusy(false); updBtn();
  }
}

async function runScenario(id) {
  var s = SC[id]; if (!s) return;
  resetAll(); setSt('\u25cf Listening...');
  document.getElementById('lbdg').style.display = 'inline';
  document.getElementById('rb').disabled = true;
  for (var i=0; i<s.lines.length; i++) {
    await new Promise(function(r){ setTimeout(r, 900); });
    var e = document.getElementById('trb');
    e.classList.remove('empty');
    e.textContent = s.lines.slice(0,i+1).join('\n');
  }
  await new Promise(function(r){ setTimeout(r, 600); });
  setSt('\u25cf Processing...');
  document.getElementById('lbdg').style.display = 'none';
  await new Promise(function(r){ setTimeout(r, 1200); });
  showTr(s.tr); showSm(s.sm, s.tt, s.dg); showTn(s.tn, s.ln);
  setTriage(s.lv, s.lb); setSt('Assessment Complete'); setDone(true); updBtn();
}

function confirmTriage() {
  alert('\u2713 Triage confirmed: ' + document.getElementById('tlabel').textContent + '\nRecord sent to duty nurse station.');
}
function contactConsultant() {
  alert('\ud83d\udcde Connecting to on-call consultant...');
}
</script>
</body>
</html>"""

pathlib.Path("templates/index.html").write_text(html, encoding="utf-8")
print("templates/index.html created!")

# ── Write app.py ──────────────────────────────────────────────────────────────
app_code = """import os, base64, tempfile, mimetypes
from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from backend.pipeline import (
    step_transcribe, step_summarise, step_translate, step_tts,
    LANGUAGE_NAMES, MAX_AUDIO_SECONDS,
)

app = FastAPI(title="Kutuliza")
Path("static").mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SUPPORTED_AUDIO_MIMES = {
    "audio/mpeg","audio/mp3","audio/wav","audio/wave",
    "audio/ogg","audio/m4a","audio/aac","audio/x-m4a",
}
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
    stt_language: str  = Form("lug"),
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
"""

Path("app.py").write_text(app_code, encoding="utf-8")
print("app.py created!")

print()
print("=" * 40)
print("All done! Now run:")
print("  uvicorn app:app --reload --port 8000")
print("Then open: http://localhost:8000")
print("=" * 40)