"""Integration tests for the ULMS requirements-engineering CLI."""
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_main_cli_generates_reports_and_prints_core_sections():
    result = subprocess.run(
        [sys.executable, "main.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    for heading in (
        "=== Requirements ===",
        "=== Testability / Quality Check ===",
        "=== Priority Breakdown ===",
        "=== Traceability / Coverage Report ===",
        "=== Generated Artifacts ===",
    ):
        assert heading in result.stdout


def test_workbook_and_generated_srs_exist():
    assert (ROOT / "data" / "ULMS_Online_2026_Requirements_Demo.xlsx").exists()
    assert (ROOT / "case-study-srs" / "output" / "ULMS_SRS.md").exists()
