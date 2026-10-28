from requirements_toolkit.requirement import Requirement, RequirementSet, RequirementType
from requirements_toolkit.validation import validate_requirement, validate_requirement_set

def make_req(req_id, statement):
    return Requirement(req_id, "Requirement", statement, RequirementType.FUNCTIONAL)

def test_validation_flags_vague_requirement():
    result = validate_requirement(make_req("REQ-01", "The system shall search quickly."))
    assert result is not None
    assert len(result.issues) > 0

def test_validation_accepts_clear_requirement_or_returns_report():
    result = validate_requirement(make_req("REQ-02", "The system shall display search results within 2 seconds."))
    assert hasattr(result, "issues")

def test_validate_requirement_set_returns_report():
    reqs = RequirementSet("ULMS")
    reqs.add(make_req("REQ-01", "The system shall display search results within 2 seconds."))
    report = validate_requirement_set(reqs)
    assert hasattr(report, "issues")
