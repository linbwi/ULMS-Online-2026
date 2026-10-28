import pytest
from requirements_toolkit.elicitation import ElicitationFinding, ElicitationMethod, ElicitationSession, ElicitationSessionSet, FindingType

def make_session(sid="ES-01"):
    finding = ElicitationFinding("F-01", "Students want filters by author.", FindingType.NEED, source="Student interview")
    return ElicitationSession(session_id=sid, title="Student interview",
        method=ElicitationMethod.INTERVIEW, objective="Understand book search needs",
        participants=["Student"], findings=[finding])

def test_finding_requires_id_and_description():
    with pytest.raises(ValueError):
        ElicitationFinding("", "A finding")

def test_session_records_method_and_findings():
    session = make_session()
    assert session.method == ElicitationMethod.INTERVIEW
    assert len(session.findings) == 1

def test_session_set_rejects_duplicate_ids():
    sessions = ElicitationSessionSet("ULMS elicitation")
    sessions.add(make_session())
    with pytest.raises(ValueError):
        sessions.add(make_session())
