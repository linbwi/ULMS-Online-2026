import pytest
from requirements_toolkit.stakeholders import Stakeholder, StakeholderRole, StakeholderType, StakeholderPriority, StakeholderSet

def make_stakeholder(sid="ST-01"):
    return Stakeholder(stakeholder_id=sid, name="Student",
        role=StakeholderRole.STUDENT, stakeholder_type=StakeholderType.PRIMARY,
        interest=5, influence=3, responsibilities="Search and borrow digital books",
        needs="Find books easily", priority=StakeholderPriority.HIGH)

def test_stakeholder_keeps_role_and_needs():
    s = make_stakeholder()
    assert s.name == "Student"
    assert s.role == StakeholderRole.STUDENT
    assert s.needs == "Find books easily"

def test_stakeholder_set_adds_stakeholder():
    group = StakeholderSet("ULMS stakeholders")
    group.add(make_stakeholder())
    assert len(group.stakeholders) == 1

def test_stakeholder_set_rejects_duplicate_ids():
    group = StakeholderSet("ULMS stakeholders")
    group.add(make_stakeholder())
    with pytest.raises(ValueError):
        group.add(make_stakeholder())
