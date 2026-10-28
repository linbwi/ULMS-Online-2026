# ULMS Online — Architecture

This repository contains two related but distinct parts.

## 1. Online library application

- `app.py`: Flask application entry point and HTTP routes.
- `models.py`: SQLAlchemy models for library operations.
- `config.py`: environment-based application configuration.
- `templates/`: Jinja2 pages.
- `static/`: CSS and static assets.
- `instance/ulms.db`: local SQLite database, if present.

Run the web application with `python app.py`. This part handles library features such as accounts, catalogue browsing, loans and administrative pages.

## 2. Software Requirements Engineering toolkit

- `requirements_toolkit/requirement.py`: requirement domain model and collection.
- `validation.py`: quality checks for requirement statements and sets.
- `change_management.py`: change request and baseline support.
- `nfr.py`: non-functional requirement modeling.
- `stakeholders.py`: stakeholder records and analysis.
- `use_case.py`: use-case modeling.
- `diagrams.py`: lightweight diagram/model helpers.
- `safety.py`: hazard and safety analysis.
- `traceability.py`: links between requirements and other artifacts.
- `export.py`: CSV/JSON/Markdown export utilities.
- `process.py`: requirements engineering process modeling.
- `elicitation.py`: elicitation session and analysis helpers.
- `srs_generator.py`: SRS document generation.

The toolkit is deliberately separate from the Flask app so it can be tested and demonstrated independently. `main.py` runs a small in-memory toolkit demo. `case-study-srs/build_ulms_srs.py` reads the project workbook and creates a case-study SRS plus data exports.

## Data flow

`data/ULMS_Online_2026_Requirements_Demo.xlsx`
→ workbook reader
→ `RequirementSet`
→ SRS Markdown / CSV / JSON summary in `case-study-srs/output/`.

## Test

Run `pytest` from the repository root. Tests exercise the public APIs and the workbook-based report builder.
