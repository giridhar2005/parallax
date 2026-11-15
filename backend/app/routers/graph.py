"""Bi-Temporal Hypergraph Visualizer Router."""

from __future__ import annotations

from fastapi import APIRouter

from backend.app.models.schemas import BiTemporalHypergraphResponse
from backend.app.services.hypergraph import get_bitemporal_graph

router = APIRouter(prefix="/api/graph", tags=["Hypergraph"])


@router.get("/bitemporal", response_model=BiTemporalHypergraphResponse)
async def query_bitemporal_graph() -> BiTemporalHypergraphResponse:
    """Return unified bi-temporal coordinate points, claims, evidence, and contradiction edges."""
    return get_bitemporal_graph()
