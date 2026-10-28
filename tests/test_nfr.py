import pytest
from requirements_toolkit.nfr import NFR, NFRSet, NFRCategory, NFRPriority

def make_nfr(nfr_id="NFR-01"):
    return NFR(nfr_id=nfr_id, title="Search performance",
               statement="The system shall return search results within 2 seconds.",
               category=NFRCategory.PERFORMANCE, priority=NFRPriority.MUST)

def test_nfr_stores_ulms_quality_requirement():
    nfr = make_nfr()
    assert nfr.nfr_id == "NFR-01"
    assert nfr.category == NFRCategory.PERFORMANCE

def test_nfr_set_adds_item():
    nfrs = NFRSet("ULMS NFRs")
    nfrs.add(make_nfr())
    assert len(nfrs.nfrs) == 1

def test_nfr_set_rejects_duplicate_ids():
    nfrs = NFRSet("ULMS NFRs")
    nfrs.add(make_nfr())
    with pytest.raises(ValueError):
        nfrs.add(make_nfr())
