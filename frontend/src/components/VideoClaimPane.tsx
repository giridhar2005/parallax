import React from "react";
import {
  Play,
  Pause,
  RotateCcw,
  SkipBack,
  SkipForward,
  Volume2,
  User,
  Clock,
} from "lucide-react";
import { Contradiction } from "../types";

interface VideoClaimPaneProps {
  currentTimeSec: number;
  isPlaying: boolean;
  onTogglePlay: () => void;
  onSeek: (sec: number) => void;
  activeContradiction: Contradiction | null;
}

export const VideoClaimPane: React.FC<VideoClaimPaneProps> = ({
  currentTimeSec,
  isPlaying,
  onTogglePlay,
  onSeek,
  activeContradiction,
}) => {
  const formatTimecode = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    const ms = Math.floor((seconds % 1) * 1000);
    return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}.${String(ms).padStart(3, "0")}`;
  };

  // Sample transcript segments for Marcus Vance
  const TRANSCRIPTS = [
    {
      time: 84.2,
      speaker: "Marcus Vance (CEO)",
      text: "At no point prior to September 15, 2023, did Apex Global transfer any corporate capital to offshore Cayman subsidiaries or Cayman accounts.",
      isContradiction: true,
      id: "contra_01",
    },
    {
      time: 142.0,
      speaker: "Marcus Vance (CEO)",
      text: "We maintained all routine operating accounts strictly within domestic banking networks, in full compliance with Delaware covenants.",
      isContradiction: false,
    },
    {
      time: 218.4,
      speaker: "Marcus Vance (CEO)",
      text: "Our total unencumbered liquidity at the close of Q2 was well above forty million dollars, with zero outstanding third-party liens.",
      isContradiction: true,
      id: "contra_02",
    },
    {
      time: 320.0,
      speaker: "Special Counsel",
      text: "Mr. Vance, let me direct your attention to the audited debt schedules submitted under Exhibit C.",
      isContradiction: false,
    },
    {
      time: 412.5,
      speaker: "Marcus Vance (CEO)",
      text: "The maritime fleet lease agreement was renewed on standard terms in July, without granting any senior collateral pledges to lenders.",
      isContradiction: true,
      id: "contra_03",
    },
  ];

  return (
    <div className="flex-1 flex flex-col bg-[#09090B] border-r border-[#27272A] overflow-hidden">
      {/* Pane Header */}
      <div className="h-9 px-3 border-b border-[#27272A] bg-[#0E0E10] flex items-center justify-between text-xs font-mono text-zinc-400">
        <div className="flex items-center space-x-2">
          <span className="w-1.5 h-1.5 rounded-full bg-rose-500" />
          <span className="font-semibold text-zinc-300">CLAIM STREAM (ORAL TESTIMONY)</span>
        </div>
        <div className="flex items-center space-x-2 text-[11px] text-zinc-500">
          <span>SOURCE: APEX_CEO_DEPOSITION.MP4</span>
          <span>·</span>
          <span className="text-emerald-400">60 FPS</span>
        </div>
      </div>

      {/* Video Viewport Stage */}
      <div className="relative aspect-video bg-[#000000] border-b border-[#27272A] flex items-center justify-center overflow-hidden">
        {/* Simulated Deposition Video Stream with Forensic CRT Overlay */}
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-gradient-to-b from-[#18181B]/40 to-[#09090B]">
          <div className="w-24 h-24 rounded-full border border-zinc-700/60 bg-zinc-900/80 flex items-center justify-center text-zinc-400 mb-2">
            <User className="w-12 h-12 text-zinc-500" />
          </div>
          <div className="text-xs font-mono font-semibold text-zinc-200">
            MARCUS VANCE — CEO, APEX GLOBAL LOGISTICS
          </div>
          <div className="text-[11px] font-mono text-zinc-500">
            U.S. DISTRICT COURT DEPOSITION · SESSION 3
          </div>
        </div>

        {/* Burned-in Millisecond Timecode HUD Overlay (Top-Left) */}
        <div className="absolute top-3 left-3 bg-[#09090B]/85 border border-[#27272A] px-2.5 py-1 rounded text-xs font-mono font-semibold text-emerald-400 tabular-nums">
          TC: {formatTimecode(currentTimeSec)}
        </div>

        {/* Forensic Contradiction Banner (Top-Right if active) */}
        {activeContradiction && (
          <div className="absolute top-3 right-3 bg-rose-500/20 border border-rose-500/50 px-2.5 py-1 rounded text-xs font-mono font-semibold text-rose-300 animate-pulse">
            CONTRADICTION DETECTED: {activeContradiction.nli_score.toFixed(2)}
          </div>
        )}

        {/* Live Audio Waveform Simulation Bar (Bottom Overlay) */}
        <div className="absolute bottom-2 inset-x-3 h-6 bg-[#09090B]/70 backdrop-blur rounded flex items-center px-2 space-x-1 border border-[#27272A]/60">
          <Volume2 className="w-3.5 h-3.5 text-zinc-400 mr-1" />
          {Array.from({ length: 48 }).map((_, i) => {
            const h = Math.abs(Math.sin(i * 0.4 + currentTimeSec * 2)) * 14 + 2;
            return (
              <div
                key={i}
                className="flex-1 bg-zinc-600 rounded-full transition-all duration-75"
                style={{
                  height: `${h}px`,
                  backgroundColor: h > 10 ? "#EF4444" : h > 6 ? "#10B981" : "#52525B",
                }}
              />
            );
          })}
        </div>
      </div>

      {/* Media Playback Transport Bar */}
      <div className="h-10 px-3 bg-[#111113] border-b border-[#27272A] flex items-center justify-between text-xs font-mono">
        <div className="flex items-center space-x-1">
          <button
            onClick={() => onSeek(Math.max(0, currentTimeSec - 5))}
            className="p-1 rounded text-zinc-400 hover:text-white hover:bg-zinc-800 transition"
            title="Rewind 5s"
          >
            <SkipBack className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={onTogglePlay}
            className="p-1.5 rounded bg-zinc-200 text-zinc-950 hover:bg-white transition"
          >
            {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
          </button>
          <button
            onClick={() => onSeek(currentTimeSec + 5)}
            className="p-1 rounded text-zinc-400 hover:text-white hover:bg-zinc-800 transition"
            title="Forward 5s"
          >
            <SkipForward className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => onSeek(0)}
            className="p-1 rounded text-zinc-400 hover:text-white hover:bg-zinc-800 transition"
            title="Restart"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="text-zinc-400 tabular-nums">
          <span className="text-zinc-200 font-semibold">{formatTimecode(currentTimeSec)}</span> / 12:04.500
        </div>
      </div>

      {/* Synchronized Transcript Stage */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2 bg-[#09090B]">
        <div className="text-[11px] font-mono text-zinc-500 uppercase tracking-wider mb-1 flex items-center justify-between">
          <span>Synchronized Oral Testimony Transcript</span>
          <span>Click timestamp to seek</span>
        </div>

        {TRANSCRIPTS.map((t, idx) => {
          const isActive = Math.abs(currentTimeSec - t.time) < 15.0;
          return (
            <div
              key={idx}
              onClick={() => onSeek(t.time)}
              className={`p-2.5 rounded border text-xs font-mono transition cursor-pointer ${
                isActive
                  ? "bg-[#18181B] border-amber-500/50 shadow-sm"
                  : "bg-[#111113] border-[#27272A] hover:border-zinc-600 text-zinc-400"
              }`}
            >
              <div className="flex items-center justify-between mb-1 text-[11px]">
                <div className="flex items-center space-x-1.5 font-semibold text-zinc-300">
                  <User className="w-3 h-3 text-zinc-500" />
                  <span>{t.speaker}</span>
                </div>
                <div className="flex items-center space-x-2">
                  {t.isContradiction && (
                    <span className="px-1.5 py-0.2 rounded bg-rose-500/20 text-rose-400 border border-rose-500/40 text-[10px] font-semibold">
                      CONFLICT SPIKE
                    </span>
                  )}
                  <span className="text-zinc-500 tabular-nums flex items-center space-x-1">
                    <Clock className="w-2.5 h-2.5" />
                    <span>{formatTimecode(t.time)}</span>
                  </span>
                </div>
              </div>
              <p className={`leading-relaxed ${isActive ? "text-zinc-100" : "text-zinc-300"}`}>
                "{t.text}"
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
