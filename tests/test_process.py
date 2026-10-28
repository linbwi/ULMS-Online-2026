import pytest
from requirements_toolkit.process import ProcessStep, ProcessPhase, ProcessStatus, RequirementsProcess

def make_step(step_id="STEP-01"):
    return ProcessStep(step_id=step_id, name="Validate requirements",
        phase=ProcessPhase.VALIDATION, description="Review requirements for clarity.")

def test_process_step_start_and_complete():
    step = make_step()
    step.start()
    assert step.status == ProcessStatus.IN_PROGRESS
    step.complete()
    assert step.status == ProcessStatus.COMPLETED
    assert step.is_completed

def test_process_rejects_duplicate_step_ids():
    process = RequirementsProcess("ULMS RE process")
    process.add_step(make_step())
    with pytest.raises(ValueError):
        process.add_step(make_step())

def test_process_unknown_step_returns_false():
    process = RequirementsProcess("ULMS RE process")
    assert process.start_step("MISSING") is False
