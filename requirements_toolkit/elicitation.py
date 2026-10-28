"""
Requirements Elicitation Module for ULMS Online.

This module manages elicitation sessions, including:
- Interviews
- Surveys
- Observations
- Workshops
- Document analysis
- Brainstorming

It also records findings, participants, and related requirements.
"""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


# ==================================================
# ENUMS
# ==================================================

class ElicitationMethod(str, Enum):
    """Methods used to elicit software requirements."""

    INTERVIEW = "INTERVIEW"
    SURVEY = "SURVEY"
    OBSERVATION = "OBSERVATION"
    WORKSHOP = "WORKSHOP"
    DOCUMENT_ANALYSIS = "DOCUMENT_ANALYSIS"
    BRAINSTORMING = "BRAINSTORMING"
    FOCUS_GROUP = "FOCUS_GROUP"
    OTHER = "OTHER"


class ElicitationStatus(str, Enum):
    """Lifecycle status of an elicitation session."""

    PLANNED = "PLANNED"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class FindingType(str, Enum):
    """Types of findings collected during elicitation."""

    REQUIREMENT = "REQUIREMENT"
    PROBLEM = "PROBLEM"
    NEED = "NEED"
    CONSTRAINT = "CONSTRAINT"
    ASSUMPTION = "ASSUMPTION"
    RISK = "RISK"
    OTHER = "OTHER"


# ==================================================
# ELICITATION FINDING
# ==================================================

@dataclass
class ElicitationFinding:
    """A finding discovered during an elicitation session."""

    finding_id: str
    description: str
    finding_type: FindingType = FindingType.OTHER
    source: str = ""
    related_requirement_ids: list[str] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self):
        self.finding_id = str(self.finding_id).strip()
        self.description = str(self.description).strip()
        self.source = str(self.source).strip()
        self.notes = str(self.notes).strip()

        if not self.finding_id:
            raise ValueError("finding_id must not be empty.")

        if not self.description:
            raise ValueError("description must not be empty.")

        if not isinstance(self.finding_type, FindingType):
            try:
                self.finding_type = FindingType(
                    str(self.finding_type).strip().upper()
                )
            except ValueError as exc:
                raise ValueError(
                    f"Invalid finding type: {self.finding_type}"
                ) from exc

        self.related_requirement_ids = [
            str(req_id).strip()
            for req_id in self.related_requirement_ids
            if str(req_id).strip()
        ]

    def has_related_requirements(self) -> bool:
        """Return True if this finding references requirements."""
        return bool(self.related_requirement_ids)

    def to_dict(self) -> dict:
        """Convert the finding to a dictionary."""
        return {
            "finding_id": self.finding_id,
            "description": self.description,
            "finding_type": self.finding_type.value,
            "source": self.source,
            "related_requirement_ids": self.related_requirement_ids.copy(),
            "notes": self.notes,
        }

    def __str__(self) -> str:
        return (
            f"{self.finding_id} | "
            f"{self.finding_type.value} | "
            f"{self.description}"
        )


# ==================================================
# ELICITATION SESSION
# ==================================================

