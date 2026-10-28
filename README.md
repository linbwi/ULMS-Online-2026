# ULMS Online — Software Requirements Engineering Project

This repository contains the online library application and the requirements-engineering coursework toolkit.

## Two separate entry points

- `python app.py` starts the Flask website.
- `python main.py` reads the requirements workbook, runs automated requirement-quality checks, summarizes priorities and traceability, and generates the reports.

The toolkit does not replace the website; both are part of the ULMS project.

## Setup (Windows PowerShell)

From the folder containing `app.py`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Generate the coursework reports:

```powershell
python main.py
```

Run the tests:

```powershell
python -m pytest tests -v
```

Start the website separately:

```powershell
python app.py
```

## Workbook and generated artifacts

Input workbook: `data/ULMS_Online_2026_Requirements_Demo.xlsx`

Generated files in `case-study-srs/output/`:

- `ULMS_SRS.md` — generated draft Software Requirements Specification.
- `ULMS_requirements.csv` — requirements exported for review.
- `ULMS_traceability.json` — traceability links.
- `ULMS_dashboard.json` — workbook counts and summary metrics.

The report generator reads the workbook each time it runs. Review its outputs and resolve validation findings before submission. Automated validation uses heuristics; it does not establish that requirements are correct or approved.

## Project layout

- `app.py`, `models.py`, `config.py`, `templates/`, `static/`: web application.
- `requirements_toolkit/`: reusable requirements-engineering modules.
- `data/`: project requirements workbook.
- `case-study-srs/build_ulms_srs.py`: workbook-to-report generator.
- `tests/`: unit and smoke tests.
