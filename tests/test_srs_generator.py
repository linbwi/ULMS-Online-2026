from requirements_toolkit.srs_generator import SRSMetadata, SRSGenerator
from requirements_toolkit.requirement import Requirement, RequirementSet, RequirementType, Priority

def test_srs_metadata_rejects_empty_project_name():
    import pytest
    with pytest.raises(ValueError):
        SRSMetadata(project_name=" ")

def test_srs_generator_includes_project_and_requirement(tmp_path):
    reqs = RequirementSet("ULMS")
    reqs.add(Requirement("REQ-01", "Search books",
        "The system shall allow students to search the catalogue.",
        RequirementType.FUNCTIONAL, Priority.MUST))
    generator = SRSGenerator(metadata=SRSMetadata(project_name="ULMS Online"),
        requirements=reqs)
    output = generator.generate_markdown()
    assert "ULMS Online" in output
    assert "REQ-01" in output
