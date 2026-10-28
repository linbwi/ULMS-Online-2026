"""Execute mapped Excel test cases using existing pytest integration tests.

Only cases with a mapping to a real pytest node are executed. Unmapped cases are
reported as NOT_AUTOMATED rather than being falsely marked PASS.
Usage: python test_scripts/run_tests.py
"""
from __future__ import annotations
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "test_data" / "input.json"
RAW_RESULTS = ROOT / "test_data" / "execution_results.json"

# Explicit traceability from Excel IDs to existing executable integration tests.
# Extend this mapping when additional test functions are implemented.
TEST_MAP = {
    "TC-01": "tests/test_app.py::test_registered_member_can_log_in_with_valid_credentials",
    "TC-02": "tests/test_app.py::test_catalogue_search_returns_matching_results_within_two_seconds",
    "TC-04": "tests/test_app.py::test_eligible_member_can_renew_active_loan",
    "TC-07": "tests/test_app.py::test_member_can_view_loan_history_fines_and_favourites",
    "TC-03": "tests/test_app.py::test_access_request_is_pending_when_circulation_admin_approval_enabled",
    "TC-05": "tests/test_app.py::test_member_cannot_open_admin_page",
    "TC-09": "tests/test_app.py::test_member_can_add_and_remove_favorite",
    "TC-10": "tests/test_app.py::test_member_with_active_loan_can_read_book",
    "TC-11": "tests/test_app.py::test_member_without_active_loan_is_redirected_from_reader",
    "TC-14": "tests/test_app.py::test_admin_can_approve_pending_access_and_audit_it",
    "TC-15": "tests/test_app.py::test_admin_can_suspend_member_and_audit_action",
    "TC-18": "tests/test_app.py::test_member_cannot_view_admin_audit_log",
    "TC-19": "tests/test_app.py::test_member_can_reserve_book_when_no_copies_available",
    "TC-23": "tests/test_app.py::test_search_escapes_script_input_in_rendered_html",
    "TC-06": "tests/test_app.py::test_expired_digital_access_is_revoked_on_next_read_attempt",
    "TC-08": "tests/test_app.py::test_login_and_online_access_decisions_are_audited",
    "TC-12": "tests/test_app.py::test_member_can_request_access_again_after_previous_loan_returned",
    "TC-13": "tests/test_app.py::test_member_with_unpaid_fine_cannot_request_another_book",
    "TC-16": "tests/test_app.py::test_suspended_member_cannot_read_even_with_active_loan",
    "TC-17": "tests/test_app.py::test_overdue_fine_uses_full_overdue_days_and_configured_daily_rate",
    "TC-20": "tests/test_app.py::test_return_marks_next_reservation_ready_and_records_audit",
    "TC-21": "tests/test_app.py::test_overdue_loan_appears_in_member_notifications",
    "TC-22": "tests/test_app.py::test_reservation_return_fine_transactions_are_audited",
}


def main() -> int:
    if not INPUT.exists():
        print("Input file not found. Run: python test_scripts/generate_input.py", file=sys.stderr)
        return 2
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    results = []
    for case in payload.get("test_cases", []):
        case_id = case["id"]
        node = TEST_MAP.get(case_id)
        base = {
            "test_case_id": case_id,
            "title": case.get("title"),
            "related_requirements": case.get("related_requirements"),
            "expected_result": case.get("expected_result"),
            "pytest_node": node,
        }
        if not node:
            results.append({**base, "status": "NOT_AUTOMATED", "actual_result": None,
                            "duration_seconds": 0, "details": "No executable pytest mapping yet; not counted as PASS or FAIL."})
            print(f"[NOT AUTOMATED] {case_id} - {case.get('title')}")
            continue
        start = time.perf_counter()
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", node, "-q", "--disable-warnings"],
            cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        duration = round(time.perf_counter() - start, 3)
        if proc.returncode == 0:
            status = "PASS"
            actual = "Mapped pytest test passed."
        elif proc.returncode == 5 or "ModuleNotFoundError" in proc.stdout or "ImportError while loading conftest" in proc.stdout:
            status = "ERROR"
            actual = "Test could not execute because collection/environment setup failed; inspect details."
        else:
            status = "FAIL"
            actual = "Mapped pytest test ran and failed; inspect details."
        results.append({**base, "status": status, "actual_result": actual,
                        "duration_seconds": duration, "details": proc.stdout[-6000:]})
        print(f"[{status}] {case_id} - {case.get('title')} ({duration}s)")

    counts = {key: sum(1 for r in results if r["status"] == key)
              for key in ("PASS", "FAIL", "ERROR", "NOT_AUTOMATED")}
    report = {
        "source_input": str(INPUT.relative_to(ROOT)),
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "summary": {"total": len(results), **counts},
        "results": results,
        "note": "Only mapped tests are executed. NOT_AUTOMATED cases are explicitly not treated as passing.",
    }
    RAW_RESULTS.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRaw execution results: {RAW_RESULTS}")
    print("Summary: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    return 1 if counts["FAIL"] or counts["ERROR"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
