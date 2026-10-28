import pytest
from requirements_toolkit.change_management import ChangeRequest, ChangeRequestSet, ChangeType, ChangePriority

def make_change(cid="CR-01"):
    return ChangeRequest(change_id=cid, title="Add book preview",
        description="Allow users to preview a digital book before opening it.",
        change_type=ChangeType.ADD, requester="Student",
        reason="Improve book discovery", priority=ChangePriority.MEDIUM)

def test_change_request_captures_reason_and_type():
    change = make_change()
    assert change.change_id == "CR-01"
    assert change.change_type == ChangeType.ADD

def test_change_request_set_adds_request():
    changes = ChangeRequestSet("ULMS change requests")
    changes.add(make_change())
    assert len(changes.requests) == 1

def test_change_request_set_rejects_duplicate_ids():
    changes = ChangeRequestSet("ULMS change requests")
    changes.add(make_change())
    with pytest.raises(ValueError):
        changes.add(make_change())
