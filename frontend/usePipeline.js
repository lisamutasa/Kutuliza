// frontend/hooks/usePipeline.js
import { useState } from "react";
import { processText, processAudio } from "../utils/api";

export function usePipeline() {
  const [status, setStatus] = useState("idle");
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState("");
  const [translation, setTranslation] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [targetLanguageName, setTargetLanguageName] = useState("");
  const [triageLevel, setTriageLevel] = useState("Neutral");
  const [dangerSigns, setDangerSigns] = useState([]);
  const [error, setError] = useState("");

  const reset = () => {
    setStatus("idle");
    setTranscript("");
    setSummary("");
    setTranslation("");
    setAudioUrl("");
    setDangerSigns([]);
    setError("");
  };

  const submitText = async (text, targetLang) => {
    setStatus("processing");
    setError("");
    try {
      const data = await processText(text, targetLang);
      updateUI(data);
    } catch (err) {
      setError(err.message);
      setStatus("error");
    }
  };

  const submitAudio = async (audioFile, sttLang, targetLang) => {
    setStatus("processing");
    setError("");
    try {
      const data = await processAudio(audioFile, sttLang, targetLang);
      updateUI(data);
    } catch (err) {
      setError(err.message);
      setStatus("error");
    }
  };

  const updateUI = (data) => {
    setTranscript(data.transcript || data.source_text || "");
    setSummary(data.summary || "");
    setTranslation(data.translation || "");
    setTargetLanguageName(data.target_language_name || "");

    // Create audio URL from base64
    if (data.audio_b64) {
      const audioBlob = new Blob(
        [Uint8Array.from(atob(data.audio_b64), c => c.charCodeAt(0))],
        { type: "audio/mpeg" }
      );
      setAudioUrl(URL.createObjectURL(audioBlob));
    }

    // Simple triage detection
    const triageText = (data.summary || "").toLowerCase();
    if (triageText.includes("red") || triageText.includes("emergency")) {
      setTriageLevel("Red");
    } else if (triageText.includes("yellow") || triageText.includes("priority")) {
      setTriageLevel("Yellow");
    } else {
      setTriageLevel("Green");
    }

    setStatus("done");
  };

  const runTestScenario = (id) => {
    const scenarios = {
      maternal: "Ndi omwiru, ndi na obulumi munnyo mu lubuto era ndi na omusana omukali. Ensimbi zange zirwadde.",
      child: "Mutoto wange alina musango wa kufura na omusana.",
    };
    submitText(scenarios[id] || scenarios.maternal, "lug");
  };

  return {
    status,
    transcript,
    summary,
    translation,
    audioUrl,
    targetLanguageName,
    triageLevel,
    dangerSigns,
    error,
    submitText,
    submitAudio,
    runTestScenario,
    reset,
  };
}