@dataclass
class ElicitationSession:
    """An individual requirements elicitation session."""

    session_id: str
    title: str
    method: ElicitationMethod
    objective: str = ""
    session_date: Optional[str] = None
    facilitator: str = ""
    participants: list[str] = field(default_factory=list)
    status: ElicitationStatus = ElicitationStatus.PLANNED
    duration_minutes: Optional[int] = None
    location: str = ""
    questions: list[str] = field(default_factory=list)
    findings: list[ElicitationFinding] = field(default_factory=list)
    related_requirement_ids: list[str] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self):
        self.session_id = str(self.session_id).strip()
        self.title = str(self.title).strip()
        self.objective = str(self.objective).strip()
        self.facilitator = str(self.facilitator).strip()
        self.location = str(self.location).strip()
        self.notes = str(self.notes).strip()

        if not self.session_id:
            raise ValueError("session_id must not be empty.")

        if not self.title:
            raise ValueError("title must not be empty.")

        if not isinstance(self.method, ElicitationMethod):
            try:
                self.method = ElicitationMethod(
                    str(self.method).strip().upper()
                )
            except ValueError as exc:
                raise ValueError(
                    f"Invalid elicitation method: {self.method}"
                ) from exc

        if not isinstance(self.status, ElicitationStatus):
            try:
                self.status = ElicitationStatus(
                    str(self.status).strip().upper()
                )
            except ValueError as exc:
                raise ValueError(
                    f"Invalid elicitation status: {self.status}"
                ) from exc

        if self.session_date is not None:
            self.session_date = str(self.session_date).strip()

            if self.session_date:
                try:
                    date.fromisoformat(self.session_date)
                except ValueError as exc:
                    raise ValueError(
                        "session_date must use YYYY-MM-DD format."
                    ) from exc
            else:
                self.session_date = None

        if self.duration_minutes is not None:
            if (
                isinstance(self.duration_minutes, bool)
                or not isinstance(self.duration_minutes, int)
                or self.duration_minutes <= 0
            ):
                raise ValueError(
                    "duration_minutes must be a positive integer."
                )

        self.participants = [
            str(person).strip()
            for person in self.participants
            if str(person).strip()
        ]

        self.questions = [
            str(question).strip()
            for question in self.questions
            if str(question).strip()
        ]

        self.related_requirement_ids = [
            str(req_id).strip()
            for req_id in self.related_requirement_ids
            if str(req_id).strip()
        ]

        for finding in self.findings:
            if not isinstance(finding, ElicitationFinding):
                raise TypeError(
                    "Every finding must be an ElicitationFinding object."
                )

    # ----------------------------------------------
    # SESSION INFORMATION
    # ----------------------------------------------

    def add_participant(self, participant: str) -> None:
        """Add a participant if not already present."""
        participant = str(participant).strip()

        if not participant:
            raise ValueError("Participant must not be empty.")

        if participant not in self.participants:
            self.participants.append(participant)

    def remove_participant(self, participant: str) -> bool:
        """Remove a participant. Return whether one was removed."""
        participant = str(participant).strip()

        if participant in self.participants:
            self.participants.remove(participant)
            return True

        return False

    def add_question(self, question: str) -> None:
        """Add a question to the session."""
        question = str(question).strip()

        if not question:
            raise ValueError("Question must not be empty.")

        self.questions.append(question)

    # ----------------------------------------------
    # FINDINGS
    # ----------------------------------------------

    def add_finding(self, finding: ElicitationFinding) -> None:
        """Add a finding while preventing duplicate finding IDs."""
        if not isinstance(finding, ElicitationFinding):
            raise TypeError(
                "finding must be an ElicitationFinding object."
            )

        if any(
            existing.finding_id == finding.finding_id
            for existing in self.findings
        ):
            raise ValueError(
                f"Finding ID '{finding.finding_id}' already exists."
            )

        self.findings.append(finding)

    def get_finding(self, finding_id: str) -> Optional[ElicitationFinding]:
        """Find a finding by ID."""
        finding_id = str(finding_id).strip()

        for finding in self.findings:
            if finding.finding_id == finding_id:
                return finding

        return None

    def add_related_requirement(self, req_id: str) -> None:
        """Associate a requirement with this session."""
        req_id = str(req_id).strip()

        if not req_id:
            raise ValueError("Requirement ID must not be empty.")

        if req_id not in self.related_requirement_ids:
            self.related_requirement_ids.append(req_id)

    # ----------------------------------------------
    # QUALITY CHECKS
    # ----------------------------------------------

    def has_participants(self) -> bool:
        return bool(self.participants)

    def has_questions(self) -> bool:
        return bool(self.questions)

    def has_findings(self) -> bool:
        return bool(self.findings)

    def is_completed(self) -> bool:
        return self.status == ElicitationStatus.COMPLETED

    def is_complete(self) -> bool:
        """Check whether the session has its basic planning information."""
        return all([
            bool(self.session_id),
            bool(self.title),
            bool(self.objective),
            bool(self.participants),
            self.session_date is not None,
        ])

    def quality_issues(self) -> list[str]:
        """Return potential planning or documentation issues."""
        issues = []

        if not self.objective:
            issues.append("Session objective is missing.")

        if not self.participants:
            issues.append("No participants have been recorded.")

        if self.session_date is None:
            issues.append("Session date has not been specified.")

        if (
            self.status == ElicitationStatus.COMPLETED
            and not self.findings
        ):
            issues.append(
                "The session is completed but has no recorded findings."
            )

        if (
            self.method == ElicitationMethod.INTERVIEW
            and not self.questions
        ):
            issues.append(
                "Interview session has no prepared questions."
            )

        return issues

    # ----------------------------------------------
    # SERIALIZATION
    # ----------------------------------------------

    def to_dict(self) -> dict:
        """Convert the session and its findings into a dictionary."""
        return {
            "session_id": self.session_id,
            "title": self.title,
            "method": self.method.value,
            "objective": self.objective,
            "session_date": self.session_date,
            "facilitator": self.facilitator,
            "participants": self.participants.copy(),
            "status": self.status.value,
            "duration_minutes": self.duration_minutes,
            "location": self.location,
            "questions": self.questions.copy(),
            "findings": [
                finding.to_dict()
                for finding in self.findings
            ],
            "related_requirement_ids": (
                self.related_requirement_ids.copy()
            ),
            "notes": self.notes,
        }

    def __str__(self) -> str:
        return (
            f"{self.session_id} | {self.title} | "
            f"{self.method.value} | {self.status.value}"
        )


