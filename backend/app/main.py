"""Parallax FastAPI Application Entrypoint.

Provides unified REST APIs, Bi-Temporal Hypergraph engine, and static SPA serving
optimized for native macOS Cocoa WebKit execution inside Parallax.app.
"""

from __future__ import annotations

import contextlib
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.db.database import check_wal_status, get_db, init_db
from backend.app.routers import analysis, compile, graph, media, system
from backend.app.services.fixtures import seed_fixtures

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("parallax")


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and seed baseline dataset if empty."""
    logger.info(f"Initializing Parallax SQLite database at: {settings.db_path}")
    init_db()

    # If first boot, seed realistic deposition fraud fixtures
    try:
        with get_db() as conn:
            cnt = conn.execute("SELECT COUNT(*) FROM claims").fetchone()[0]
            if cnt == 0:
                logger.info("Empty database detected: Auto-seeding initial forensic investigation fixtures...")
                seed_fixtures()
    except Exception as e:
        logger.warning(f"Auto-seed check: {e}")

    yield
    logger.info("Parallax backend shutting down.")


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title="Parallax",
        description="Cross-Modal Forensic Video Compiler & Bi-Temporal Hypergraph Engine",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Healthcheck probe for desktop window readiness
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {
            "status": "ok",
            "app": "Parallax",
            "version": "1.0.0",
            "wal": check_wal_status(),
        }

    # Include API sub-routers
    app.include_router(system.router)
    app.include_router(media.router)
    app.include_router(analysis.router)
    app.include_router(graph.router)
    app.include_router(compile.router)

    # Resolve static frontend distribution
    dist_dir = settings.get_frontend_dist_dir()
    if dist_dir and (dist_dir / "index.html").is_file():
        logger.info(f"Mounting compiled React frontend from: {dist_dir}")
        assets_dir = dist_dir / "assets"
        if assets_dir.is_dir():
            app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

        @app.get("/{full_path:path}", response_class=HTMLResponse, include_in_schema=False)
        async def serve_spa(full_path: str):
            # If path points to an actual file in dist, return it
            requested = dist_dir / full_path
            if requested.is_file():
                return FileResponse(requested)
            # SPA fallback: return index.html
            return FileResponse(dist_dir / "index.html")
    else:
        logger.info("Compiled frontend/dist not found; mounting fallback dashboard page.")

        @app.get("/", response_class=HTMLResponse, include_in_schema=False)
        async def fallback_landing():
            return HTMLResponse(
                content="""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <title>Parallax — Forensic Video Compiler</title>
                    <style>
                        body { background: #09090B; color: #FAFAFA; font-family: -apple-system, monospace; padding: 40px; }
                        h1 { font-size: 20px; font-weight: 600; letter-spacing: -0.02em; }
                        p { color: #A1A1AA; font-size: 13px; line-height: 1.6; }
                        .pill { display: inline-block; padding: 4px 10px; background: #111113; border: 1px solid #27272A; border-radius: 4px; font-size: 12px; color: #10B981; }
                    </style>
                </head>
                <body>
                    <h1>Parallax Engine Online</h1>
                    <div class="pill">SQLITE WAL: ACTIVE</div>
                    <p>API is active. Compile the React frontend with <code>npm run build</code> in <code>frontend/</code> to load the interactive desktop workbench.</p>
                </body>
                </html>
                """
            )

    return app


app = create_app()


def run_server(host: str = "127.0.0.1", port: int = 8000):
    """CLI entrypoint for standalone server mode."""
    import uvicorn
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    run_server()
