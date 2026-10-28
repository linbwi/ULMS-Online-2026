"""
Non-Functional Requirements Module for
University Library Management System Online (ULMS).

This module provides models and operations for managing,
classifying, and validating non-functional requirements.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


# ============================================================
# 1. NFR CATEGORY
# ============================================================

class NFRCategory(Enum):
    """Categories of non-functional requirements."""

    PERFORMANCE = "Performance"
    SECURITY = "Security"
    USABILITY = "Usability"
    RELIABILITY = "Reliability"
    AVAILABILITY = "Availability"
    SCALABILITY = "Scalability"
    MAINTAINABILITY = "Maintainability"
    COMPATIBILITY = "Compatibility"
    ACCESSIBILITY = "Accessibility"
    DATA_INTEGRITY = "Data Integrity"
    PRIVACY = "Privacy"
    OTHER = "Other"


# ============================================================
# 2. NFR PRIORITY
# ============================================================

class NFRPriority(Enum):
    """Priority levels for non-functional requirements."""

    MUST = "Must"
    SHOULD = "Should"
    COULD = "Could"
    WONT = "Won't"


# ============================================================
# 3. NFR STATUS
# ============================================================

class NFRStatus(Enum):
    """Lifecycle statuses of non-functional requirements."""

    PROPOSED = "Proposed"
    APPROVED = "Approved"
    IMPLEMENTED = "Implemented"
    VERIFIED = "Verified"
    DEFERRED = "Deferred"
    REJECTED = "Rejected"


# ============================================================
# 4. NFR MODEL
# ============================================================

@dataclass
class NFR:
    """
    Represent one non-functional requirement in the ULMS project.

    Attributes:
        nfr_id: Unique NFR identifier, e.g. NFR-01.
        title: Short title of the NFR.
        statement: Detailed requirement statement.
        category: Quality attribute addressed by the NFR.
        priority: Importance of the NFR.
        status: Current lifecycle status.
        metric: Measurable performance or quality metric.
        target_value: Required measurable target.
        measurement_unit: Unit used to measure the target.
        verification_method: Method used to verify the NFR.
        source: Stakeholder or source that provided the NFR.
        rationale: Reason why the NFR is needed.
        acceptance_criteria: Conditions for accepting the NFR.
        dependencies: IDs of related requirements.
        tags: Keywords used to categorize the NFR.
    """

    nfr_id: str
    title: str
    statement: str
    category: NFRCategory

    priority: NFRPriority = NFRPriority.SHOULD
    status: NFRStatus = NFRStatus.PROPOSED

    metric: str = ""
    target_value: str = ""
    measurement_unit: str = ""

    verification_method: str = "Test"
    source: str = ""
    rationale: str = ""
    acceptance_criteria: str = ""

    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Normalize and validate NFR data."""

        # Validate required text fields.
        if not isinstance(self.nfr_id, str):
            raise TypeError("NFR ID must be a string.")

        if not isinstance(self.title, str):
            raise TypeError("NFR title must be a string.")

        if not isinstance(self.statement, str):
            raise TypeError("NFR statement must be a string.")

        # Normalize text fields.
        self.nfr_id = self.nfr_id.strip().upper()
        self.title = self.title.strip()
        self.statement = self.statement.strip()

        # Validate required fields.
        if not self.nfr_id:
            raise ValueError("NFR ID cannot be empty.")

        if not self.title:
            raise ValueError("NFR title cannot be empty.")

        if not self.statement:
            raise ValueError("NFR statement cannot be empty.")

        # Validate enumeration values.
        if not isinstance(self.category, NFRCategory):
            raise TypeError(
                "category must be an NFRCategory value."
            )

        if not isinstance(self.priority, NFRPriority):
            raise TypeError(
                "priority must be an NFRPriority value."
            )

        if not isinstance(self.status, NFRStatus):
            raise TypeError(
                "status must be an NFRStatus value."
            )

        # Normalize dependencies.
        if not isinstance(self.dependencies, list):
            raise TypeError("Dependencies must be a list.")

        normalized_dependencies = []

        for dependency in self.dependencies:
            if not isinstance(dependency, str):
                raise TypeError(
                    "Each dependency ID must be a string."
                )

            dependency_id = dependency.strip().upper()

            if dependency_id:
                normalized_dependencies.append(dependency_id)

        self.dependencies = normalized_dependencies

        # Normalize tags.
        if not isinstance(self.tags, list):
            raise TypeError("Tags must be a list.")

        normalized_tags = []

        for tag in self.tags:
            if not isinstance(tag, str):
                raise TypeError("Each tag must be a string.")

            normalized_tag = tag.strip()

            if normalized_tag:
                normalized_tags.append(normalized_tag)

        self.tags = normalized_tags

    # --------------------------------------------------------
    # NFR QUALITY CHECKS
    # --------------------------------------------------------

    def has_metric(self) -> bool:
        """Return True if a measurement metric is specified."""

        return bool(self.metric.strip())

    def has_target(self) -> bool:
        """Return True if a target value is specified."""

        return bool(self.target_value.strip())

    def is_measurable(self) -> bool:
        """
        Check whether the NFR has a metric and a target value.

        This is a basic structural check. It does not guarantee
        that the target is realistic or sufficiently precise.
        """

        return self.has_metric() and self.has_target()

    def is_verifiable(self) -> bool:
        """Check whether a verification method is specified."""

        return bool(self.verification_method.strip())

    def is_complete(self) -> bool:
        """Check whether the main NFR information is provided."""

        return all([
            self.nfr_id,
            self.title,
            self.statement,
            self.category,
            self.priority,
            self.status,
            self.verification_method.strip(),
        ])

    def has_dependencies(self) -> bool:
        """Return True if the NFR has dependencies."""

        return len(self.dependencies) > 0

    def has_self_dependency(self) -> bool:
        """Check whether the NFR depends on itself."""

        return self.nfr_id in self.dependencies

    def quality_issues(self) -> List[str]:
        """
        Return a list of potential NFR quality issues.

        These checks are preliminary and do not replace
        manual review by the project team.
        """

        issues = []

        if not self.is_measurable():
            issues.append(
                "A measurable metric and target value should be specified."
            )

        if not self.is_verifiable():
            issues.append(
                "A verification method should be specified."
            )

        if not self.acceptance_criteria.strip():
            issues.append(
                "Acceptance criteria have not been specified."
            )

        if self.has_self_dependency():
            issues.append(
                "The NFR depends on itself."
            )

        return issues

    # --------------------------------------------------------
    # DATA CONVERSION
    # --------------------------------------------------------

    def to_dict(self) -> dict:
        """Convert the NFR into a dictionary."""

        return {
            "nfr_id": self.nfr_id,
            "title": self.title,
            "statement": self.statement,
            "category": self.category.value,
            "priority": self.priority.value,
            "status": self.status.value,
            "metric": self.metric,
            "target_value": self.target_value,
            "measurement_unit": self.measurement_unit,
            "verification_method": self.verification_method,
            "source": self.source,
            "rationale": self.rationale,
            "acceptance_criteria": self.acceptance_criteria,
            "dependencies": ";".join(self.dependencies),
            "tags": ";".join(self.tags),
        }

    def __str__(self) -> str:
        """Return a readable representation of the NFR."""

        return (
            f"[{self.nfr_id}] {self.title} "
            f"({self.category.value}, "
            f"{self.priority.value}, "
            f"{self.status.value})"
        )


