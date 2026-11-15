# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller Bundle Specification for Parallax.app (macOS Apple Silicon)."""

import os
import shutil
from pathlib import Path

block_cipher = None

# Resolve project root from SPECPATH
SPEC_DIR = Path(SPECPATH).resolve()
PROJECT_ROOT = SPEC_DIR.parent

# Resolve ffmpeg binary to embed in bundle
ffmpeg_bin = shutil.which("ffmpeg") or str(Path.home() / ".local" / "bin" / "ffmpeg")
binaries = []
if os.path.isfile(ffmpeg_bin) and os.access(ffmpeg_bin, os.X_OK):
    binaries.append((ffmpeg_bin, "."))

datas = [
    (str(PROJECT_ROOT / "frontend" / "dist"), "frontend/dist"),
    (str(PROJECT_ROOT / "backend" / "app" / "db" / "schema.sql"), "backend/app/db"),
    (str(SPEC_DIR / "Parallax.icns"), "packaging"),
]

hiddenimports = [
    "uvicorn",
    "uvicorn.config",
    "uvicorn.main",
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.loops.asyncio",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.http.h11_impl",
    "uvicorn.protocols.http.httptools_impl",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespans",
    "uvicorn.lifespans.auto",
    "uvicorn.lifespans.on",
    "fastapi",
    "starlette",
    "starlette.routing",
    "starlette.responses",
    "starlette.staticfiles",
    "pydantic",
    "pydantic.deprecated.decorator",
    "webview",
    "webview.platforms.cocoa",
    "sqlite3",
    "aiofiles",
    "multipart",
    "PIL",
]

a = Analysis(
    [str(PROJECT_ROOT / "backend" / "desktop.py")],
    pathex=[str(PROJECT_ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "notebook"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Parallax",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch="arm64",
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Parallax",
)

app = BUNDLE(
    coll,
    name="Parallax.app",
    icon=str(SPEC_DIR / "Parallax.icns"),
    bundle_identifier="com.giridhar.parallax",
    info_plist={
        "CFBundleName": "Parallax",
        "CFBundleDisplayName": "Parallax",
        "CFBundleIdentifier": "com.giridhar.parallax",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "12.0",
        "NSRequiresAquaSystemAppearance": False,
        "NSHumanReadableCopyright": "Copyright © 2026 Giridhar. MIT License.",
        "NSMicrophoneUsageDescription": "Parallax processes audio for cross-modal testimony contradiction detection.",
    },
)
