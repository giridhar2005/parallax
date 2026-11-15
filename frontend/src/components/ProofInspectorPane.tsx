import React, { useState } from "react";
import {
  FileText,
  AlertTriangle,
  ZoomIn,
  ZoomOut,
  Copy,
  Check,
  ShieldAlert,
  Sparkles,
} from "lucide-react";
import { Contradiction } from "../types";

interface ProofInspectorPaneProps {
  contradiction: Contradiction | null;
}

export const ProofInspectorPane: React.FC<ProofInspectorPaneProps> = ({
  contradiction,
}) => {
  const [copied, setCopied] = useState<boolean>(false);
  const [zoomLevel, setZoomLevel] = useState<number>(100);

  if (!contradiction) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center bg-[#0E0E10] text-zinc-500 font-mono text-xs">
        <FileText className="w-8 h-8 text-zinc-600 mb-2" />
        <p>No contradiction selected. Scrub timeline to inspect documentary proof.</p>
      </div>
    );
  }

  const box = contradiction.evidence_box || [0.12, 0.48, 0.88, 0.62];
  const [x1, y1, x2, y2] = box;

  const handleCopy = () => {
    if (contradiction.evidence_text) {
      navigator.clipboard.writeText(contradiction.evidence_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-[#09090B] overflow-hidden">
      {/* Pane Header */}
      <div className="h-9 px-3 border-b border-[#27272A] bg-[#0E0E10] flex items-center justify-between text-xs font-mono text-zinc-400">
        <div className="flex items-center space-x-2">
          <FileText className="w-3.5 h-3.5 text-rose-400" />
          <span className="font-semibold text-zinc-200">
            CONTRADICTION PROOF ({contradiction.evidence_type?.toUpperCase() || "DOCUMENT"})
          </span>
        </div>
        <div className="flex items-center space-x-2 text-[11px] text-zinc-500">
          <span>PAGE {contradiction.evidence_page || 4}</span>
          <span>·</span>
          <span className="text-zinc-300">VALID TIME: {contradiction.valid_time?.slice(0, 10)}</span>
        </div>
      </div>

      {/* PDF Visual Canvas Viewport with Bounding Box SVG */}
      <div className="relative aspect-video bg-[#111113] border-b border-[#27272A] p-4 flex items-center justify-center overflow-hidden">
        {/* Simulated Legal Document Canvas */}
        <div
          className="relative w-full h-full bg-[#18181B] border border-[#27272A] rounded p-4 text-[10px] font-mono text-zinc-400 select-none overflow-hidden shadow-inner"
          style={{ transform: `scale(${zoomLevel / 100})`, transformOrigin: "center" }}
        >
          {/* Header Lines */}
          <div className="border-b border-zinc-700/60 pb-2 mb-3 flex justify-between items-center text-zinc-500">
            <span>DELOITTE & TOUCHE / SEC EXHIBIT ARCHIVE</span>
            <span>RESTRICTED FORENSIC DISCLOSURE</span>
          </div>

          {/* Dummy Document Text Lines */}
          <div className="space-y-1 opacity-40">
            <div className="h-2 bg-zinc-600 rounded w-5/6" />
            <div className="h-2 bg-zinc-600 rounded w-4/6" />
            <div className="h-2 bg-zinc-600 rounded w-full" />
            <div className="h-2 bg-zinc-600 rounded w-3/4" />
          </div>

          {/* Glowing Red SVG Bounding Box around the conflicting clause */}
          <div
            className="absolute rounded border-2 border-rose-500 bg-rose-500/10 box-highlight-pulse flex flex-col justify-between p-2 z-10"
            style={{
              left: `${x1 * 100}%`,
              top: `${y1 * 100}%`,
              width: `${(x2 - x1) * 100}%`,
              height: `${(y2 - y1) * 100}%`,
            }}
          >
            <div className="flex items-center justify-between text-[9px] font-semibold text-rose-300">
              <span className="flex items-center space-x-1">
                <ShieldAlert className="w-2.5 h-2.5" />
                <span>FORENSIC CONFLICT HIGHLIGHT [{x1}, {y1}]</span>
              </span>
              <span>SCORE: {contradiction.nli_score.toFixed(2)}</span>
            </div>
            <p className="text-[10px] font-mono font-medium text-white leading-tight line-clamp-2">
              {contradiction.evidence_text}
            </p>
          </div>

          {/* Subsequent Dummy Text Lines */}
          <div className="space-y-1 opacity-40 mt-16">
            <div className="h-2 bg-zinc-600 rounded w-full" />
            <div className="h-2 bg-zinc-600 rounded w-2/3" />
            <div className="h-2 bg-zinc-600 rounded w-5/6" />
          </div>
        </div>

        {/* Zoom Controls Overlay */}
        <div className="absolute bottom-3 right-3 flex items-center space-x-1 bg-[#09090B]/80 border border-[#27272A] rounded p-1 text-zinc-400">
          <button
            onClick={() => setZoomLevel((z) => Math.max(80, z - 10))}
            className="p-1 hover:text-white hover:bg-zinc-800 rounded transition"
            title="Zoom Out"
          >
            <ZoomOut className="w-3 h-3" />
          </button>
          <span className="text-[10px] font-mono px-1 tabular-nums">{zoomLevel}%</span>
          <button
            onClick={() => setZoomLevel((z) => Math.min(140, z + 10))}
            className="p-1 hover:text-white hover:bg-zinc-800 rounded transition"
            title="Zoom In"
          >
            <ZoomIn className="w-3 h-3" />
          </button>
        </div>
      </div>

      {/* Cross-Encoder DeBERTa NLI Analysis Card */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-[#0E0E10]">
        {/* NLI Metrics Pill & Probability Bars */}
        <div className="bg-[#111113] border border-[#27272A] rounded p-3 space-y-2.5 font-mono text-xs">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Sparkles className="w-3.5 h-3.5 text-rose-400" />
              <span className="font-semibold text-zinc-200">DeBERTa Cross-Encoder NLI Score</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 border border-rose-500/50 font-bold text-[11px] tabular-nums">
                {contradiction.nli_score.toFixed(3)} {contradiction.nli_label}
              </span>
              <span className="px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-300 text-[10px]">
                {contradiction.severity}
              </span>
            </div>
          </div>

          {/* Probability Distribution */}
          <div className="space-y-1 text-[11px]">
            <div className="flex justify-between text-zinc-400">
              <span>Contradiction Probability</span>
              <span className="text-rose-400 font-bold tabular-nums">
                {(contradiction.contradiction_prob * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-[#18181B] h-1.5 rounded-full overflow-hidden">
              <div
                className="bg-rose-500 h-full rounded-full transition-all duration-300"
                style={{ width: `${contradiction.contradiction_prob * 100}%` }}
              />
            </div>

            <div className="flex justify-between text-zinc-500 text-[10px] pt-1">
              <span>Entailment: {(contradiction.entailment_prob * 100).toFixed(1)}%</span>
              <span>Neutral: {(contradiction.neutral_prob * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>

        {/* Forensic Contradiction Reasoning Box */}
        <div className="bg-[#111113] border border-[#27272A] rounded p-3 space-y-2 font-mono text-xs">
          <div className="flex items-center justify-between text-zinc-400 text-[11px] pb-1 border-b border-[#1F1F23]">
            <span className="font-semibold text-zinc-300 flex items-center space-x-1.5">
              <AlertTriangle className="w-3 h-3 text-amber-400" />
              <span>Forensic Reasoning</span>
            </span>
            <button
              onClick={handleCopy}
              className="flex items-center space-x-1 text-[10px] text-zinc-400 hover:text-white transition"
            >
              {copied ? <Check className="w-2.5 h-2.5 text-emerald-400" /> : <Copy className="w-2.5 h-2.5" />}
              <span>{copied ? "Copied" : "Copy Evidence"}</span>
            </button>
          </div>

          <p className="text-zinc-200 leading-relaxed text-[11px]">
            {contradiction.reasoning}
          </p>

          <div className="mt-2 pt-2 border-t border-[#1F1F23] text-[10px] text-zinc-500 flex justify-between">
            <span>Claim ID: {contradiction.claim_id}</span>
            <span>Evidence ID: {contradiction.evidence_id}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
