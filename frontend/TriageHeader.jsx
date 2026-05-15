// src/components/TriageHeader.jsx
// Large status banner that changes color with triage level.

import { TRIAGE_LEVELS } from "../utils/constants";

export default function TriageHeader({ triageLevel, status }) {
  const cfg = TRIAGE_LEVELS[triageLevel];

  return (
    <header
      className={`
        flex items-center justify-between px-8 py-5
        border-b-4 transition-all duration-500
        ${cfg.headerClass}
      `}
    >
      {/* Left: Branding */}
      <div className="flex items-center gap-4">
        <div
          className={`
            w-12 h-12 rounded-xl flex items-center justify-center
            transition-colors duration-500
            ${triageLevel === "NEUTRAL" ? "bg-slate-600" :
              triageLevel === "ROUTINE"   ? "bg-green-600" :
              triageLevel === "PRIORITY"  ? "bg-yellow-500" :
                                            "bg-red-600"}
          `}
        >
          <CrossIcon />
        </div>
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Kutuliza
          </h1>
          <p className="text-xs font-mono text-slate-500 tracking-widest uppercase">
            AI Medical Triage · Uganda
          </p>
        </div>
      </div>

      {/* Centre: Triage Badge */}
      <div className="flex flex-col items-center gap-1">
        <span className="text-xs font-mono text-slate-500 uppercase tracking-widest">
          Triage Level
        </span>
        <span
          className={`
            flex items-center gap-2 px-5 py-2 rounded-lg text-lg font-bold
            border-2 transition-all duration-500
            ${cfg.badgeClass}
            ${triageLevel === "EMERGENCY" ? "border-red-400" :
              triageLevel === "PRIORITY"  ? "border-yellow-400" :
              triageLevel === "ROUTINE"   ? "border-green-400" :
                                            "border-slate-300"}
          `}
        >
          <span className={`w-3 h-3 rounded-full ${cfg.dotClass}`} />
          {cfg.label}
        </span>
      </div>

      {/* Right: System clock + status */}
      <div className="flex flex-col items-end gap-1">
        <LiveClock />
        <span className="text-xs font-mono text-slate-500">
          {status === "idle"       && "Ready"}
          {status === "listening"  && "⬤ Listening..."}
          {status === "processing" && "⬤ Processing..."}
          {status === "done"       && "Assessment Complete"}
          {status === "error"      && "⚠ Error"}
        </span>
      </div>
    </header>
  );
}

function CrossIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" className="w-7 h-7">
      <path
        d="M12 2v20M2 12h20"
        stroke="white" strokeWidth="3" strokeLinecap="round"
      />
    </svg>
  );
}

function LiveClock() {
  const [time, setTime] = React.useState(new Date());

  React.useEffect(() => {
    const id = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <span className="text-xl font-mono font-semibold text-slate-700">
      {time.toLocaleTimeString("en-UG", { hour: "2-digit", minute: "2-digit", second: "2-digit" })}
    </span>
  );
}

// React must be available in scope (Next.js provides it globally)
import React from "react";
