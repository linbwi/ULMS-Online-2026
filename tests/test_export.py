import json
from requirements_toolkit.export import DataExporter
from requirements_toolkit.requirement import Requirement, RequirementType, Priority

def test_exporter_writes_json_file(tmp_path):
    exporter = DataExporter(str(tmp_path))
    req = Requirement("REQ-01", "Search books",
        "The system shall allow students to search books.",
        RequirementType.FUNCTIONAL, Priority.MUST)
    path = exporter.export_json([req], "requirements.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data[0]["id"] == "REQ-01"

def test_exporter_writes_csv_file(tmp_path):
    exporter = DataExporter(str(tmp_path))
    req = Requirement("REQ-01", "Search books",
        "The system shall allow students to search books.",
        RequirementType.FUNCTIONAL, Priority.MUST)
    path = exporter.export_csv([req], "requirements.csv")
    assert "REQ-01" in path.read_text(encoding="utf-8")
