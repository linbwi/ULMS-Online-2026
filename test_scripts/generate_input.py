"""Convert the Excel test_cases sheet into a machine-readable input.json.

Usage (from project root): python test_scripts/generate_input.py
"""
from __future__ import annotations
import json
import sys
from datetime import date, datetime
from pathlib import Path
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_XLSX = ROOT / "data" / "ULMS_Online_2026_Requirements_Demo.xlsx"
OUTPUT = ROOT / "test_data" / "input.json"
SHEET_NAME = "test_cases"


def json_value(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def main() -> int:
    source = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_XLSX
    if not source.exists():
        print(f"ERROR: Excel file not found: {source}", file=sys.stderr)
        return 2
    workbook = load_workbook(source, read_only=True, data_only=True)
    if SHEET_NAME not in workbook.sheetnames:
        print(f"ERROR: Required sheet '{SHEET_NAME}' not found. Available: {workbook.sheetnames}", file=sys.stderr)
        return 2
    sheet = workbook[SHEET_NAME]
    rows = sheet.iter_rows(values_only=True)
    headers = [str(h).strip() if h is not None else "" for h in next(rows, ())]
    if not headers or "id" not in headers:
        print("ERROR: test_cases sheet must contain an 'id' column.", file=sys.stderr)
        return 2

    cases = []
    seen = set()
    for row_number, row in enumerate(rows, start=2):
        raw = {headers[i]: json_value(row[i]) if i < len(row) else None for i in range(len(headers)) if headers[i]}
        if not any(v not in (None, "") for v in raw.values()):
            continue
        case_id = str(raw.get("id") or "").strip()
        if not case_id:
            print(f"WARNING: Row {row_number} skipped because id is empty.")
            continue
        if case_id in seen:
            print(f"ERROR: Duplicate test case id '{case_id}' at row {row_number}.", file=sys.stderr)
            return 2
        seen.add(case_id)
        cases.append({
            "id": case_id,
            "title": raw.get("title"),
            "related_requirements": raw.get("related_requirements"),
            "type": raw.get("type"),
            "priority": raw.get("priority"),
            "preconditions": raw.get("preconditions"),
            "steps": raw.get("steps"),
            "expected_result": raw.get("expected_result"),
            # Existing Excel status/actual_result are historical records, not new run results.
            "source_status": raw.get("status"),
            "automation_key": raw.get("automation_key") or None,
            "input_data": raw.get("input_data") or None,
            "source_row": row_number,
        })
    payload = {
        "source_file": str(source.name),
        "source_sheet": SHEET_NAME,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "count": len(cases),
        "test_cases": cases,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Excel: {source}")
    print(f"Test cases extracted: {len(cases)}")
    print(f"Input generated: {OUTPUT}")
    print("Note: Excel status/actual_result are preserved as source metadata only; they are not treated as execution results.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
