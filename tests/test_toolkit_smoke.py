"""Smoke and contract tests for the ULMS requirements toolkit."""
import importlib
from pathlib import Path

import pytest

from requirements_toolkit.requirement import (
    Priority, Requirement, RequirementSet, RequirementStatus, RequirementType,
)
from requirements_toolkit.validation import validate_requirement, validate_requirement_set
from requirements_toolkit.srs_generator import SRSGenerator, SRSMetadata
from requirements_toolkit.traceability import (
    TraceabilityLink, TraceabilityMatrix, TraceabilityType,
)
from requirements_toolkit.export import DataExporter


MODULES = [
    "requirement", "validation", "change_management", "nfr",
    "stakeholders", "use_case", "diagrams", "safety", "export",
    "process", "elicitation", "traceability", "srs_generator",
]


@pytest.fixture
def sample_requirement():
    return Requirement(
        req_id=" req-01 ",
        title="Search books",
        statement="The system shall let users search books by title.",
        req_type=RequirementType.FUNCTIONAL,
        priority=Priority.MUST,
        status=RequirementStatus.PROPOSED,
        acceptance_criteria="Matching books are displayed.",
        verification_method="Test",
    )


def test_all_toolkit_modules_import():
    for module in MODULES:
        assert importlib.import_module(f"requirements_toolkit.{module}")


def test_requirement_normalizes_id(sample_requirement):
    assert sample_requirement.req_id == "REQ-01"


def test_requirement_serializes(sample_requirement):
    record = sample_requirement.to_dict()
    assert record["id"] == "REQ-01"
    assert record["title"] == "Search books"


def test_requirement_rejects_empty_id():
    with pytest.raises(ValueError):
        Requirement("", "Title", "A statement", RequirementType.FUNCTIONAL)


def test_requirement_set_add_and_get(sample_requirement):
    requirements = RequirementSet("ULMS")
    requirements.add(sample_requirement)
    assert requirements.get("req-01") is sample_requirement
    assert len(requirements.requirements) == 1


def test_requirement_set_rejects_duplicate(sample_requirement):
    requirements = RequirementSet("ULMS")
    requirements.add(sample_requirement)
    with pytest.raises(ValueError):
        requirements.add(sample_requirement)


def test_requirement_set_remove(sample_requirement):
    requirements = RequirementSet("ULMS", [sample_requirement])
    assert requirements.remove("REQ-01") is True
    assert requirements.get("REQ-01") is None


def test_single_requirement_validation_returns_report(sample_requirement):
    report = validate_requirement(sample_requirement)
    assert hasattr(report, "issues")


def test_requirement_set_validation_returns_report(sample_requirement):
    report = validate_requirement_set(RequirementSet("ULMS", [sample_requirement]))
    assert hasattr(report, "issues")
    assert isinstance(report.summary(), dict)


def test_traceability_link_normalizes_ids():
    link = TraceabilityLink(
        "req-01", "uc-01", TraceabilityType.REQUIREMENT_TO_USE_CASE
    )
    assert link.source_id == "REQ-01"
    assert link.target_id == "UC-01"


def test_traceability_rejects_self_link():
    with pytest.raises(ValueError):
        TraceabilityLink(
            "REQ-01", "REQ-01",
            TraceabilityType.REQUIREMENT_TO_REQUIREMENT,
        )


def test_traceability_matrix_add_and_query():
    matrix = TraceabilityMatrix("ULMS")
    link = TraceabilityLink(
        "REQ-01", "TC-01", TraceabilityType.REQUIREMENT_TO_TEST_CASE
    )
    matrix.add_link(link)
    assert matrix.has_link("req-01", "tc-01")
    assert len(matrix.forward("REQ-01")) == 1


def test_traceability_matrix_rejects_duplicate():
    link = TraceabilityLink(
        "REQ-01", "TC-01", TraceabilityType.REQUIREMENT_TO_TEST_CASE
    )
    matrix = TraceabilityMatrix("ULMS", [link])
    with pytest.raises(ValueError):
        matrix.add_link(link)


def test_srs_generator_creates_markdown(sample_requirement, tmp_path):
    generator = SRSGenerator(
        metadata=SRSMetadata(project_name="ULMS Online"),
        requirements=RequirementSet("ULMS", [sample_requirement]),
    )
    content = generator.generate_markdown()
    assert "Software Requirements Specification" in content
    assert "REQ-01" in content
    output = generator.save(str(tmp_path / "srs.md"))
    assert output.exists()


def test_srs_generator_rejects_unknown_format(tmp_path):
    generator = SRSGenerator()
    with pytest.raises(ValueError):
        generator.save(str(tmp_path / "srs.unknown"))


def test_export_json(sample_requirement, tmp_path):
    exporter = DataExporter(str(tmp_path))
    output = exporter.export_json([sample_requirement], "requirements.json")
    assert output.exists()
    assert "REQ-01" in output.read_text(encoding="utf-8")


def test_export_csv(sample_requirement, tmp_path):
    exporter = DataExporter(str(tmp_path))
    output = exporter.export_csv([sample_requirement], "requirements.csv")
    assert output.exists()
    assert "REQ-01" in output.read_text(encoding="utf-8")


def test_case_study_builder_loads_workbook():
    from importlib.util import spec_from_file_location, module_from_spec
    project_root = Path(__file__).resolve().parents[1]
    script = project_root / "case-study-srs" / "build_ulms_srs.py"
    if not script.exists():
        script = project_root.parent / "case-study-srs" / "build_ulms_srs.py"
    spec = spec_from_file_location("build_ulms_srs", script)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    workbook = module.load_workbook(module.WORKBOOK, read_only=True, data_only=True)
    try:
        records = module.read_sheet(workbook, "requirements")
    finally:
        workbook.close()
    assert len(records) > 0
    assert "id" in records[0]
    assert "description" in records[0]


def test_case_study_builder_converts_requirements():
    from importlib.util import spec_from_file_location, module_from_spec
    project_root = Path(__file__).resolve().parents[1]
    script = project_root / "case-study-srs" / "build_ulms_srs.py"
    if not script.exists():
        script = project_root.parent / "case-study-srs" / "build_ulms_srs.py"
    spec = spec_from_file_location("build_ulms_srs", script)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    wb = module.load_workbook(module.WORKBOOK, read_only=True, data_only=True)
    try:
        records = module.read_sheet(wb, "requirements")
    finally:
        wb.close()
    req_set = module.build_requirement_set(records)
    assert len(req_set.requirements) > 0
    assert req_set.requirements[0].req_id.startswith("REQ-")
