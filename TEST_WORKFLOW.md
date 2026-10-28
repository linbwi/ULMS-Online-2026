# ULMS Online - Excel-driven test workflow

## Flow

`data/ULMS_Online_2026_Requirements_Demo.xlsx` → `test_scripts/generate_input.py` → `test_data/input.json` → `test_scripts/run_tests.py` → `test_data/execution_results.json` → `test_scripts/generate_output.py` → `test_data/output.json` and `test_data/output.csv`.

## Run from the project root

Install dependencies if needed:

```bash
pip install -r requirements.txt
```

Run the complete workflow:

```bash
python test_scripts/generate_input.py
python test_scripts/run_tests.py
python test_scripts/generate_output.py
```

You can pass a different Excel path to the generator:

```bash
python test_scripts/generate_input.py path/to/your.xlsx
```

## Important accuracy rules

- The generator reads the `test_cases` sheet and preserves each Excel Test Case ID and expected result.
- Existing Excel `status` and `actual_result` values are treated as historical source metadata, never as the result of the new test run.
- `run_tests.py` maps a subset of Test Case IDs to existing executable pytest tests. Only those mapped tests are run.
- Cases without a real mapping are reported as `NOT_AUTOMATED`; they are not falsely marked PASS. Add a real test function and a `TEST_MAP` entry before claiming automated coverage.
- A mapped test's pytest result is the execution status. Its printed details are stored in `execution_results.json` and `output.json` for debugging.
- Tests use the in-memory SQLite database configured in `tests/conftest.py`, not the persistent `instance/ulms.db` database.

## Extend coverage

1. Implement a pytest test in `tests/test_app.py` (or another `tests/test_*.py` file).
2. Add the Excel ID to `TEST_MAP` in `test_scripts/run_tests.py` using its exact pytest node ID.
3. Re-run all three commands.

Some Excel test cases describe background jobs, email delivery, performance percentile measurements, or business behavior not currently exposed as a callable test target. These remain `NOT_AUTOMATED` until the relevant implementation/test harness exists.
