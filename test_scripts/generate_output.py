"""Build a concise final output report from actual pytest execution results."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "test_data" / "execution_results.json"
OUTPUT_JSON = ROOT / "test_data" / "output.json"
OUTPUT_CSV = ROOT / "test_data" / "output.csv"


def main() -> int:
    if not RAW.exists():
        raise SystemExit("No execution results found. Run: python test_scripts/run_tests.py")
    data = json.loads(RAW.read_text(encoding="utf-8"))
    output = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "summary": data.get("summary", {}),
        "results": [
            {k: result.get(k) for k in (
                "test_case_id", "title", "related_requirements", "expected_result",
                "actual_result", "status", "duration_seconds", "pytest_node", "details"
            )}
            for result in data.get("results", [])
        ],
        "note": data.get("note"),
    }
    OUTPUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    # CSV report is convenient for Excel/teacher review.
    import csv
    columns = ["test_case_id", "title", "related_requirements", "expected_result", "actual_result", "status", "duration_seconds", "pytest_node"]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(output["results"])
    print(f"Output JSON generated: {OUTPUT_JSON}")
    print(f"Output CSV generated:  {OUTPUT_CSV}")
    print("Summary:", output["summary"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
