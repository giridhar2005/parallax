import React, { useState, useEffect } from "react";
import { useForensics } from "./hooks/useForensics";
import { TopCommandBar } from "./components/TopCommandBar";
import { DualEvidenceStage } from "./components/DualEvidenceStage";
import { BiTemporalTimeline } from "./components/BiTemporalTimeline";
import { ImportModal } from "./components/ImportModal";
import { ExposeModal } from "./components/ExposeModal";
import { ExposeCompileResult } from "./types";

export const App: React.FC = () => {
  const {
    status,
    contradictions,
    activeContradiction,
    currentTimeSec,
    isPlaying,
    loading,
    isHunting,
    isCompiling,
    setIsPlaying,
    seekTo,
    selectContradiction,
    runHunt,
    compileExpose,
    importFile,
  } = useForensics();

  const [isImportOpen, setIsImportOpen] = useState<boolean>(false);
  const [exposeResult, setExposeResult] = useState<ExposeCompileResult | null>(null);

  // Native macOS Custom Event Listener from pywebview Menu Actions
  useEffect(() => {
    const handleOpenImport = () => setIsImportOpen(true);
    window.addEventListener("parallax:open-import", handleOpenImport);
    return () => window.removeEventListener("parallax:open-import", handleOpenImport);
  }, []);

  // Global Keyboard Navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

      if (e.code === "Space") {
        e.preventDefault();
        setIsPlaying((p) => !p);
      } else if (e.key === "ArrowLeft") {
        seekTo(Math.max(0, currentTimeSec - 5));
      } else if (e.key === "ArrowRight") {
        seekTo(currentTimeSec + 5);
      } else if (["1", "2", "3", "4"].includes(e.key)) {
        const idx = parseInt(e.key, 10) - 1;
        if (contradictions[idx]) {
          selectContradiction(contradictions[idx]);
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [currentTimeSec, contradictions, seekTo, selectContradiction, setIsPlaying]);

  const handleCompile = async () => {
    try {
      const res = await compileExpose();
      setExposeResult(res);
    } catch {
      alert("Failed to compile 60fps expose video.");
    }
  };

  return (
    <div className="h-screen w-screen bg-[#09090B] text-zinc-100 flex flex-col font-sans select-none overflow-hidden">
      {/* 1. Top Command Bar */}
      <TopCommandBar
        status={status}
        onOpenImport={() => setIsImportOpen(true)}
        onRunHunt={runHunt}
        onCompileExpose={handleCompile}
        isHunting={isHunting}
        isCompiling={isCompiling}
      />

      {/* 2. Synchronized Dual-Evidence Center Stage */}
      <DualEvidenceStage
        currentTimeSec={currentTimeSec}
        isPlaying={isPlaying}
        onTogglePlay={() => setIsPlaying((p) => !p)}
        onSeek={seekTo}
        activeContradiction={activeContradiction}
      />

      {/* 3. Bi-Temporal Hypergraph Timeline Scrubber */}
      <BiTemporalTimeline
        currentTimeSec={currentTimeSec}
        totalDurationSec={724.5}
        contradictions={contradictions}
        activeContradiction={activeContradiction}
        onSeek={seekTo}
        onSelectContradiction={selectContradiction}
      />

      {/* Import Modal */}
      <ImportModal
        isOpen={isImportOpen}
        onClose={() => setIsImportOpen(false)}
        onImport={importFile}
      />

      {/* 60fps Expose Compilation Modal */}
      <ExposeModal
        result={exposeResult}
        onClose={() => setExposeResult(null)}
      />
    </div>
  );
};
