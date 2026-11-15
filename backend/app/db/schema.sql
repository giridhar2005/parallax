-- Parallax Forensic Engine: Bi-Temporal Hypergraph Schema (SQLite WAL)

PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;

-- Media Assets (Video, Audio, PDF evidence documents)
CREATE TABLE IF NOT EXISTS media_assets (
    id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL CHECK(file_type IN ('video', 'pdf', 'audio')),
    file_path TEXT NOT NULL,
    file_size_bytes INTEGER NOT NULL,
    duration_sec REAL,
    page_count INTEGER,
    sha256_hash TEXT NOT NULL,
    metadata JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Claims Extracted from Oral Testimony / Video Stream
CREATE TABLE IF NOT EXISTS claims (
    id TEXT PRIMARY KEY,
    media_id TEXT NOT NULL REFERENCES media_assets(id) ON DELETE CASCADE,
    speaker TEXT NOT NULL DEFAULT 'Subject',
    statement TEXT NOT NULL,
    transaction_time_start REAL NOT NULL, -- Media playback timestamp (sec)
    transaction_time_end REAL NOT NULL,
    valid_time_start TEXT,               -- Real-world historical date/event referenced (ISO-8601)
    valid_time_end TEXT,
    confidence REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Concrete Evidence Nodes (PDF clauses with coordinates, video physical frames)
CREATE TABLE IF NOT EXISTS evidence_nodes (
    id TEXT PRIMARY KEY,
    media_id TEXT NOT NULL REFERENCES media_assets(id) ON DELETE CASCADE,
    evidence_type TEXT NOT NULL CHECK(evidence_type IN ('pdf_clause', 'video_frame', 'transcript_segment')),
    page_number INTEGER,
    bounding_box JSON,                  -- [x1, y1, x2, y2] normalized (0.0 - 1.0) or pixel
    timecode_sec REAL,
    extracted_text TEXT NOT NULL,
    valid_time TEXT NOT NULL,           -- Timestamp of document creation/validity
    metadata JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cross-Modal Contradiction Edges in the Hypergraph
CREATE TABLE IF NOT EXISTS contradictions (
    id TEXT PRIMARY KEY,
    claim_id TEXT NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    evidence_id TEXT NOT NULL REFERENCES evidence_nodes(id) ON DELETE CASCADE,
    nli_score REAL NOT NULL,            -- e.g. 0.94
    nli_label TEXT NOT NULL DEFAULT 'CONTRADICTION',
    contradiction_prob REAL NOT NULL DEFAULT 0.94,
    entailment_prob REAL NOT NULL DEFAULT 0.03,
    neutral_prob REAL NOT NULL DEFAULT 0.03,
    reasoning TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'CRITICAL' CHECK(severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
    status TEXT NOT NULL DEFAULT 'DETECTED' CHECK(status IN ('DETECTED', 'VERIFIED', 'RESOLVED')),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full-Text Search Indexes
CREATE INDEX IF NOT EXISTS idx_claims_media ON claims(media_id);
CREATE INDEX IF NOT EXISTS idx_claims_tx_time ON claims(transaction_time_start, transaction_time_end);
CREATE INDEX IF NOT EXISTS idx_evidence_media ON evidence_nodes(media_id);
CREATE INDEX IF NOT EXISTS idx_contradictions_claim ON contradictions(claim_id);
CREATE INDEX IF NOT EXISTS idx_contradictions_evidence ON contradictions(evidence_id);
CREATE INDEX IF NOT EXISTS idx_contradictions_score ON contradictions(nli_score DESC);
