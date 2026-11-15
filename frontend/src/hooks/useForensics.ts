import { useState, useEffect, useCallback } from "react";
import {
  SystemStatus,
  MediaAsset,
  Contradiction,
  BiTemporalHypergraph,
  ExposeCompileResult,
} from "../types";

export function useForensics() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [mediaList, setMediaList] = useState<MediaAsset[]>([]);
  const [contradictions, setContradictions] = useState<Contradiction[]>([]);
  const [graph, setGraph] = useState<BiTemporalHypergraph | null>(null);
  const [activeContradiction, setActiveContradiction] = useState<Contradiction | null>(null);

  // Playback & Scrubber State
  const [currentTimeSec, setCurrentTimeSec] = useState<number>(84.2);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [isHunting, setIsHunting] = useState<boolean>(false);
  const [isCompiling, setIsCompiling] = useState<boolean>(false);

  const fetchData = useCallback(async () => {
    try {
      const [statusRes, mediaRes, contraRes, graphRes] = await Promise.all([
        fetch("/api/system/status").then((r) => r.json()),
        fetch("/api/media/list").then((r) => r.json()),
        fetch("/api/analysis/contradictions").then((r) => r.json()),
        fetch("/api/graph/bitemporal").then((r) => r.json()),
      ]);

      setStatus(statusRes);
      setMediaList(mediaRes || []);
      setContradictions(contraRes || []);
      setGraph(graphRes);

      if (contraRes && contraRes.length > 0 && !activeContradiction) {
        setActiveContradiction(contraRes[0]);
        if (contraRes[0].transaction_time_start) {
          setCurrentTimeSec(contraRes[0].transaction_time_start);
        }
      }
    } catch (err) {
      console.error("Forensics data fetch failed:", err);
    } finally {
      setLoading(false);
    }
  }, [activeContradiction]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Video playback ticker
  useEffect(() => {
    if (!isPlaying) return;
    const interval = setInterval(() => {
      setCurrentTimeSec((prev) => {
        if (prev >= 720.0) {
          setIsPlaying(false);
          return 0.0;
        }
        return Number((prev + 0.1).toFixed(2));
      });
    }, 100);
    return () => clearInterval(interval);
  }, [isPlaying]);

  const selectContradiction = useCallback((c: Contradiction) => {
    setActiveContradiction(c);
    if (c.transaction_time_start !== undefined) {
      setCurrentTimeSec(c.transaction_time_start);
    }
  }, []);

  const seekTo = useCallback((seconds: number) => {
    setCurrentTimeSec(Number(seconds.toFixed(2)));
    // Find closest contradiction if any
    const match = contradictions.find(
      (c) =>
        c.transaction_time_start !== undefined &&
        Math.abs(c.transaction_time_start - seconds) < 20.0
    );
    if (match) {
      setActiveContradiction(match);
    }
  }, [contradictions]);

  const runHunt = async () => {
    setIsHunting(true);
    try {
      await fetch("/api/analysis/hunt", { method: "POST" });
      await fetchData();
    } catch (err) {
      console.error("NLI hunt failed:", err);
    } finally {
      setIsHunting(false);
    }
  };

  const compileExpose = async (): Promise<ExposeCompileResult> => {
    setIsCompiling(true);
    try {
      const res = await fetch("/api/compile/expose", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          fps: 60,
          resolution: "1920x1080",
          split_screen_layout: "side_by_side",
        }),
      });
      return await res.json();
    } finally {
      setIsCompiling(false);
    }
  };

  const importFile = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch("/api/media/import", {
      method: "POST",
      body: formData,
    });
    if (!res.ok) throw new Error("Upload failed");
    await fetchData();
  };

  return {
    status,
    mediaList,
    contradictions,
    graph,
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
    refresh: fetchData,
  };
}
