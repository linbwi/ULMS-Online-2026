import pytest
from requirements_toolkit.traceability import TraceabilityLink, TraceabilityType, TraceabilityMatrix

def test_traceability_link_normalizes_ids():
    link = TraceabilityLink(" req-01 ", " uc-01 ", TraceabilityType.REQUIREMENT_TO_USE_CASE)
    assert link.source_id == "REQ-01"
    assert link.target_id == "UC-01"

def test_traceability_link_rejects_empty_endpoint():
    with pytest.raises(ValueError):
        TraceabilityLink("", "UC-01", TraceabilityType.REQUIREMENT_TO_USE_CASE)

def test_traceability_matrix_stores_links():
    link = TraceabilityLink("REQ-01", "UC-01", TraceabilityType.REQUIREMENT_TO_USE_CASE)
    matrix = TraceabilityMatrix("ULMS traceability", [link])
    assert len(matrix.links) == 1
