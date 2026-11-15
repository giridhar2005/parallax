import React, { useState } from "react";
import { X, Video, CheckCircle2, Copy, Check, ExternalLink } from "lucide-react";
import { ExposeCompileResult } from "../types";

interface ExposeModalProps {
  result: ExposeCompileResult | null;
  onClose: () => void;
}

export const ExposeModal: React.FC<ExposeModalProps> = ({ result, onClose }) => {
  const [copied, setCopied] = useState<boolean>(false);

  if (!result) return null;

  const handleCopyPath = () => {
    navigator.clipboard.writeText(result.output_path);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm select-none">
      <div className="w-full max-w-lg bg-[#111113] border border-[#27272A] rounded shadow-2xl overflow-hidden font-mono text-xs">
        {/* Header */}
        <div className="p-3 border-b border-[#27272A] flex items-center justify-between bg-[#0E0E10]">
          <div className="flex items-center space-x-2 text-zinc-200">
            <Video className="w-4 h-4 text-emerald-400" />
            <span className="font-semibold text-sm">60fps Forensic Expose Compiled</span>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-zinc-500 hover:text-white transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 space-y-4">
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded flex items-center space-x-3 text-emerald-300">
            <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
            <div>
              <div className="font-semibold">Broadcast-Ready Forensic Video Rendered</div>
              <div className="text-[11px] text-zinc-400">
                Split-screen testimony vs documentary proof with burnt-in millisecond timecodes.
              </div>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2 text-center">
            <div className="bg-[#09090B] border border-[#27272A] p-2 rounded">
              <div className="text-[10px] text-zinc-500">Framerate</div>
              <div className="text-zinc-200 font-bold text-sm tabular-nums">{result.fps} FPS</div>
            </div>
            <div className="bg-[#09090B] border border-[#27272A] p-2 rounded">
              <div className="text-[10px] text-zinc-500">Duration</div>
              <div className="text-zinc-200 font-bold text-sm tabular-nums">{result.duration_sec.toFixed(1)}s</div>
            </div>
            <div className="bg-[#09090B] border border-[#27272A] p-2 rounded">
              <div className="text-[10px] text-zinc-500">Contradictions</div>
              <div className="text-rose-400 font-bold text-sm tabular-nums">{result.contradictions_rendered}</div>
            </div>
          </div>

          <div className="space-y-1">
            <div className="text-zinc-400 text-[11px] font-semibold">Output File Path</div>
            <div className="p-2.5 bg-[#09090B] border border-[#27272A] rounded flex items-center justify-between text-zinc-300 font-mono text-[11px] break-all">
              <span className="truncate mr-2">{result.output_path}</span>
              <button
                onClick={handleCopyPath}
                className="flex items-center space-x-1 px-2 py-1 bg-[#18181B] border border-[#27272A] hover:text-white rounded text-zinc-400 transition flex-shrink-0"
              >
                {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                <span>{copied ? "Copied" : "Copy"}</span>
              </button>
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              onClick={onClose}
              className="px-4 py-1.5 rounded bg-zinc-200 text-zinc-950 hover:bg-white font-semibold transition"
            >
              Done
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
