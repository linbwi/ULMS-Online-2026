"""
Use Case Management Module for University Library Management System Online.

This module provides:
- Use Case data models
- Actor and scenario management
- Preconditions and postconditions
- Main and alternative flows
- Use Case validation
- Use Case collection management
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ============================================================
# 1. ENUMS
# ============================================================

class UseCasePriority(Enum):
    """Priority levels for use cases."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class UseCaseStatus(Enum):
    """Lifecycle status of a use case."""
    PROPOSED = "Proposed"
    APPROVED = "Approved"
    IMPLEMENTED = "Implemented"
    VERIFIED = "Verified"
    DEFERRED = "Deferred"
    REJECTED = "Rejected"


# ============================================================
# 2. USE CASE CLASS
# ============================================================

@dataclass
class UseCase:
    """
    Represents a use case in the ULMS Online system.

    Attributes:
        use_case_id: Unique identifier, e.g. UC-01.
        name: Short use case name.
        description: Brief description of the use case.
        primary_actor: Main actor initiating the use case.
        secondary_actors: Other actors or external systems involved.
        preconditions: Conditions that must hold before execution.
        postconditions: Conditions that should hold after execution.
        main_flow: Normal sequence of interactions.
        alternative_flows: Alternative or exceptional sequences.
        priority: Business priority.
        status: Current lifecycle status.
        related_requirements: IDs of related requirements.
        notes: Additional information.
    """

    use_case_id: str
    name: str
    description: str
    primary_actor: str

    secondary_actors: list[str] = field(default_factory=list)
    preconditions: list[str] = field(default_factory=list)
    postconditions: list[str] = field(default_factory=list)
    main_flow: list[str] = field(default_factory=list)
    alternative_flows: list[str] = field(default_factory=list)

    priority: UseCasePriority = UseCasePriority.MEDIUM
    status: UseCaseStatus = UseCaseStatus.PROPOSED

    related_requirements: list[str] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self):
        """Normalize values and validate required fields."""
        self.use_case_id = str(self.use_case_id).strip().upper()
        self.name = str(self.name).strip()
        self.description = str(self.description).strip()
        self.primary_actor = str(self.primary_actor).strip()

        if not self.use_case_id:
            raise ValueError("Use case ID cannot be empty.")

        if not self.name:
            raise ValueError("Use case name cannot be empty.")

        if not self.description:
            raise ValueError("Use case description cannot be empty.")

        if not self.primary_actor:
            raise ValueError("Primary actor cannot be empty.")

        # Normalize list attributes.
        self.secondary_actors = self._normalize_list(self.secondary_actors)
        self.preconditions = self._normalize_list(self.preconditions)
        self.postconditions = self._normalize_list(self.postconditions)
        self.main_flow = self._normalize_list(self.main_flow)
        self.alternative_flows = self._normalize_list(self.alternative_flows)
        self.related_requirements = [
            item.upper()
            for item in self._normalize_list(self.related_requirements)
        ]

        self.notes = str(self.notes).strip()

        # Validate enum fields.
        if not isinstance(self.priority, UseCasePriority):
            try:
                self.priority = UseCasePriority(self.priority)
            except ValueError:
                raise ValueError(
                    f"Invalid use case priority: {self.priority}"
                )

        if not isinstance(self.status, UseCaseStatus):
            try:
                self.status = UseCaseStatus(self.status)
            except ValueError:
                raise ValueError(
                    f"Invalid use case status: {self.status}"
                )

    @staticmethod
    def _normalize_list(values) -> list[str]:
        """Convert a list of values into a clean list of strings."""
        if values is None:
            return []

        if isinstance(values, str):
            values = [values]

        if not isinstance(values, (list, tuple, set)):
            raise ValueError("Expected a list of strings.")

        return [
            str(value).strip()
            for value in values
            if value is not None and str(value).strip()
        ]

    # --------------------------------------------------------
    # USE CASE QUALITY CHECKS
    # --------------------------------------------------------

    def has_main_flow(self) -> bool:
        """Return True if the use case has a main flow."""
        return len(self.main_flow) > 0

    def has_preconditions(self) -> bool:
        """Return True if the use case defines preconditions."""
        return len(self.preconditions) > 0

    def has_postconditions(self) -> bool:
        """Return True if the use case defines postconditions."""
        return len(self.postconditions) > 0

    def has_related_requirements(self) -> bool:
        """Return True if related requirements are specified."""
        return len(self.related_requirements) > 0

    def is_complete(self) -> bool:
        """
        Check whether the use case has its essential information.

        This is a basic completeness check, not a guarantee that
        the use case is correct or fully specified.
        """
        return all([
            self.use_case_id,
            self.name,
            self.description,
            self.primary_actor,
            self.has_main_flow(),
            self.has_postconditions(),
        ])

    def quality_issues(self) -> list[str]:
        """Return a list of possible completeness issues."""
        issues = []

        if not self.name:
            issues.append("Use case name is missing.")

        if not self.description:
            issues.append("Use case description is missing.")

        if not self.primary_actor:
            issues.append("Primary actor is missing.")

        if not self.preconditions:
            issues.append("Preconditions are not specified.")

        if not self.main_flow:
            issues.append("Main flow is not specified.")

        if not self.postconditions:
            issues.append("Postconditions are not specified.")

        if not self.related_requirements:
            issues.append("Related requirements are not specified.")

        return issues

    # --------------------------------------------------------
    # CONVERSION
    # --------------------------------------------------------

    def to_dict(self) -> dict:
        """Convert the use case to a dictionary."""
        return {
            "use_case_id": self.use_case_id,
            "name": self.name,
            "description": self.description,
            "primary_actor": self.primary_actor,
            "secondary_actors": self.secondary_actors.copy(),
            "preconditions": self.preconditions.copy(),
            "postconditions": self.postconditions.copy(),
            "main_flow": self.main_flow.copy(),
            "alternative_flows": self.alternative_flows.copy(),
            "priority": self.priority.value,
            "status": self.status.value,
            "related_requirements": self.related_requirements.copy(),
            "notes": self.notes,
        }

    def __str__(self) -> str:
        """Return a readable summary."""
        return (
            f"{self.use_case_id}: {self.name} "
            f"[Priority: {self.priority.value}, "
            f"Status: {self.status.value}]"
        )


