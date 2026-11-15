"""Tests for Cross-Encoder NLI Contradiction Hunter."""

from backend.app.services.nli import NLIHunter


def test_nli_score_explicit_contradiction():
    """Universal negative claim vs positive wire transfer must trigger high contradiction score."""
    hypothesis = "At no point did Apex transfer any capital to offshore Cayman subsidiaries."
    premise = "Outbound wire USD 14,200,000.00 from Apex to Apex Cayman Holdings Ltd."

    score_result = NLIHunter.score_pair(premise=premise, hypothesis=hypothesis)
    assert score_result["nli_score"] >= 0.70
    assert score_result["nli_label"] == "CONTRADICTION"
    assert "universal negative" in score_result["reasoning"].lower()


def test_nli_score_entailment_or_neutral():
    """Consistent statements should not flag contradiction."""
    hypothesis = "We maintained ongoing operations in North America."
    premise = "Apex logistics operations continued across standard domestic shipping corridors."

    score_result = NLIHunter.score_pair(premise=premise, hypothesis=hypothesis)
    assert score_result["nli_score"] < 0.70
    assert score_result["nli_label"] != "CONTRADICTION"


def test_nli_hunt_execution(temp_storage):
    """Hunter execution should scan unlinked records and commit contradictions."""
    res = NLIHunter.run_hunt()
    assert "status" in res
    assert res["status"] == "completed"
