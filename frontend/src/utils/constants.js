// src/utils/constants.js

/** Supported target languages for translation and TTS. */
export const LANGUAGES = [
  { code: "lug", name: "Luganda" },
  { code: "nyn", name: "Runyankole" },
  { code: "teo", name: "Ateso" },
  { code: "lgg", name: "Lugbara" },
  { code: "ach", name: "Acholi" },
];

/** Triage level definitions. */
export const TRIAGE_LEVELS = {
  NEUTRAL: {
    key: "NEUTRAL",
    label: "Awaiting Assessment",
    color: "neutral",
    headerClass: "bg-slate-100 border-slate-300",
    badgeClass: "bg-slate-200 text-slate-700",
    dotClass: "bg-slate-400",
  },
  ROUTINE: {
    key: "ROUTINE",
    label: "Routine",
    color: "green",
    headerClass: "bg-green-50 border-green-300",
    badgeClass: "bg-green-100 text-green-800",
    dotClass: "bg-green-500",
  },
  PRIORITY: {
    key: "PRIORITY",
    label: "Priority",
    color: "yellow",
    headerClass: "bg-yellow-50 border-yellow-300",
    badgeClass: "bg-yellow-100 text-yellow-800",
    dotClass: "bg-yellow-500",
  },
  EMERGENCY: {
    key: "EMERGENCY",
    label: "Emergency",
    color: "red",
    headerClass: "bg-red-50 border-red-400",
    badgeClass: "bg-red-100 text-red-800",
    dotClass: "bg-red-500 animate-pulse",
  },
};

/** Pre-built test scenarios for the demo button. */
export const TEST_SCENARIOS = [
  {
    id: "preeclampsia",
    label: "Maternal Emergency",
    triageLevel: "EMERGENCY",
    sttLanguage: "lug",
    transcriptLines: [
      "Nnyabo, omwana wange afumba nnyo...",
      "Alina obukambwe obungi mu maaso...",
      "Ebyenyi ebinafu bingi mu bigere n'emikono...",
      "N'okulaba kubi nnyo, n'omutwe ogukoma.",
    ],
    transcript:
      "Nnyabo, omwana wange afumba nnyo, alina obukambwe mu maaso, ebyenyi ebinafu mu bigere n'emikono, n'okulaba kubi, n'omutwe ogukoma.",
    summary:
      "Patient reports severe headache, blurred vision, and significant oedema in the face, hands, and feet. Symptoms are consistent with a hypertensive emergency in pregnancy.",
    dangerSigns: [
      "Severe headache",
      "Blurred / disturbed vision",
      "Facial and peripheral oedema",
      "Possible hypertension",
    ],
    clinicalTitle: "Maternal Emergency: Possible Preeclampsia",
    translation:
      "Omulwadde alaga omutwe ogukoma nnyo, okulaba kubi, n'ebyenyi ebinafu mu maaso, emikono n'ebigere. Bino bitereka mu bulwadde bw'omutima ogw'omuntu owazaalira.",
  },
  {
    id: "malaria",
    label: "Paediatric Fever",
    triageLevel: "PRIORITY",
    sttLanguage: "nyn",
    transcriptLines: [
      "Omwana wange afite omusujja mungi...",
      "Yaayogera enjura nyinshi...",
      "N'okurya akayirwa.",
    ],
    transcript:
      "Omwana wange afite omusujja mungi, yaayogera enjura nyinshi, n'okurya akayirwa.",
    summary:
      "Child presents with high fever, multiple vomiting episodes, and loss of appetite. Symptoms suggest possible malaria or acute infection requiring rapid diagnostic test.",
    dangerSigns: [
      "High fever (>38.5 °C suspected)",
      "Repeated vomiting",
      "Poor feeding / appetite loss",
    ],
    clinicalTitle: "Paediatric Priority: Possible Malaria",
    translation:
      "Omwana afite omusujja mungi, yayogera enjura nyinshi kandi taribwa kirungi. Ebimenyetso bitereka endwara ya malaria oba obutane obw'omubiri.",
  },
];
