import React from "react";
import {
  Crosshair,
  Database,
  Cpu,
  Upload,
  Search,
  Video,
  Loader2,
  HardDrive,
} from "lucide-react";
import { SystemStatus } from "../types";

interface TopCommandBarProps {
  status: SystemStatus | null;
  onOpenImport: () => void;
  onRunHunt: () => void;
  onCompileExpose: () => void;
  isHunting: boolean;
  isCompiling: boolean;
}

export const TopCommandBar: React.FC<TopCommandBarProps> = ({
  status,
  onOpenImport,
  onRunHunt,
  onCompileExpose,
  isHunting,
  isCompiling,
}) => {
  return (
    <header className="h-14 border-b border-[#27272A] bg-[#09090B] px-4 flex items-center justify-between select-none">
      {/* Brand & Forensic Tag */}
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 rounded bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-500">
          <Crosshair className="w-4 h-4 animate-pulse" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className="font-mono font-bold tracking-wider text-sm text-zinc-100">
              PARALLAX
            </span>
            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700">
              v1.0.0 · macOS arm64
            </span>
          </div>
          <p className="text-[10px] font-mono text-zinc-500 leading-none">
            Cross-Modal Forensic Video Compiler
          </p>
        </div>
      </div>

      {/* Center Telemetry Badges */}
      <div className="hidden lg:flex items-center space-x-3 text-xs font-mono">
        {/* SQLite WAL indicator */}
        <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded bg-[#111113] border border-[#27272A] text-zinc-300">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <Database className="w-3.5 h-3.5 text-zinc-400" />
          <span>SQLITE WAL:</span>
          <span className="text-emerald-400 font-semibold">{status?.sqlite_wal || "ACTIVE"}</span>
        </div>

        {/* FFmpeg Engine */}
        <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded bg-[#111113] border border-[#27272A] text-zinc-300">
          <Cpu className="w-3.5 h-3.5 text-blue-400" />
          <span>ENGINE:</span>
          <span className="text-blue-300 font-semibold">FFMPEG 60FPS</span>
        </div>

        {/* Storage Location Badge */}
        <div
          title={status?.storage_path || ""}
          className="flex items-center space-x-1.5 px-2.5 py-1 rounded bg-[#111113] border border-[#27272A] text-zinc-400 max-w-xs truncate"
        >
          <HardDrive className="w-3.5 h-3.5 text-zinc-500" />
          <span className="truncate">
            {status?.is_frozen ? "~/Library/Application Support/Parallax" : "Local ./data"}
          </span>
        </div>
      </div>

      {/* Primary Action Triggers */}
      <div className="flex items-center space-x-2 text-xs font-mono">
        {/* Import Media Button */}
        <button
          onClick={onOpenImport}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-[#111113] border border-[#27272A] text-zinc-200 hover:text-white hover:border-zinc-500 transition active:scale-95"
        >
          <Upload className="w-3.5 h-3.5 text-zinc-400" />
          <span>+ Import Media</span>
        </button>

        {/* Run Contradiction Hunt */}
        <button
          onClick={onRunHunt}
          disabled={isHunting}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-[#18181B] border border-amber-500/40 text-amber-300 hover:bg-amber-500/10 hover:border-amber-400 transition active:scale-95 disabled:opacity-50"
        >
          {isHunting ? (
            <Loader2 className="w-3.5 h-3.5 animate-spin text-amber-400" />
          ) : (
            <Search className="w-3.5 h-3.5 text-amber-400" />
          )}
          <span>{isHunting ? "Hunting..." : "Hunt Contradictions"}</span>
        </button>

        {/* Compile 60fps Expose */}
        <button
          onClick={onCompileExpose}
          disabled={isCompiling}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-rose-500 hover:bg-rose-600 text-white font-semibold transition shadow-sm active:scale-95 disabled:opacity-50"
        >
          {isCompiling ? (
            <Loader2 className="w-3.5 h-3.5 animate-spin" />
          ) : (
            <Video className="w-3.5 h-3.5" />
          )}
          <span>{isCompiling ? "Compiling..." : "Compile 60fps Expose"}</span>
        </button>
      </div>
    </header>
  );
};
