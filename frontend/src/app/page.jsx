"use client";
import { useState, useEffect } from "react";
import { LANGUAGES } from "../utils/constants";   // Make sure this file exists

export default function KutulizaTriage() {
  const [status, setStatus] = useState("idle");
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState("");
  const [translation, setTranslation] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [targetLanguageName, setTargetLanguageName] = useState("");
  const [triageLevel, setTriageLevel] = useState("Neutral");
  const [error, setError] = useState("");
  const [text, setText] = useState("");
  const [targetLang, setTargetLang] = useState("lug");
  const [audioFile, setAudioFile] = useState(null);

  const busy = status === "processing";

  const processInput = async (inputText = "", isAudio = false) => {
    setStatus("processing");
    setError("");

    try {
      let data;

      if (isAudio && audioFile) {
        const formData = new FormData();
        formData.append("audio", audioFile);
        formData.append("target_language", targetLang);

        const res = await fetch("http://127.0.0.1:8000/api/process/audio", {
          method: "POST",
          body: formData,
        });
        data = await res.json();
      } else {
        const res = await fetch("http://127.0.0.1:8000/api/process/text", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: inputText || text, target_language: targetLang }),
        });
        data = await res.json();
      }

      // Update UI
      setTranscript(data.transcript || data.source_text || "");
      setSummary(data.summary || "");
      setTranslation(data.translation || "");
      setTargetLanguageName(data.target_language_name || "Luganda");

      // Create playable audio from base64
      if (data.audio_b64) {
        const byteCharacters = atob(data.audio_b64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: "audio/mpeg" });
        setAudioUrl(URL.createObjectURL(blob));
      }

      // Detect triage level
      const lowerSummary = (data.summary || "").toLowerCase();
      if (lowerSummary.includes("red") || lowerSummary.includes("emergency")) {
        setTriageLevel("Red");
      } else if (lowerSummary.includes("yellow")) {
        setTriageLevel("Yellow");
      } else {
        setTriageLevel("Green");
      }

      setStatus("done");
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to connect to backend");
      setStatus("error");
    }
  };

  const runTestScenario = () => {
    const sample = "Ndi omwiru, ndi na obulumi munnyo mu lubuto era ndi na omusana omukali. Ensimbi zange zirwadde nnyo.";
    setText(sample);
    processInput(sample);
  };

  const reset = () => {
    setStatus("idle");
    setTranscript("");
    setSummary("");
    setTranslation("");
    setAudioUrl("");
    setError("");
  };

  return (
    <div className="min-h-screen bg-slate-100 font-sans">
      {/* Header */}
      <div className="bg-white border-b-4 border-red-600 p-6 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-red-600 rounded-xl flex items-center justify-center text-white text-3xl">✚</div>
          <div>
            <h1 className="text-4xl font-bold text-slate-900">Kutuliza</h1>
            <p className="text-sm text-slate-500">AI MEDICAL TRIAGE • UGANDA</p>
          </div>
        </div>

        <div className="text-center">
          <div className="text-xs text-slate-500 mb-1">CURRENT TRIAGE</div>
          <div className={`inline-flex items-center gap-3 px-6 py-3 rounded-2xl text-xl font-bold
            ${triageLevel === "Red" ? "bg-red-600 text-white" : 
              triageLevel === "Yellow" ? "bg-yellow-500 text-black" : "bg-green-600 text-white"}`}>
            {triageLevel === "Red" && "🚨 EMERGENCY"}
            {triageLevel === "Yellow" && "⚠️ PRIORITY"}
            {triageLevel === "Green" && "✅ ROUTINE"}
          </div>
        </div>

        <button
          onClick={runTestScenario}
          className="bg-slate-900 text-white px-8 py-4 rounded-2xl font-semibold hover:bg-black"
        >
          Test Emergency Scenario
        </button>
      </div>

      <div className="max-w-7xl mx-auto p-6 grid grid-cols-2 gap-6">
        {/* Left - Input */}
        <div className="bg-white rounded-3xl p-8 shadow">
          <h2 className="text-lg font-semibold mb-6">PATIENT INPUT</h2>

          <select
            value={targetLang}
            onChange={(e) => setTargetLang(e.target.value)}
            className="w-full p-4 border rounded-2xl mb-6"
          >
            {LANGUAGES?.map(l => (
              <option key={l.code} value={l.code}>{l.name}</option>
            )) || (
              <>
                <option value="lug">Luganda</option>
                <option value="nyn">Runyankole</option>
                <option value="ach">Acholi</option>
              </>
            )}
          </select>

          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type patient symptoms here..."
            className="w-full h-48 p-5 border rounded-2xl mb-6 font-mono"
          />

          <button
            onClick={() => processInput()}
            disabled={busy || !text.trim()}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white py-5 rounded-2xl font-bold text-lg"
          >
            {busy ? "Processing..." : "Process with Sunbird AI"}
          </button>
        </div>

        {/* Right - Output */}
        <div className="bg-white rounded-3xl p-8 shadow space-y-8">
          <h2 className="text-lg font-semibold">CLINICAL ANALYSIS</h2>

          {transcript && (
            <div>
              <h3 className="text-sm font-bold text-slate-500 mb-2">TRANSCRIPT</h3>
              <p className="bg-slate-50 p-5 rounded-2xl">{transcript}</p>
            </div>
          )}

          {summary && (
            <div>
              <h3 className="text-sm font-bold text-slate-500 mb-2">NURSE SUMMARY</h3>
              <p className="bg-slate-50 p-5 rounded-2xl whitespace-pre-wrap">{summary}</p>
            </div>
          )}

          {translation && (
            <div>
              <h3 className="text-sm font-bold text-slate-500 mb-2">TRANSLATION — {targetLanguageName}</h3>
              <p className="bg-slate-50 p-5 rounded-2xl">{translation}</p>
            </div>
          )}

          {audioUrl && (
            <div>
              <h3 className="text-sm font-bold text-slate-500 mb-3">🔊 AUDIO PLAYBACK</h3>
              <audio controls src={audioUrl} className="w-full" />
            </div>
          )}

          {error && <p className="text-red-600 bg-red-50 p-4 rounded-2xl">{error}</p>}
        </div>
      </div>
    </div>
  );
}