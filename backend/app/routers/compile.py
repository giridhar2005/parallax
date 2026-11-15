"""Video Expose Compiler Router."""

from __future__ import annotations

from fastapi import APIRouter

from backend.app.models.schemas import ExposeCompileRequest, ExposeCompileResponse
from backend.app.services.compiler import VideoCompiler

router = APIRouter(prefix="/api/compile", tags=["Compiler"])


@router.post("/expose", response_model=ExposeCompileResponse)
async def compile_expose(req: ExposeCompileRequest) -> ExposeCompileResponse:
    """Compile cross-modal contradiction pairs into a deterministic 60fps video expose."""
    return VideoCompiler.compile_expose(req)
