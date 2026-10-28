from requirements_toolkit.diagrams import DiagramGenerator

def test_use_case_diagram_contains_mermaid_flowchart(tmp_path):
    generator = DiagramGenerator(str(tmp_path))
    diagram = generator.use_case_diagram(
        actors=["Student"],
        use_cases=[{"use_case_id": "UC-01", "name": "Search Books", "primary_actor": "Student"}])
    assert diagram.startswith("flowchart LR")
    assert "Search Books" in diagram
    assert "Student" in diagram

def test_escape_text_removes_newlines_and_mermaid_delimiters():
    text = DiagramGenerator._escape_text('Search [books]| "online"\nnow')
    assert "\n" not in text
    assert "[" not in text and "]" not in text