# ============================================================
# 5. NFR SET
# ============================================================

@dataclass
class NFRSet:
    """
    Manage a collection of non-functional requirements.
    """

    name: str
    nfrs: List[NFR] = field(default_factory=list)

    def __post_init__(self):
        """Validate the collection and prevent duplicate IDs."""

        if not isinstance(self.name, str):
            raise TypeError("NFR set name must be a string.")

        self.name = self.name.strip()

        if not self.name:
            raise ValueError("NFR set name cannot be empty.")

        if not isinstance(self.nfrs, list):
            raise TypeError("NFRs must be provided as a list.")

        initial_nfrs = list(self.nfrs)
        self.nfrs = []

        for nfr in initial_nfrs:
            self.add(nfr)

    # --------------------------------------------------------
    # ADD NFR
    # --------------------------------------------------------

    def add(self, nfr: NFR) -> None:
        """Add an NFR while preventing duplicate IDs."""

        if not isinstance(nfr, NFR):
            raise TypeError("Only NFR objects can be added.")

        if self.get(nfr.nfr_id) is not None:
            raise ValueError(
                f"Duplicate NFR ID: {nfr.nfr_id}"
            )

        self.nfrs.append(nfr)

    # --------------------------------------------------------
    # FIND AND REMOVE NFR
    # --------------------------------------------------------

    def get(self, nfr_id: str) -> Optional[NFR]:
        """Find an NFR by its ID."""

        if not isinstance(nfr_id, str):
            return None

        normalized_id = nfr_id.strip().upper()

        for nfr in self.nfrs:
            if nfr.nfr_id == normalized_id:
                return nfr

        return None

    def remove(self, nfr_id: str) -> bool:
        """Remove an NFR by its ID."""

        nfr = self.get(nfr_id)

        if nfr is None:
            return False

        self.nfrs.remove(nfr)
        return True

    # --------------------------------------------------------
    # FILTER NFRS
    # --------------------------------------------------------

    def by_category(
        self,
        category: NFRCategory
    ) -> List[NFR]:
        """Return NFRs matching a specific category."""

        return [
            nfr for nfr in self.nfrs
            if nfr.category == category
        ]

    def by_priority(
        self,
        priority: NFRPriority
    ) -> List[NFR]:
        """Return NFRs matching a specific priority."""

        return [
            nfr for nfr in self.nfrs
            if nfr.priority == priority
        ]

    def by_status(
        self,
        status: NFRStatus
    ) -> List[NFR]:
        """Return NFRs matching a specific status."""

        return [
            nfr for nfr in self.nfrs
            if nfr.status == status
        ]

    # --------------------------------------------------------
    # NFR QUALITY ANALYSIS
    # --------------------------------------------------------

    def unmeasurable(self) -> List[NFR]:
        """Return NFRs without both a metric and target."""

        return [
            nfr for nfr in self.nfrs
            if not nfr.is_measurable()
        ]

    def incomplete(self) -> List[NFR]:
        """Return NFRs missing basic required information."""

        return [
            nfr for nfr in self.nfrs
            if not nfr.is_complete()
        ]

    def with_quality_issues(self) -> List[NFR]:
        """Return NFRs with one or more potential quality issues."""

        return [
            nfr for nfr in self.nfrs
            if nfr.quality_issues()
        ]

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    def count_by_category(self) -> dict:
        """Count NFRs by category."""

        return {
            category.value: len(self.by_category(category))
            for category in NFRCategory
        }

    def count_by_priority(self) -> dict:
        """Count NFRs by priority."""

        return {
            priority.value: len(self.by_priority(priority))
            for priority in NFRPriority
        }

    def count_by_status(self) -> dict:
        """Count NFRs by status."""

        return {
            status.value: len(self.by_status(status))
            for status in NFRStatus
        }

    # --------------------------------------------------------
    # COLLECTION OPERATIONS
    # --------------------------------------------------------

    def __len__(self) -> int:
        """Return the total number of NFRs."""

        return len(self.nfrs)

    def __iter__(self):
        """Allow iteration over the NFR collection."""

        return iter(self.nfrs)

    def __contains__(self, nfr_id: str) -> bool:
        """Check whether an NFR ID exists in the collection."""

        return self.get(nfr_id) is not None

    def __str__(self) -> str:
        """Return a readable summary of the NFR collection."""

        return (
            f"NFRSet(name='{self.name}', "
            f"total_nfrs={len(self.nfrs)})"
        )