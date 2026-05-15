// frontend/utils/api.js
const BASE_URL = "http://127.0.0.1:8000";

export async function processText(text, target_language = "lug") {
  const res = await fetch(`${BASE_URL}/api/process/text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, target_language }),
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || "Failed to process text");
  }
  return res.json();
}

export async function processAudio(audioFile, stt_language = "lug", target_language = "lug") {
  const formData = new FormData();
  formData.append("audio", audioFile);
  formData.append("stt_language", stt_language);
  formData.append("target_language", target_language);

  const res = await fetch(`${BASE_URL}/api/process/audio`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || "Failed to process audio");
  }
  return res.json();
}