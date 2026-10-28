"""
Requirement Models for University Library Management System Online (ULMS).

This module defines:
- RequirementType: Categories of software requirements.
- Priority: Requirement priority levels.
- RequirementStatus: Requirement lifecycle statuses.
- Requirement: Represents one software requirement.
- RequirementSet: Manages a collection of software requirements.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


# ============================================================
# 1. REQUIREMENT TYPE
# ============================================================

class RequirementType(Enum):
    """Categories of requirements used in the ULMS project."""

    BUSINESS = "Business"
    STAKEHOLDER = "Stakeholder"
    FUNCTIONAL = "Functional"
    NON_FUNCTIONAL = "Non-Functional"
    CONSTRAINT = "Constraint"
    BUSINESS_RULE = "Business Rule"


# ============================================================
# 2. PRIORITY
# ============================================================

class Priority(Enum):
    """Priority levels for software requirements."""

    MUST = "Must"
    SHOULD = "Should"
    COULD = "Could"
    WONT = "Won't"


# ============================================================
# 3. REQUIREMENT STATUS
# ============================================================

class RequirementStatus(Enum):
    """Lifecycle statuses of a software requirement."""

    PROPOSED = "Proposed"
    APPROVED = "Approved"
    IMPLEMENTED = "Implemented"
    VERIFIED = "Verified"
    DEFERRED = "Deferred"
    REJECTED = "Rejected"


# ============================================================
# 4. REQUIREMENT MODEL
# ============================================================

@dataclass
class Requirement:
    """
    Represent one software requirement in the ULMS project.

    Attributes:
        req_id: Unique requirement identifier, e.g. REQ-01.
        title: Short name of the requirement.
        statement: Detailed requirement statement.
        req_type: Category of the requirement.
        priority: Importance of the requirement.
        status: Current lifecycle status.
        source: Person or stakeholder who provided the requirement.
        rationale: Reason why the requirement is needed.
        owner: Person responsible for the requirement.
        release: Planned release or version.
        acceptance_criteria: Conditions for accepting the requirement.
        verification_method: Method used to verify the requirement.
        complexity: Estimated implementation complexity.
        dependencies: IDs of requirements this requirement depends on.
        tags: Keywords used to categorize the requirement.
    """

    req_id: str
    title: str
    statement: str
    req_type: RequirementType

    priority: Priority = Priority.SHOULD
    status: RequirementStatus = RequirementStatus.PROPOSED

    source: str = ""
    rationale: str = ""
    owner: str = ""
    release: str = ""

    acceptance_criteria: str = ""
    verification_method: str = "Test"

    complexity: str = ""
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Normalize and validate requirement data."""

        # Validate required text fields.
        if not isinstance(self.req_id, str):
            raise TypeError("Requirement ID must be a string.")

        if not isinstance(self.title, str):
            raise TypeError("Requirement title must be a string.")

        if not isinstance(self.statement, str):
            raise TypeError("Requirement statement must be a string.")

        # Normalize basic text fields.
        self.req_id = self.req_id.strip().upper()
        self.title = self.title.strip()
        self.statement = self.statement.strip()

        # Check required fields.
        if not self.req_id:
            raise ValueError("Requirement ID cannot be empty.")

        if not self.title:
            raise ValueError("Requirement title cannot be empty.")

        if not self.statement:
            raise ValueError("Requirement statement cannot be empty.")

        # Validate enum fields.
        if not isinstance(self.req_type, RequirementType):
            raise TypeError(
                "req_type must be a RequirementType value."
            )

        if not isinstance(self.priority, Priority):
            raise TypeError(
                "priority must be a Priority value."
            )

        if not isinstance(self.status, RequirementStatus):
            raise TypeError(
                "status must be a RequirementStatus value."
            )

        # Validate and normalize dependencies.
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

        # Validate and normalize tags.
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
    # REQUIREMENT VALIDATION
    # --------------------------------------------------------

    def is_testable(self) -> bool:
        """
        Perform a preliminary check of requirement testability.

        A requirement is considered potentially testable when:
        - Its statement contains the word 'shall'.
        - Its statement does not contain common vague expressions.

        This is a heuristic check, not a complete quality assessment.
        """

        statement = self.statement.lower()

        vague_terms = [
            "quickly",
            "fast",
            "slow",
            "user-friendly",
            "easy to use",
            "flexible",
            "robust",
            "efficient",
            "optimal",
            "appropriate",
            "as needed",
            "etc.",
        ]

        if "shall" not in statement:
            return False

        if any(term in statement for term in vague_terms):
            return False

        return True

    def is_complete(self) -> bool:
        """
        Check whether the main required information is available.
        """

        return all([
            self.req_id,
            self.title,
            self.statement,
            self.req_type,
            self.priority,
            self.status,
            self.verification_method.strip(),
        ])

    def has_dependencies(self) -> bool:
        """Return True if the requirement has dependencies."""

        return len(self.dependencies) > 0

    def has_self_dependency(self) -> bool:
        """Check whether the requirement depends on itself."""

        return self.req_id in self.dependencies

    # --------------------------------------------------------
    # DATA CONVERSION
    # --------------------------------------------------------

    def to_dict(self) -> dict:
        """Convert the requirement into a dictionary."""

        return {
            "id": self.req_id,
            "title": self.title,
            "description": self.statement,
            "type": self.req_type.value,
            "priority": self.priority.value,
            "status": self.status.value,
            "source": self.source,
            "rationale": self.rationale,
            "owner": self.owner,
            "release": self.release,
            "acceptance_criteria": self.acceptance_criteria,
            "verification_method": self.verification_method,
            "complexity": self.complexity,
            "dependencies": ";".join(self.dependencies),
            "tags": ";".join(self.tags),
        }

    def __str__(self) -> str:
        """Return a readable representation of the requirement."""

        return (
            f"[{self.req_id}] {self.title} "
            f"({self.req_type.value}, "
            f"{self.priority.value}, "
            f"{self.status.value})"
        )


