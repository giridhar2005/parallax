import React from "react";
import { VideoClaimPane } from "./VideoClaimPane";
import { ProofInspectorPane } from "./ProofInspectorPane";
import { Contradiction } from "../types";

interface DualEvidenceStageProps {
  currentTimeSec: number;
  isPlaying: boolean;
  onTogglePlay: () => void;
  onSeek: (sec: number) => void;
  activeContradiction: Contradiction | null;
}

export const DualEvidenceStage: React.FC<DualEvidenceStageProps> = ({
  currentTimeSec,
  isPlaying,
  onTogglePlay,
  onSeek,
  activeContradiction,
}) => {
  return (
    <div className="flex-1 grid grid-cols-1 md:grid-cols-2 border-b border-[#27272A] overflow-hidden min-h-[480px]">
      {/* Left Pane: Claim Stream & Timecode Video Player */}
      <VideoClaimPane
        currentTimeSec={currentTimeSec}
        isPlaying={isPlaying}
        onTogglePlay={onTogglePlay}
        onSeek={onSeek}
        activeContradiction={activeContradiction}
      />

      {/* Right Pane: Contradiction Proof Document with Glowing SVG Box */}
      <ProofInspectorPane contradiction={activeContradiction} />
    </div>
  );
};