# ============================================================
# 3. USE CASE COLLECTION
# ============================================================

@dataclass
class UseCaseSet:
    """Manage a collection of use cases."""

    name: str
    use_cases: list[UseCase] = field(default_factory=list)

    def __post_init__(self):
        self.name = str(self.name).strip()

        if not self.name:
            raise ValueError("Use case set name cannot be empty.")

        if not isinstance(self.use_cases, list):
            raise ValueError("use_cases must be a list.")

        existing_ids = set()

        for use_case in self.use_cases:
            if not isinstance(use_case, UseCase):
                raise TypeError(
                    "Every item in use_cases must be a UseCase object."
                )

            if use_case.use_case_id in existing_ids:
                raise ValueError(
                    f"Duplicate use case ID: {use_case.use_case_id}"
                )

            existing_ids.add(use_case.use_case_id)

    # --------------------------------------------------------
    # CRUD OPERATIONS
    # --------------------------------------------------------

    def add(self, use_case: UseCase) -> None:
        """Add a use case if its ID is unique."""
        if not isinstance(use_case, UseCase):
            raise TypeError("use_case must be a UseCase object.")

        if self.get(use_case.use_case_id) is not None:
            raise ValueError(
                f"Use case ID already exists: {use_case.use_case_id}"
            )

        self.use_cases.append(use_case)

    def get(self, use_case_id: str) -> Optional[UseCase]:
        """Find a use case by ID."""
        target_id = str(use_case_id).strip().upper()

        for use_case in self.use_cases:
            if use_case.use_case_id == target_id:
                return use_case

        return None

    def remove(self, use_case_id: str) -> bool:
        """Remove a use case by ID. Return True if removed."""
        use_case = self.get(use_case_id)

        if use_case is None:
            return False

        self.use_cases.remove(use_case)
        return True

    # --------------------------------------------------------
    # FILTERING
    # --------------------------------------------------------

    def by_priority(self, priority: UseCasePriority) -> list[UseCase]:
        """Return use cases matching a priority."""
        if not isinstance(priority, UseCasePriority):
            priority = UseCasePriority(priority)

        return [
            use_case
            for use_case in self.use_cases
            if use_case.priority == priority
        ]

    def by_status(self, status: UseCaseStatus) -> list[UseCase]:
        """Return use cases matching a status."""
        if not isinstance(status, UseCaseStatus):
            status = UseCaseStatus(status)

        return [
            use_case
            for use_case in self.use_cases
            if use_case.status == status
        ]

    def by_actor(self, actor: str) -> list[UseCase]:
        """Return use cases involving the specified actor."""
        target_actor = str(actor).strip().casefold()

        return [
            use_case
            for use_case in self.use_cases
            if (
                use_case.primary_actor.casefold() == target_actor
                or any(
                    item.casefold() == target_actor
                    for item in use_case.secondary_actors
                )
            )
        ]

    def incomplete(self) -> list[UseCase]:
        """Return use cases that fail the basic completeness check."""
        return [
            use_case
            for use_case in self.use_cases
            if not use_case.is_complete()
        ]

    def with_quality_issues(self) -> dict[str, list[str]]:
        """Return quality issues grouped by use case ID."""
        return {
            use_case.use_case_id: use_case.quality_issues()
            for use_case in self.use_cases
            if use_case.quality_issues()
        }

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    def count_by_priority(self) -> dict[str, int]:
        """Count use cases by priority."""
        return {
            priority.value: sum(
                1 for use_case in self.use_cases
                if use_case.priority == priority
            )
            for priority in UseCasePriority
        }

    def count_by_status(self) -> dict[str, int]:
        """Count use cases by status."""
        return {
            status.value: sum(
                1 for use_case in self.use_cases
                if use_case.status == status
            )
            for status in UseCaseStatus
        }

    def __len__(self) -> int:
        return len(self.use_cases)

    def __iter__(self):
        return iter(self.use_cases)

    def __contains__(self, use_case_id: str) -> bool:
        return self.get(use_case_id) is not None

    def __str__(self) -> str:
        return (
            f"UseCaseSet(name='{self.name}', "
            f"total={len(self.use_cases)})"
        )