// src/components/ActionBar.jsx
// Bottom touch-friendly action bar with triage confirmation, print, and consultant contact.

import { TEST_SCENARIOS } from "../utils/constants";

export default function ActionBar({
  onConfirmTriage,
  onPrint,
  onContactConsultant,
  onTestScenario,
  onReset,
  triageLevel,
  status,
}) {
  const isDone = status === "done";
  const isProcessing = status === "processing" || status === "listening";

  return (
    <footer className="border-t-2 border-slate-200 bg-white px-6 py-4">
      <div className="flex items-center gap-3 flex-wrap">

        {/* === Test scenario buttons === */}
        <div className="flex items-center gap-2 mr-auto flex-wrap">
          <span className="text-xs font-mono text-slate-400 uppercase tracking-widest mr-1">
            Demo
          </span>
          {TEST_SCENARIOS.map((s) => (
            <button
              key={s.id}
              onClick={() => onTestScenario(s.id)}
              disabled={isProcessing}
              className="px-4 py-3 rounded-xl text-sm font-semibold border-2
                border-slate-300 bg-white text-slate-600
                hover:border-blue-400 hover:text-blue-700
                active:scale-[0.97] transition-all disabled:opacity-40"
            >
              ⚡ Test: {s.label}
            </button>
          ))}

          {/* Reset */}
          {(isDone || status === "error") && (
            <button
              onClick={onReset}
              className="px-4 py-3 rounded-xl text-sm font-semibold border-2
                border-slate-200 bg-slate-50 text-slate-500
                hover:bg-slate-100 active:scale-[0.97] transition-all"
            >
              ↺ Reset
            </button>
          )}
        </div>

        {/* === Primary actions (only active when triage is done) === */}
        <ActionButton
          label="✓ Confirm Triage"
          onClick={onConfirmTriage}
          disabled={!isDone}
          variant={
            triageLevel === "EMERGENCY" ? "danger" :
            triageLevel === "PRIORITY"  ? "warning" : "primary"
          }
        />

        <ActionButton
          label="🖨 Print Patient ID"
          onClick={onPrint}
          disabled={!isDone}
          variant="secondary"
        />

        <ActionButton
          label="📞 Contact Consultant"
          onClick={onContactConsultant}
          disabled={!isDone}
          variant="secondary"
        />
      </div>
    </footer>
  );
}

function ActionButton({ label, onClick, disabled, variant = "primary" }) {
  const base = `
    px-6 py-4 rounded-2xl text-base font-bold tracking-wide
    transition-all duration-150 active:scale-[0.97] shadow-sm
    disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none
  `;
  const variants = {
    primary:   "bg-blue-600 text-white hover:bg-blue-700",
    danger:    "bg-red-600 text-white hover:bg-red-700 animate-pulse",
    warning:   "bg-yellow-500 text-white hover:bg-yellow-600",
    secondary: "bg-white text-slate-700 border-2 border-slate-200 hover:bg-slate-50",
  };
  return (
    <button onClick={onClick} disabled={disabled} className={`${base} ${variants[variant]}`}>
      {label}
    </button>
  );
}
