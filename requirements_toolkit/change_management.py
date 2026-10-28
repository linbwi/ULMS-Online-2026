"""
Change Management Module for University Library Management System Online.

This module provides:
- Change request data management
- Change request status tracking
- Change request priority management
- Change impact analysis
- Change request filtering and statistics
- Change request validation
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ============================================================
# 1. ENUMS
# ============================================================

class ChangeType(Enum):
    """Types of change requests."""

    ADD = "Add"
    MODIFY = "Modify"
    DELETE = "Delete"
    REPLACE = "Replace"
    CLARIFY = "Clarify"


class ChangePriority(Enum):
    """Priority levels of change requests."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class ChangeStatus(Enum):
    """Lifecycle status of a change request."""

    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    IMPLEMENTED = "Implemented"
    VERIFIED = "Verified"
    DEFERRED = "Deferred"


class ChangeImpact(Enum):
    """Estimated impact of a proposed change."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


# ============================================================
# 2. CHANGE REQUEST
# ============================================================

@dataclass
class ChangeRequest:
    """
    Represents a change request for a project requirement.

    Attributes:
        change_id: Unique identifier, e.g. CR-01.
        title: Short title of the proposed change.
        description: Explanation of the requested change.
        change_type: Type of change being requested.
        requester: Person or role requesting the change.
        reason: Reason for the change.
        affected_requirements: IDs of affected requirements.
        affected_use_cases: IDs of affected use cases.
        affected_test_cases: IDs of affected test cases.
        priority: Business priority of the request.
        status: Current status.
        impact: Estimated impact.
        submitted_date: Date the request was submitted.
        reviewer: Person responsible for reviewing the request.
        decision_reason: Explanation of the approval/rejection decision.
        notes: Additional information.
    """

    change_id: str
    title: str
    description: str
    change_type: ChangeType
    requester: str
    reason: str

    affected_requirements: list[str] = field(default_factory=list)
    affected_use_cases: list[str] = field(default_factory=list)
    affected_test_cases: list[str] = field(default_factory=list)

    priority: ChangePriority = ChangePriority.MEDIUM
    status: ChangeStatus = ChangeStatus.SUBMITTED
    impact: ChangeImpact = ChangeImpact.MEDIUM

    submitted_date: str = ""
    reviewer: str = ""
    decision_reason: str = ""
    notes: str = ""

    def __post_init__(self):
        """Normalize values and validate required fields."""

        self.change_id = str(self.change_id).strip().upper()
        self.title = str(self.title).strip()
        self.description = str(self.description).strip()
        self.requester = str(self.requester).strip()
        self.reason = str(self.reason).strip()

        if not self.change_id:
            raise ValueError("Change request ID cannot be empty.")

        if not self.title:
            raise ValueError("Change request title cannot be empty.")

        if not self.description:
            raise ValueError("Change request description cannot be empty.")

        if not self.requester:
            raise ValueError("Requester cannot be empty.")

        if not self.reason:
            raise ValueError("Reason for change cannot be empty.")

        # Normalize artifact ID lists.
        self.affected_requirements = self._normalize_ids(
            self.affected_requirements
        )
        self.affected_use_cases = self._normalize_ids(
            self.affected_use_cases
        )
        self.affected_test_cases = self._normalize_ids(
            self.affected_test_cases
        )

        # Normalize text fields.
        self.submitted_date = str(self.submitted_date).strip()
        self.reviewer = str(self.reviewer).strip()
        self.decision_reason = str(self.decision_reason).strip()
        self.notes = str(self.notes).strip()

        # Validate enum fields.
        self.change_type = self._normalize_enum(
            self.change_type, ChangeType, "change type"
        )
        self.priority = self._normalize_enum(
            self.priority, ChangePriority, "priority"
        )
        self.status = self._normalize_enum(
            self.status, ChangeStatus, "status"
        )
        self.impact = self._normalize_enum(
            self.impact, ChangeImpact, "impact"
        )

    @staticmethod
    def _normalize_ids(values) -> list[str]:
        """Normalize a list of artifact IDs."""

        if values is None:
            return []

        if isinstance(values, str):
            values = [values]

        if not isinstance(values, (list, tuple, set)):
            raise ValueError("Artifact IDs must be supplied as a list.")

        return [
            str(value).strip().upper()
            for value in values
            if value is not None and str(value).strip()
        ]

    @staticmethod
    def _normalize_enum(value, enum_class, field_name):
        """Convert a string into its corresponding enum value."""

        if isinstance(value, enum_class):
            return value

        try:
            return enum_class(value)
        except ValueError:
            valid_values = [item.value for item in enum_class]

            raise ValueError(
                f"Invalid {field_name}: {value}. "
                f"Expected one of: {valid_values}"
            )

    # --------------------------------------------------------
    # CHANGE REQUEST CHECKS
    # --------------------------------------------------------

    def has_affected_artifacts(self) -> bool:
        """Check whether any project artifacts are affected."""

        return any([
            self.affected_requirements,
            self.affected_use_cases,
            self.affected_test_cases,
        ])

    def is_complete(self) -> bool:
        """Check whether the request has its essential information."""

        return all([
            self.change_id,
            self.title,
            self.description,
            self.requester,
            self.reason,
        ])

    def requires_impact_analysis(self) -> bool:
        """Check whether impact analysis should be performed."""

        return self.status in {
            ChangeStatus.SUBMITTED,
            ChangeStatus.UNDER_REVIEW,
        }

    def is_pending(self) -> bool:
        """Check whether the request is awaiting a final decision."""

        return self.status in {
            ChangeStatus.SUBMITTED,
            ChangeStatus.UNDER_REVIEW,
        }

    def is_approved(self) -> bool:
        """Check whether the request has been approved."""

        return self.status == ChangeStatus.APPROVED

    def quality_issues(self) -> list[str]:
        """Return possible issues in the change request."""

        issues = []

        if not self.title:
            issues.append("Change request title is missing.")

        if not self.description:
            issues.append("Change description is missing.")

        if not self.requester:
            issues.append("Requester is missing.")

        if not self.reason:
            issues.append("Reason for change is missing.")

        if not self.has_affected_artifacts():
            issues.append(
                "No affected requirements, use cases, or test cases specified."
            )

        if (
            self.status in {
                ChangeStatus.APPROVED,
                ChangeStatus.REJECTED,
            }
            and not self.decision_reason
        ):
            issues.append(
                "Decision reason is missing for an approved or rejected request."
            )

        return issues

    # --------------------------------------------------------
    # UPDATE OPERATIONS
    # --------------------------------------------------------

    def update_status(
        self,
        new_status: ChangeStatus,
        decision_reason: Optional[str] = None,
    ) -> None:
        """Update status and optionally record the decision reason."""

        new_status = self._normalize_enum(
            new_status, ChangeStatus, "status"
        )

        self.status = new_status

        if decision_reason is not None:
            self.decision_reason = str(decision_reason).strip()

    def set_impact(self, impact: ChangeImpact) -> None:
        """Update the estimated impact."""

        self.impact = self._normalize_enum(
            impact, ChangeImpact, "impact"
        )

    def add_affected_requirement(self, requirement_id: str) -> None:
        """Add an affected requirement ID if it is not already present."""

        requirement_id = str(requirement_id).strip().upper()

        if not requirement_id:
            raise ValueError("Requirement ID cannot be empty.")

        if requirement_id not in self.affected_requirements:
            self.affected_requirements.append(requirement_id)

    def add_affected_use_case(self, use_case_id: str) -> None:
        """Add an affected use case ID if it is not already present."""

        use_case_id = str(use_case_id).strip().upper()

        if not use_case_id:
            raise ValueError("Use case ID cannot be empty.")

        if use_case_id not in self.affected_use_cases:
            self.affected_use_cases.append(use_case_id)

    def add_affected_test_case(self, test_case_id: str) -> None:
        """Add an affected test case ID if it is not already present."""

        test_case_id = str(test_case_id).strip().upper()

        if not test_case_id:
            raise ValueError("Test case ID cannot be empty.")

        if test_case_id not in self.affected_test_cases:
            self.affected_test_cases.append(test_case_id)

    # --------------------------------------------------------
    # CONVERSION
    # --------------------------------------------------------

    def to_dict(self) -> dict:
        """Convert the change request into a dictionary."""

        return {
            "change_id": self.change_id,
            "title": self.title,
            "description": self.description,
            "change_type": self.change_type.value,
            "requester": self.requester,
            "reason": self.reason,
            "affected_requirements": self.affected_requirements.copy(),
            "affected_use_cases": self.affected_use_cases.copy(),
            "affected_test_cases": self.affected_test_cases.copy(),
            "priority": self.priority.value,
            "status": self.status.value,
            "impact": self.impact.value,
            "submitted_date": self.submitted_date,
            "reviewer": self.reviewer,
            "decision_reason": self.decision_reason,
            "notes": self.notes,
        }

    def __str__(self) -> str:
        return (
            f"{self.change_id}: {self.title} "
            f"[Status: {self.status.value}, "
            f"Priority: {self.priority.value}, "
            f"Impact: {self.impact.value}]"
        )


# ============================================================
# 3. CHANGE REQUEST COLLECTION
# ============================================================

@dataclass
class ChangeRequestSet:
    """Manage a collection of change requests."""

    name: str
    requests: list[ChangeRequest] = field(default_factory=list)

    def __post_init__(self):
        self.name = str(self.name).strip()

        if not self.name:
            raise ValueError("Change request set name cannot be empty.")

        if not isinstance(self.requests, list):
            raise ValueError("requests must be a list.")

        existing_ids = set()

        for request in self.requests:
            if not isinstance(request, ChangeRequest):
                raise TypeError(
                    "Every item must be a ChangeRequest object."
                )

            if request.change_id in existing_ids:
                raise ValueError(
                    f"Duplicate change request ID: {request.change_id}"
                )

            existing_ids.add(request.change_id)

    # --------------------------------------------------------
    # CRUD OPERATIONS
    # --------------------------------------------------------

    def add(self, request: ChangeRequest) -> None:
        """Add a new change request."""

        if not isinstance(request, ChangeRequest):
            raise TypeError("request must be a ChangeRequest object.")

        if self.get(request.change_id) is not None:
            raise ValueError(
                f"Change request ID already exists: {request.change_id}"
            )

        self.requests.append(request)

    def get(self, change_id: str) -> Optional[ChangeRequest]:
        """Find a change request by ID."""

        change_id = str(change_id).strip().upper()

        for request in self.requests:
            if request.change_id == change_id:
                return request

        return None

    def remove(self, change_id: str) -> bool:
        """Remove a change request by ID."""

        request = self.get(change_id)

        if request is None:
            return False

        self.requests.remove(request)
        return True

    # --------------------------------------------------------
    # FILTERING
    # --------------------------------------------------------

    def by_status(self, status: ChangeStatus) -> list[ChangeRequest]:
        """Return requests matching a status."""

        if not isinstance(status, ChangeStatus):
            status = ChangeStatus(status)

        return [
            request
            for request in self.requests
            if request.status == status
        ]

    def by_priority(
        self,
        priority: ChangePriority,
    ) -> list[ChangeRequest]:
        """Return requests matching a priority."""

        if not isinstance(priority, ChangePriority):
            priority = ChangePriority(priority)

        return [
            request
            for request in self.requests
            if request.priority == priority
        ]

    def by_impact(
        self,
        impact: ChangeImpact,
    ) -> list[ChangeRequest]:
        """Return requests matching an impact level."""

        if not isinstance(impact, ChangeImpact):
            impact = ChangeImpact(impact)

        return [
            request
            for request in self.requests
            if request.impact == impact
        ]

    def pending(self) -> list[ChangeRequest]:
        """Return requests awaiting a decision."""

        return [
            request
            for request in self.requests
            if request.is_pending()
        ]

    def approved(self) -> list[ChangeRequest]:
        """Return approved requests."""

        return self.by_status(ChangeStatus.APPROVED)

    def rejected(self) -> list[ChangeRequest]:
        """Return rejected requests."""

        return self.by_status(ChangeStatus.REJECTED)

    def with_quality_issues(self) -> dict[str, list[str]]:
        """Return requests with possible quality issues."""

        return {
            request.change_id: request.quality_issues()
            for request in self.requests
            if request.quality_issues()
        }

    # --------------------------------------------------------
    # IMPACT ANALYSIS
    # --------------------------------------------------------

    def affecting_requirement(
        self,
        requirement_id: str,
    ) -> list[ChangeRequest]:
        """Find change requests affecting a requirement."""

        requirement_id = str(requirement_id).strip().upper()

        return [
            request
            for request in self.requests
            if requirement_id in request.affected_requirements
        ]

    def affecting_use_case(
        self,
        use_case_id: str,
    ) -> list[ChangeRequest]:
        """Find change requests affecting a use case."""

        use_case_id = str(use_case_id).strip().upper()

        return [
            request
            for request in self.requests
            if use_case_id in request.affected_use_cases
        ]

    def affecting_test_case(
        self,
        test_case_id: str,
    ) -> list[ChangeRequest]:
        """Find change requests affecting a test case."""

        test_case_id = str(test_case_id).strip().upper()

        return [
            request
            for request in self.requests
            if test_case_id in request.affected_test_cases
        ]

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    def count_by_status(self) -> dict[str, int]:
        """Count requests by status."""

        return {
            status.value: sum(
                1 for request in self.requests
                if request.status == status
            )
            for status in ChangeStatus
        }

    def count_by_priority(self) -> dict[str, int]:
        """Count requests by priority."""

        return {
            priority.value: sum(
                1 for request in self.requests
                if request.priority == priority
            )
            for priority in ChangePriority
        }

    def count_by_impact(self) -> dict[str, int]:
        """Count requests by impact."""

        return {
            impact.value: sum(
                1 for request in self.requests
                if request.impact == impact
            )
            for impact in ChangeImpact
        }

    def __len__(self) -> int:
        return len(self.requests)

    def __iter__(self):
        return iter(self.requests)

    def __contains__(self, change_id: str) -> bool:
        return self.get(change_id) is not None

    def __str__(self) -> str:
        return (
            f"ChangeRequestSet(name='{self.name}', "
            f"total={len(self.requests)})"
        )