import pytest
from requirements_toolkit.use_case import UseCase, UseCaseSet

def make_use_case(uid="UC-01"):
    return UseCase(use_case_id=uid, name="Search Books",
        description="Student searches the online catalogue.",
        primary_actor="Student",
        preconditions=["The website is available"],
        postconditions=["Matching books are displayed"],
        main_flow=["Enter keywords", "Submit search", "View results"])

def test_use_case_records_main_flow_and_actor():
    uc = make_use_case()
    assert uc.primary_actor == "Student"
    assert len(uc.main_flow) == 3

def test_use_case_set_adds_use_case():
    cases = UseCaseSet("ULMS use cases")
    cases.add(make_use_case())
    assert len(cases.use_cases) == 1

def test_use_case_set_rejects_duplicate_ids():
    cases = UseCaseSet("ULMS use cases")
    cases.add(make_use_case())
    with pytest.raises(ValueError):
        cases.add(make_use_case())
