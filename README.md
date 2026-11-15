<div align="center">

# PARALLAX

### Cross-Modal Forensic Video Compiler & Bi-Temporal Hypergraph Engine

[![macOS Apple Silicon](https://img.shields.io/badge/macOS-Apple%20Silicon%20(arm64)-000000?style=for-the-badge&logo=apple&logoColor=white)](https://github.com/giridhar2005/parallax/releases)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQLite WAL](https://img.shields.io/badge/Storage-SQLite%20WAL-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/Frontend-React%2018%20%2B%20TypeScript-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-FAFAFA?style=for-the-badge)](LICENSE)

<br/>

**Parallax** is an investigative intelligence platform and native macOS desktop application designed to detect, cross-examine, and render factual contradictions between spoken oral testimony and documentary proof.

[Download .DMG](#-download-for-macos) • [Architecture](#-system-architecture) • [Developer Quickstart](#-developer-quickstart) • [Makefile](#-makefile-reference)

</div>

---

## ⚡ Download for macOS

Pre-built drag-and-drop macOS disk images are packaged for Apple Silicon (`arm64`):

| Release File | Architecture | Format | Status |
| :--- | :--- | :--- | :--- |
| [**Parallax-v1.0.0-macOS-arm64.dmg**](https://github.com/giridhar2005/parallax/releases/tag/v1.0.0) | Apple Silicon (M1/M2/M3/M4) | Compressed UDZO DMG | [![Release](https://img.shields.io/github/v/release/giridhar2005/parallax?color=10B981&label=latest)](https://github.com/giridhar2005/parallax/releases) |

### Installation Instructions
1. Download **`Parallax-v1.0.0-macOS-arm64.dmg`** from GitHub Releases.
2. Open the disk image and drag **`Parallax.app`** into your **`/Applications`** folder.
3. If macOS Gatekeeper flags the standalone binary on initial launch, clear the quarantine attribute via Terminal:
   ```bash
   xattr -cr /Applications/Parallax.app
   ```

---

## 📐 System Architecture

Parallax models cross-modal evidence through a **Bi-Temporal Hypergraph** that decouples the playback timeline from historical calendar time.

```text
  [ Oral Deposition Video ]               [ Documentary Evidence / PDFs ]
            │                                           │
    (Transaction Time)                           (Valid Time)
   00:01:24.200 (Playback)                     2023-06-18 (Lien Ledger)
            │                                           │
            ▼                                           ▼
   ┌─────────────────┐                         ┌─────────────────┐
   │  Claims Stream  │                         │ Evidence Nodes  │
   │ "Zero transfers │                         │ SWIFT MT103 Ref │
   │  prior to Sept" │                         │ $14.2M Transfer │
   └────────┬────────┘                         └────────┬────────┘
            │                                           │
            └─────────────────┬─────────────────────────┘
                              │
                              ▼
             ┌──────────────────────────────────┐
             │ Cross-Encoder NLI Hunter Engine  │
             │ DeBERTa-v3 Semantic Divergence   │
             │ P(Contradiction) = 0.962         │
             └────────────────┬─────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
  ┌───────────────────────┐       ┌────────────────────────┐
  │ Bi-Temporal Timeline  │       │ Deterministic 60fps    │
  │ Transaction Time (X)  │       │ Video Expose Compiler  │
  │ vs. Valid Time (Y)    │       │ Split-Screen Highlight │
  └───────────────────────┘       └────────────────────────┘
```

### Core Components

1. **Bi-Temporal Hypergraph Topology:**
   - **Transaction Time ($T_x$):** The recording/playback timecode within the media file (e.g. `00:04:12.500`).
   - **Valid Time ($V_t$):** The real-world historical calendar date referenced by the speaker or documentary artifact (e.g. `2023-06-18T16:22:00Z`).
2. **Cross-Encoder NLI Contradiction Hunter:**
   - Evaluates claims against documentary records using natural language inference scoring ($P(\text{Contradiction}) \ge 0.70$).
   - Detects numerical discrepancies, negative universal assertions, and temporal discrepancies.
3. **Deterministic 60fps Video Expose Compiler:**
   - Employs embedded FFmpeg filtergraphs to assemble broadcast-grade split-screen MP4 renders with millisecond timecode burnt-in and glowing bounding-box highlights.
4. **Persistent User State:**
   - In production `.app` bundles, all mutable data (`parallax.db`, `raw/`, `processed/`, `exports/`) resides in `~/Library/Application Support/Parallax/`.

---

## 🖥️ Investigative Workbench

- **Synchronized Dual-Evidence Stage:** Video playback with millisecond timecode on the left; evidentiary PDF preview with glowing red bounding boxes on the right.
- **Bi-Temporal Scrubber:** Interactive horizontal timeline plotting Transaction Time against Valid Time, with clickable contradiction spikes.
- **Native Cocoa WebKit Window:** Zero-flash dark-mode `#09090B` container with native macOS menu integration (`File -> Import Media...`, `Help -> Reveal Data in Finder`).

---

## 🚀 Developer Quickstart

### Prerequisites
- macOS (Apple Silicon or Intel)
- Python $\ge$ 3.11 (Python 3.12 recommended via `uv`)
- Node.js $\ge$ 20 and `npm`
- `ffmpeg` in system PATH

### One-Command Setup & Verification

```bash
# 1. Clone repository
git clone git@github.com:giridhar2005/parallax.git
cd parallax

# 2. Install dependencies (Python virtualenv + Node packages)
make setup

# 3. Seed realistic forensic deposition dataset
make fixture

# 4. Execute test suite (18 tests passing)
make test

# 5. Launch native macOS desktop workbench
make desktop
```

---

## 🛠️ Makefile Reference

| Command | Action |
| :--- | :--- |
| `make setup` | Install Python virtual environment via `uv` and npm packages in `frontend/` |
| `make fixture` | Seed SQLite database with SEC deposition fraud test data |
| `make test` | Run full pytest test suite (18 tests) |
| `make lint` | Run Ruff linter across backend and tests |
| `make desktop` | Run native macOS Cocoa WebKit desktop application |
| `make dev` | Run FastAPI backend server in hot-reload mode on `127.0.0.1:8000` |
| `make frontend-build` | Compile Vite + React production assets into `frontend/dist` |
| `make icon` | Generate multi-resolution `packaging/Parallax.icns` bundle |
| `make app` | Compile standalone `dist/Parallax.app` using PyInstaller |
| `make dmg` | Build drag-to-Applications `release/Parallax-v1.0.0-macOS-arm64.dmg` |
| `make clean` | Remove build caches, temporary SQLite WAL files, and build outputs |

---

## 🔒 Security & Privacy

Parallax executes **100% locally** on your machine:
- No telemetry, third-party analytics, or cloud API dependencies.
- All extracted transcripts, PDF clauses, and hypergraph indices are stored in local SQLite WAL databases.

---

## 📄 License

Parallax is open-source software licensed under the [MIT License](LICENSE).
