# ULMS Online case-study SRS

This folder contains a workbook-to-report script for the Software Requirements Engineering course project.

## Generate the reports

From the project root:

```bash
pip install -r requirements.txt
python case-study-srs/build_ulms_srs.py
```

The script reads `data/ULMS_Online_2026_Requirements_Demo.xlsx` and writes:
- `output/ULMS_SRS.md` — generated draft SRS;
- `output/ULMS_requirements.csv` — requirement rows from the workbook;
- `output/ULMS_dashboard.json` — counts by workbook sheet, requirement type, and priority.

Review generated output before submission. A report generator does not validate the correctness of the source workbook or replace manual review.
