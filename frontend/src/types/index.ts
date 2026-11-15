export interface SystemStatus {
  version: string;
  app_name: string;
  sqlite_wal: string;
  ffmpeg_available: boolean;
  ffmpeg_path: string;
  storage_path: string;
  is_frozen: boolean;
  counts: {
    media_assets?: number;
    claims?: number;
    evidence_nodes?: number;
    contradictions?: number;
  };
}

export interface MediaAsset {
  id: string;
  filename: string;
  file_type: "video" | "pdf" | "audio" | string;
  file_path: string;
  file_size_bytes: number;
  duration_sec?: number;
  page_count?: number;
  sha256_hash: string;
  metadata?: Record<string, any>;
  created_at: string;
}

export interface Claim {
  id: string;
  media_id: string;
  speaker: string;
  statement: string;
  transaction_time_start: number;
  transaction_time_end: number;
  valid_time_start?: string;
  valid_time_end?: string;
  confidence: number;
  created_at: string;
}

export interface EvidenceNode {
  id: string;
  media_id: string;
  evidence_type: "pdf_clause" | "video_frame" | "transcript_segment" | string;
  page_number?: number;
  bounding_box?: [number, number, number, number]; // [x1, y1, x2, y2]
  timecode_sec?: number;
  extracted_text: string;
  valid_time: string;
  metadata?: Record<string, any>;
  created_at: string;
}

export interface Contradiction {
  id: string;
  claim_id: string;
  evidence_id: string;
  nli_score: number;
  nli_label: string;
  contradiction_prob: number;
  entailment_prob: number;
  neutral_prob: number;
  reasoning: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | string;
  status: "DETECTED" | "VERIFIED" | "RESOLVED" | string;
  detected_at: string;
  claim_statement?: string;
  claim_speaker?: string;
  transaction_time_start?: number;
  transaction_time_end?: number;
  valid_time?: string;
  evidence_text?: string;
  evidence_type?: string;
  evidence_page?: number;
  evidence_box?: [number, number, number, number];
}

export interface BiTemporalPoint {
  id: string;
  type: "claim" | "evidence" | "contradiction";
  label: string;
  transaction_time_sec: number;
  valid_time_iso: string;
  score?: number;
  metadata?: Record<string, any>;
}

export interface BiTemporalHypergraph {
  points: BiTemporalPoint[];
  claims: Claim[];
  evidence_nodes: EvidenceNode[];
  contradictions: Contradiction[];
  summary: {
    total_claims: number;
    total_evidence: number;
    total_contradictions: number;
    critical_count: number;
    high_count: number;
    top_nli_score: number;
  };
}

export interface ExposeCompileResult {
  success: boolean;
  export_id: string;
  output_path: string;
  file_size_bytes: number;
  duration_sec: number;
  fps: number;
  contradictions_rendered: number;
  ffmpeg_command: string;
}
