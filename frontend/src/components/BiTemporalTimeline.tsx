import React from "react";
import { Clock, Calendar, AlertOctagon, GitCommit } from "lucide-react";
import { Contradiction } from "../types";

interface BiTemporalTimelineProps {
  currentTimeSec: number;
  totalDurationSec?: number;
  contradictions: Contradiction[];
  activeContradiction: Contradiction | null;
  onSeek: (seconds: number) => void;
  onSelectContradiction: (c: Contradiction) => void;
}

export const BiTemporalTimeline: React.FC<BiTemporalTimelineProps> = ({
  currentTimeSec,
  totalDurationSec = 724.5,
  contradictions,
  activeContradiction,
  onSeek,
  onSelectContradiction,
}) => {
  const formatTimecode = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
  };

  const scrubberPercentage = Math.min(100, Math.max(0, (currentTimeSec / totalDurationSec) * 100));

  const handleTrackClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const ratio = Math.max(0, Math.min(1, clickX / rect.width));
    onSeek(ratio * totalDurationSec);
  };

  return (
    <div className="h-32 border-t border-[#27272A] bg-[#09090B] px-4 py-2.5 flex flex-col justify-between font-mono select-none">
      {/* Timeline Controls Header */}
      <div className="flex items-center justify-between text-[11px] text-zinc-400">
        <div className="flex items-center space-x-3">
          <span className="font-semibold tracking-wider text-zinc-300 flex items-center space-x-1.5">
            <Clock className="w-3 h-3 text-emerald-400" />
            <span>TRANSACTION TIME (MEDIA PLAYBACK)</span>
          </span>
          <span className="text-zinc-600">vs</span>
          <span className="font-semibold tracking-wider text-zinc-400 flex items-center space-x-1.5">
            <Calendar className="w-3 h-3 text-blue-400" />
            <span>VALID TIME (HISTORICAL EVENTS)</span>
          </span>
        </div>

        <div className="flex items-center space-x-3 text-xs tabular-nums">
          <span className="text-emerald-400 font-semibold">{formatTimecode(currentTimeSec)}</span>
          <span className="text-zinc-600">/</span>
          <span className="text-zinc-400">{formatTimecode(totalDurationSec)}</span>
          <span className="text-zinc-500 text-[10px]">({contradictions.length} Contradictions Mapped)</span>
        </div>
      </div>

      {/* Valid Time Reference Bar (Historical Calendar Epochs) */}
      <div className="relative h-6 bg-[#111113] border border-[#27272A] rounded flex items-center px-2 text-[10px] text-zinc-500 overflow-hidden">
        <span className="text-zinc-400 font-semibold mr-4 text-[9px] uppercase tracking-wider">
          Valid Time:
        </span>
        <div className="flex-1 flex justify-between">
          <span>2023-01 (Baseline)</span>
          <span className="text-rose-400 font-medium">2023-06 (Wire $14.2M)</span>
          <span className="text-amber-400 font-medium">2023-07 (Fleet Lien)</span>
          <span className="text-blue-400 font-medium">2023-08 (EMSA Notice)</span>
          <span>2023-09 (Board Mtg)</span>
          <span>2024-02 (Deposition)</span>
        </div>
      </div>

      {/* Primary Scrubber Track & Contradiction Spike Markers */}
      <div
        onClick={handleTrackClick}
        className="relative h-10 bg-[#111113] border border-[#27272A] rounded cursor-pointer group flex items-center"
      >
        {/* Subtle Horizontal Grid Lines */}
        <div className="absolute inset-x-0 h-[1px] bg-[#1F1F23]" />

        {/* Ruler Tick Marks along playback track */}
        {Array.from({ length: 13 }).map((_, idx) => (
          <div
            key={idx}
            className="absolute top-0 bottom-0 w-[1px] bg-[#1F1F23]"
            style={{ left: `${(idx / 12) * 100}%` }}
          >
            <span className="absolute bottom-1 left-1 text-[9px] font-mono text-zinc-600">
              {idx * 60}s
            </span>
          </div>
        ))}

        {/* Contradiction Spike Markers */}
        {contradictions.map((c) => {
          const spikeTime = c.transaction_time_start || 0;
          const leftPercent = (spikeTime / totalDurationSec) * 100;
          const isSelected = activeContradiction?.id === c.id;

          return (
            <div
              key={c.id}
              onClick={(e) => {
                e.stopPropagation();
                onSelectContradiction(c);
              }}
              className="absolute -top-1.5 -bottom-1.5 flex flex-col items-center justify-center z-20 cursor-pointer group/spike"
              style={{ left: `${leftPercent}%` }}
            >
              {/* Spike Indicator Icon */}
              <div
                className={`p-1 rounded-full border transition-all ${
                  isSelected
                    ? "bg-rose-500 border-white text-white scale-125 shadow-lg shadow-rose-500/50"
                    : "bg-rose-500/20 border-rose-500/60 text-rose-400 hover:scale-110"
                }`}
              >
                <AlertOctagon className="w-3.5 h-3.5" />
              </div>

              {/* Score Tag */}
              <span
                className={`text-[9px] font-bold px-1 rounded mt-0.5 tabular-nums ${
                  isSelected
                    ? "bg-rose-500 text-white"
                    : "bg-[#18181B] text-rose-400 border border-rose-500/30"
                }`}
              >
                {c.nli_score.toFixed(2)}
              </span>

              {/* Hover Tooltip */}
              <div className="absolute bottom-12 hidden group-hover/spike:flex flex-col bg-[#111113] border border-rose-500/40 rounded p-2 text-[10px] w-64 shadow-2xl z-30 pointer-events-none">
                <div className="flex justify-between font-bold text-rose-400 mb-1">
                  <span>{c.nli_score.toFixed(3)} CONTRADICTION</span>
                  <span>{c.severity}</span>
                </div>
                <p className="text-zinc-200 line-clamp-2 leading-tight">
                  {c.claim_statement}
                </p>
                <div className="text-[9px] text-zinc-400 mt-1 border-t border-zinc-800 pt-1">
                  Proof: {c.evidence_type} · Valid Time: {c.valid_time?.slice(0, 10)}
                </div>
              </div>
            </div>
          );
        })}

        {/* Scrubber Playhead */}
        <div
          className="absolute top-0 bottom-0 w-[2px] bg-emerald-400 z-30 shadow-[0_0_10px_rgba(16,185,129,0.8)] pointer-events-none"
          style={{ left: `${scrubberPercentage}%` }}
        >
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 -translate-x-[4px] -translate-y-1" />
        </div>
      </div>
    </div>
  );
};