# ============================================================
# 5. REQUIREMENT SET
# ============================================================

@dataclass
class RequirementSet:
    """
    Manage a collection of requirements for the ULMS project.

    The class provides operations for adding, finding, removing,
    filtering, and counting requirements.
    """

    name: str
    requirements: List[Requirement] = field(default_factory=list)

    def __post_init__(self):
        """Validate and normalize the requirement collection."""

        if not isinstance(self.name, str):
            raise TypeError("Requirement set name must be a string.")

        self.name = self.name.strip()

        if not self.name:
            raise ValueError("Requirement set name cannot be empty.")

        if not isinstance(self.requirements, list):
            raise TypeError("Requirements must be provided as a list.")

        # Validate requirements and prevent duplicate IDs.
        original_requirements = list(self.requirements)
        self.requirements = []

        for requirement in original_requirements:
            self.add(requirement)

    # --------------------------------------------------------
    # ADD REQUIREMENTS
    # --------------------------------------------------------

    def add(self, requirement: Requirement) -> None:
        """Add a requirement while preventing duplicate IDs."""

        if not isinstance(requirement, Requirement):
            raise TypeError(
                "Only Requirement objects can be added."
            )

        if self.get(requirement.req_id) is not None:
            raise ValueError(
                f"Duplicate requirement ID: {requirement.req_id}"
            )

        self.requirements.append(requirement)

    # --------------------------------------------------------
    # FIND AND REMOVE REQUIREMENTS
    # --------------------------------------------------------

    def get(self, req_id: str) -> Optional[Requirement]:
        """Find a requirement by its ID."""

        if not isinstance(req_id, str):
            return None

        normalized_id = req_id.strip().upper()

        for requirement in self.requirements:
            if requirement.req_id == normalized_id:
                return requirement

        return None

    def remove(self, req_id: str) -> bool:
        """
        Remove a requirement by its ID.

        Returns:
            True if the requirement was removed; otherwise False.
        """

        requirement = self.get(req_id)

        if requirement is None:
            return False

        self.requirements.remove(requirement)
        return True

    # --------------------------------------------------------
    # FILTER REQUIREMENTS
    # --------------------------------------------------------

    def by_type(
        self,
        req_type: RequirementType
    ) -> List[Requirement]:
        """Return requirements matching a specific type."""

        return [
            requirement
            for requirement in self.requirements
            if requirement.req_type == req_type
        ]

    def by_priority(
        self,
        priority: Priority
    ) -> List[Requirement]:
        """Return requirements matching a specific priority."""

        return [
            requirement
            for requirement in self.requirements
            if requirement.priority == priority
        ]

    def by_status(
        self,
        status: RequirementStatus
    ) -> List[Requirement]:
        """Return requirements matching a specific status."""

        return [
            requirement
            for requirement in self.requirements
            if requirement.status == status
        ]

    # --------------------------------------------------------
    # REQUIREMENT QUALITY CHECKS
    # --------------------------------------------------------

    def untestable(self) -> List[Requirement]:
        """Return requirements failing the basic testability check."""

        return [
            requirement
            for requirement in self.requirements
            if not requirement.is_testable()
        ]

    def incomplete(self) -> List[Requirement]:
        """Return requirements missing basic required information."""

        return [
            requirement
            for requirement in self.requirements
            if not requirement.is_complete()
        ]

    def with_self_dependencies(self) -> List[Requirement]:
        """Return requirements that depend on themselves."""

        return [
            requirement
            for requirement in self.requirements
            if requirement.has_self_dependency()
        ]

    def duplicate_ids(self) -> List[str]:
        """
        Return duplicate IDs if duplicates exist in the collection.

        Normally, add() prevents duplicate IDs, so this method
        is mainly useful for additional integrity checks.
        """

        seen = set()
        duplicates = set()

        for requirement in self.requirements:
            if requirement.req_id in seen:
                duplicates.add(requirement.req_id)

            seen.add(requirement.req_id)

        return sorted(duplicates)

    # --------------------------------------------------------
    # REQUIREMENT STATISTICS
    # --------------------------------------------------------

    def count_by_priority(self) -> dict:
        """Count requirements by priority."""

        return {
            priority.value: len(self.by_priority(priority))
            for priority in Priority
        }

    def count_by_status(self) -> dict:
        """Count requirements by status."""

        return {
            status.value: len(self.by_status(status))
            for status in RequirementStatus
        }

    def count_by_type(self) -> dict:
        """Count requirements by type."""

        return {
            req_type.value: len(self.by_type(req_type))
            for req_type in RequirementType
        }

    # --------------------------------------------------------
    # COLLECTION OPERATIONS
    # --------------------------------------------------------

    def __len__(self) -> int:
        """Return the total number of requirements."""

        return len(self.requirements)

    def __iter__(self):
        """Allow iteration over the requirements."""

        return iter(self.requirements)

    def __contains__(self, req_id: str) -> bool:
        """Check whether a requirement ID exists in the set."""

        return self.get(req_id) is not None

    def __str__(self) -> str:
        """Return a readable summary of the requirement set."""

        return (
            f"RequirementSet(name='{self.name}', "
            f"total_requirements={len(self.requirements)})"
        )