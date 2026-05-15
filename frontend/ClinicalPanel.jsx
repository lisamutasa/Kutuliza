// src/components/ClinicalPanel.jsx
// Right panel: live transcript, nurse's summary, danger signs, audio player.

export default function ClinicalPanel({
  status,
  transcript,
  summary,
  translation,
  audioUrl,
  targetLanguageName,
  dangerSigns,
  clinicalTitle,
  triageLevel,
}) {
  const isEmpty = status === "idle";
  const isLoading = status === "processing" || status === "listening";

  return (
    <div className="flex flex-col gap-5 h-full">

      {/* Live Transcript */}
      <Section
        title="Live Transcript"
        badge={status === "listening" ? "● Listening" : null}
        badgeColor="text-red-500"
        empty={isEmpty && !transcript}
        emptyText="Transcript will appear here..."
      >
        {transcript && (
          <pre className="whitespace-pre-wrap font-mono text-sm text-slate-700
            leading-relaxed bg-slate-50 rounded-lg p-3 border border-slate-100">
            {transcript}
          </pre>
        )}
        {isLoading && !transcript && <PulsePlaceholder lines={3} />}
      </Section>

      {/* Nurse's Summary */}
      <Section
        title={clinicalTitle || "Nurse's Summary"}
        empty={isEmpty && !summary}
        emptyText="Clinical summary will appear here..."
      >
        {summary && (
          <p className="text-slate-800 text-sm leading-relaxed">{summary}</p>
        )}
        {isLoading && !summary && <PulsePlaceholder lines={4} />}

        {/* Danger signs */}
        {dangerSigns && dangerSigns.length > 0 && (
          <div className="mt-3">
            <p className="text-xs font-bold text-red-600 uppercase tracking-wider mb-2">
              ⚠ Danger Signs Detected
            </p>
            <ul className="space-y-1">
              {dangerSigns.map((sign, i) => (
                <li key={i} className="flex items-center gap-2 text-sm text-red-700
                  bg-red-50 rounded-lg px-3 py-2 border border-red-200">
                  <span className="w-2 h-2 rounded-full bg-red-500 flex-shrink-0" />
                  {sign}
                </li>
              ))}
            </ul>
          </div>
        )}
      </Section>

      {/* Translation */}
      <Section
        title={targetLanguageName ? `Translation — ${targetLanguageName}` : "Translation"}
        empty={isEmpty && !translation}
        emptyText="Translated summary will appear here..."
      >
        {translation && (
          <p className="text-slate-800 text-sm leading-relaxed font-medium">
            {translation}
          </p>
        )}
        {isLoading && !translation && <PulsePlaceholder lines={3} />}
      </Section>

      {/* Audio Player */}
      {audioUrl && (
        <div className="bg-slate-900 rounded-2xl p-4 flex flex-col gap-2">
          <p className="text-xs font-mono text-slate-400 uppercase tracking-widest">
            🔊 Synthesised Speech — {targetLanguageName}
          </p>
          <audio
            controls
            src={audioUrl}
            className="w-full h-10 rounded-lg"
          />
        </div>
      )}
    </div>
  );
}

function Section({ title, badge, badgeColor, empty, emptyText, children }) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-4 flex flex-col gap-3 flex-1 min-h-0">
      <div className="flex items-center justify-between">
        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest">
          {title}
        </h3>
        {badge && (
          <span className={`text-xs font-mono font-semibold animate-pulse ${badgeColor}`}>
            {badge}
          </span>
        )}
      </div>
      {empty ? (
        <p className="text-sm text-slate-300 italic">{emptyText}</p>
      ) : (
        <div className="overflow-y-auto">{children}</div>
      )}
    </div>
  );
}

function PulsePlaceholder({ lines = 3 }) {
  return (
    <div className="space-y-2 animate-pulse">
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="h-3 rounded bg-slate-200"
          style={{ width: `${i === lines - 1 ? 60 : 100}%` }}
        />
      ))}
    </div>
  );
}
