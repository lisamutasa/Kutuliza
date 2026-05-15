// src/components/InputPanel.jsx
// Left panel: input mode switching, microphone button, text area, file upload.

import { useState, useRef } from "react";
import { LANGUAGES } from "../utils/constants";

const AUDIO_ACCEPT = ".mp3,.wav,.ogg,.m4a,.aac,audio/*";
const MAX_BYTES = 100 * 1024 * 1024; // 100 MB (Sunbird limit)

export default function InputPanel({ onSubmitText, onSubmitAudio, status }) {
  const [mode, setMode] = useState("text"); // "text" | "audio"
  const [text, setText] = useState("");
  const [audioFile, setAudioFile] = useState(null);
  const [sttLang, setSttLang] = useState("lug");
  const [targetLang, setTargetLang] = useState("lug");
  const [fileError, setFileError] = useState(null);
  const fileRef = useRef(null);

  const isProcessing = status === "processing" || status === "listening";

  function handleFileChange(e) {
    setFileError(null);
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > MAX_BYTES) {
      setFileError("File is too large (max 100 MB).");
      return;
    }
    setAudioFile(file);
  }

  function handleSubmit() {
    if (mode === "text") {
      if (!text.trim()) return;
      onSubmitText(text.trim(), targetLang);
    } else {
      if (!audioFile) return;
      onSubmitAudio(audioFile, sttLang, targetLang);
    }
  }

  return (
    <div className="flex flex-col h-full gap-5">
      {/* Mode toggle */}
      <div className="flex rounded-xl overflow-hidden border border-slate-200 bg-slate-100">
        {["text", "audio"].map((m) => (
          <button
            key={m}
            onClick={() => setMode(m)}
            className={`flex-1 py-3 text-sm font-semibold tracking-wide transition-colors
              ${mode === m
                ? "bg-white text-slate-900 shadow-sm"
                : "text-slate-500 hover:text-slate-700"}`}
          >
            {m === "text" ? "✍ Text Input" : "🎙 Audio Upload"}
          </button>
        ))}
      </div>

      {/* Target language picker (shared) */}
      <LangSelect
        label="Translate summary into"
        value={targetLang}
        onChange={setTargetLang}
        options={LANGUAGES}
      />

      {/* === TEXT MODE === */}
      {mode === "text" && (
        <textarea
          className="flex-1 min-h-[180px] resize-none rounded-xl border border-slate-200
            bg-white p-4 text-base text-slate-800 placeholder-slate-400
            focus:outline-none focus:ring-2 focus:ring-blue-400 font-mono leading-relaxed"
          placeholder="Type or paste text here…"
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={isProcessing}
        />
      )}

      {/* === AUDIO MODE === */}
      {mode === "audio" && (
        <div className="flex flex-col gap-4 flex-1">
          <LangSelect
            label="Audio spoken in"
            value={sttLang}
            onChange={setSttLang}
            options={[{ code: "eng", name: "English" }, ...LANGUAGES]}
          />

          {/* Drop zone */}
          <button
            type="button"
            onClick={() => fileRef.current?.click()}
            disabled={isProcessing}
            className={`
              flex-1 min-h-[140px] flex flex-col items-center justify-center gap-3
              rounded-xl border-2 border-dashed transition-all
              ${audioFile
                ? "border-blue-400 bg-blue-50 text-blue-700"
                : "border-slate-300 bg-slate-50 text-slate-500 hover:border-blue-300 hover:bg-blue-50"}
            `}
          >
            <MicIcon active={!!audioFile} />
            <span className="text-sm font-medium">
              {audioFile ? audioFile.name : "Click to upload audio (MP3/WAV/OGG/M4A/AAC)"}
            </span>
            <span className="text-xs text-slate-400">Max 5 minutes · 100 MB</span>
          </button>
          <input
            ref={fileRef}
            type="file"
            accept={AUDIO_ACCEPT}
            className="hidden"
            onChange={handleFileChange}
          />
          {fileError && (
            <p className="text-sm text-red-600 font-medium">⚠ {fileError}</p>
          )}
        </div>
      )}

      {/* Submit */}
      <button
        onClick={handleSubmit}
        disabled={isProcessing || (mode === "text" ? !text.trim() : !audioFile)}
        className={`
          w-full py-5 rounded-2xl text-lg font-bold tracking-wide
          transition-all duration-200 shadow-sm
          ${isProcessing
            ? "bg-slate-300 text-slate-500 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700 active:scale-[0.98] text-white"}
        `}
      >
        {isProcessing ? (
          <span className="flex items-center justify-center gap-3">
            <Spinner /> {status === "listening" ? "Listening…" : "Processing…"}
          </span>
        ) : (
          "Run Pipeline →"
        )}
      </button>
    </div>
  );
}

function LangSelect({ label, value, onChange, options }) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
        {label}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-lg border border-slate-200 bg-white px-3 py-2.5
          text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        {options.map((l) => (
          <option key={l.code} value={l.code}>{l.name}</option>
        ))}
      </select>
    </div>
  );
}

function MicIcon({ active }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={`w-10 h-10 ${active ? "text-blue-500" : "text-slate-400"}`}>
      <rect x="9" y="2" width="6" height="12" rx="3" stroke="currentColor" strokeWidth="2"/>
      <path d="M5 11a7 7 0 0014 0" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
      <line x1="12" y1="18" x2="12" y2="22" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
      <line x1="8" y1="22" x2="16" y2="22" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
    </svg>
  );
}

function Spinner() {
  return (
    <svg className="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
      <path className="opacity-75" fill="currentColor"
        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
    </svg>
  );
}