# ==================================================
# ELICITATION SESSION COLLECTION
# ==================================================

@dataclass
class ElicitationSessionSet:
    """Manage multiple elicitation sessions."""

    name: str = "Requirements Elicitation Sessions"
    sessions: list[ElicitationSession] = field(default_factory=list)

    def __post_init__(self):
        self.name = str(self.name).strip()

        if not self.name:
            raise ValueError("Session set name must not be empty.")

        existing_ids = set()

        for session in self.sessions:
            if not isinstance(session, ElicitationSession):
                raise TypeError(
                    "All sessions must be ElicitationSession objects."
                )

            if session.session_id in existing_ids:
                raise ValueError(
                    f"Duplicate session ID: {session.session_id}"
                )

            existing_ids.add(session.session_id)

    def add(self, session: ElicitationSession) -> None:
        """Add a session, ensuring unique session IDs."""
        if not isinstance(session, ElicitationSession):
            raise TypeError(
                "session must be an ElicitationSession object."
            )

        if self.get(session.session_id) is not None:
            raise ValueError(
                f"Session ID '{session.session_id}' already exists."
            )

        self.sessions.append(session)

    def get(self, session_id: str) -> Optional[ElicitationSession]:
        """Get a session by ID."""
        session_id = str(session_id).strip()

        for session in self.sessions:
            if session.session_id == session_id:
                return session

        return None

    def remove(self, session_id: str) -> bool:
        """Remove a session by ID."""
        session = self.get(session_id)

        if session is None:
            return False

        self.sessions.remove(session)
        return True

    def by_method(
        self,
        method: ElicitationMethod,
    ) -> list[ElicitationSession]:
        """Return sessions using a specific elicitation method."""
        if not isinstance(method, ElicitationMethod):
            method = ElicitationMethod(str(method).strip().upper())

        return [
            session for session in self.sessions
            if session.method == method
        ]

    def by_status(
        self,
        status: ElicitationStatus,
    ) -> list[ElicitationSession]:
        """Return sessions with a specific status."""
        if not isinstance(status, ElicitationStatus):
            status = ElicitationStatus(str(status).strip().upper())

        return [
            session for session in self.sessions
            if session.status == status
        ]

    def completed(self) -> list[ElicitationSession]:
        """Return all completed sessions."""
        return self.by_status(ElicitationStatus.COMPLETED)

    def pending(self) -> list[ElicitationSession]:
        """Return sessions that have not finished or been cancelled."""
        return [
            session for session in self.sessions
            if session.status in {
                ElicitationStatus.PLANNED,
                ElicitationStatus.SCHEDULED,
                ElicitationStatus.IN_PROGRESS,
            }
        ]

    def incomplete(self) -> list[ElicitationSession]:
        """Return sessions with missing basic planning information."""
        return [
            session for session in self.sessions
            if not session.is_complete()
        ]

    def with_quality_issues(self) -> list[ElicitationSession]:
        """Return sessions with one or more quality issues."""
        return [
            session for session in self.sessions
            if session.quality_issues()
        ]

    def count_by_method(self) -> dict[str, int]:
        """Count sessions by method."""
        return {
            method.value: len(self.by_method(method))
            for method in ElicitationMethod
        }

    def count_by_status(self) -> dict[str, int]:
        """Count sessions by status."""
        return {
            status.value: len(self.by_status(status))
            for status in ElicitationStatus
        }

    def all_findings(self) -> list[ElicitationFinding]:
        """Collect findings from every session."""
        return [
            finding
            for session in self.sessions
            for finding in session.findings
        ]

    def find_by_requirement(
        self,
        req_id: str,
    ) -> list[ElicitationSession]:
        """Find sessions related to a requirement ID."""
        req_id = str(req_id).strip()

        return [
            session for session in self.sessions
            if req_id in session.related_requirement_ids
            or any(
                req_id in finding.related_requirement_ids
                for finding in session.findings
            )
        ]

    def __len__(self) -> int:
        return len(self.sessions)

    def __iter__(self):
        return iter(self.sessions)

    def __contains__(self, session_id: str) -> bool:
        return self.get(session_id) is not None

    def __str__(self) -> str:
        return (
            f"{self.name}: {len(self.sessions)} session(s)"
        )