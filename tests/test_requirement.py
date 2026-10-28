import pytest
from requirements_toolkit.requirement import Requirement, RequirementSet, RequirementType, Priority

def make_req(req_id="REQ-01", statement="The system shall allow students to search books."):
    return Requirement(req_id, "Search books", statement, RequirementType.FUNCTIONAL, Priority.MUST)

def test_requirement_normalizes_id_and_text():
    req = make_req(" req-01 ")
    assert req.req_id == "REQ-01"
    assert req.title == "Search books"

def test_requirement_rejects_empty_id():
    with pytest.raises(ValueError):
        make_req(" ")

def test_requirement_set_adds_and_retrieves_requirements():
    req_set = RequirementSet("ULMS")
    req = make_req()
    req_set.add(req)
    assert len(req_set.requirements) == 1
    assert req_set.requirements[0].req_id == "REQ-01"

def test_requirement_set_rejects_duplicate_ids():
    req_set = RequirementSet("ULMS")
    req_set.add(make_req())
    with pytest.raises(ValueError):
        req_set.add(make_req())
