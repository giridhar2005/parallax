"""Parallax Desktop Native macOS Cocoa WebKit Window Entrypoint.

Starts embedded FastAPI backend on a dynamic localhost port, polls readiness,
and launches pywebview desktop window with custom menus and zero-flash dark canvas.
"""

from __future__ import annotations

import logging
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from typing import Optional

import uvicorn
import webview
import webview.menu as wm

from backend.app.config import settings

logger = logging.getLogger("parallax.desktop")


def get_free_port() -> int:
    """Allocate a free TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for_server(url: str, timeout_sec: float = 10.0) -> bool:
    """Poll healthcheck endpoint until the backend server is ready."""
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{url}/health", timeout=1.0) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.1)
    return False


def open_data_folder():
    """Reveal user storage directory in macOS Finder."""
    try:
        subprocess.run(["open", str(settings.storage_root)], check=False)
    except Exception as e:
        logger.error(f"Failed to open storage directory: {e}")


def main():
    """Launch the Parallax macOS desktop application."""
    port = get_free_port()
    base_url = f"http://127.0.0.1:{port}"

    # Start Uvicorn ASGI server in a background daemon thread
    server_config = uvicorn.Config(
        "backend.app.main:app",
        host="127.0.0.1",
        port=port,
        log_level="warning",
        access_log=False,
    )
    server = uvicorn.Server(server_config)
    server_thread = threading.Thread(target=server.run, daemon=True, name="ParallaxBackendThread")
    server_thread.start()

    # Wait for server readiness
    if not wait_for_server(base_url, timeout_sec=10.0):
        logger.error("FastAPI backend failed to start within 10s timeout.")
        sys.exit(1)

    logger.info(f"Parallax backend online at {base_url}. Spawning native macOS window...")

    # Window reference placeholder
    window_ref: list[Optional[webview.Window]] = [None]

    def reload_workbench():
        if window_ref[0]:
            window_ref[0].load_url(base_url)

    def trigger_import_modal():
        if window_ref[0]:
            window_ref[0].evaluate_js("window.dispatchEvent(new CustomEvent('parallax:open-import'))")

    # Native macOS Menus
    file_menu = wm.Menu(
        "File",
        [
            wm.MenuAction("Import Media...", trigger_import_modal),
            wm.MenuSeparator(),
            wm.MenuAction("Reveal Data in Finder", open_data_folder),
        ],
    )
    view_menu = wm.Menu(
        "View",
        [
            wm.MenuAction("Reload Workbench", reload_workbench),
        ],
    )
    help_menu = wm.Menu(
        "Help",
        [
            wm.MenuAction("Open Application Support Storage", open_data_folder),
        ],
    )

    # Launch native Cocoa WebKit window
    window = webview.create_window(
        title="Parallax — Cross-Modal Forensic Video Compiler",
        url=base_url,
        width=1440,
        height=900,
        min_size=(1024, 700),
        background_color="#09090B",
        text_select=True,
    )
    window_ref[0] = window

    try:
        webview.start(menu=[file_menu, view_menu, help_menu], debug=False)
    except Exception as e:
        # Fallback without custom menus if pywebview menu binding raises on headless/sandbox
        logger.warning(f"Starting window without custom menus due to: {e}")
        webview.start(debug=False)


if __name__ == "__main__":
    main()
