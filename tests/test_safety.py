from requirements_toolkit.safety import Hazard, HazardCategory, RiskSeverity, RiskLikelihood, HazardSet

def test_hazard_normalizes_and_stores_risk_fields():
    hazard = Hazard("HZ-01", "Unauthorized access", "A user accesses another user's loan history.",
        category=HazardCategory.UNAUTHORIZED_ACCESS,
        severity=RiskSeverity.MAJOR, likelihood=RiskLikelihood.POSSIBLE)
    assert hazard.hazard_id == "HZ-01"
    assert hazard.severity == RiskSeverity.MAJOR

def test_hazard_preserves_related_requirement_ids_as_provided():
    hazard = Hazard("HZ-02", "Data loss", "Loan records may be lost.",
        affected_requirement_ids=[" req-01 ", "REQ-01", "REQ-02"])
    assert hazard.affected_requirement_ids == ["req-01", "REQ-01", "REQ-02"]

def test_hazard_set_stores_hazards():
    group = HazardSet("ULMS hazards")
    group.add(Hazard("HZ-01", "Data loss", "Digital book metadata may be lost."))
    assert len(group.hazards) == 1
