# ULMS Online application tests

`test_app.py` exercises the Flask website routes against an in-memory SQLite database.
It is separate from the existing Requirements Toolkit unit tests. The fixture in
`conftest.py` does not use or modify `instance/ulms.db`.

## Run

From the project root (the directory containing `app.py`):

```bash
python -m pip install -r requirements.txt
python -m pytest tests/test_app.py -v
```

Run all toolkit and application tests with:

```bash
python -m pytest tests -v
```

## Coverage and limits

The new tests cover authentication validation, member/admin access control, favorites,
reader authorization, access approval, reservations, return/audit records, overdue fine
consistency, search input handling, and account restrictions.

The current application source does not expose a scheduler/job for automatic expiry
revocation or overdue notifications, and the return route only changes a reservation to
`Ready` and sets `notified_at`; it does not itself prove that an email/push notification
was delivered. Therefore TC-06 and the delivery/time part of TC-20/TC-21 still require
implementation or a separately testable service before they can be marked Passed.

These are integration tests, not a complete security audit. Passing them does not prove
that every requirement in the workbook is satisfied.
