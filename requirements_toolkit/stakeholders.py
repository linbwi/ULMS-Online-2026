"""
Stakeholder Management Module for
University Library Management System Online (ULMS).

This module provides classes for representing, managing,
classifying, and analyzing project stakeholders.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


# ============================================================
# 1. STAKEHOLDER ROLE
# ============================================================

class StakeholderRole(Enum):
    """Roles of stakeholders in the ULMS project."""

    STUDENT = "Student"
    LECTURER = "Lecturer"
    LIBRARIAN = "Librarian"
    LIBRARY_MANAGER = "Library Manager"
    SYSTEM_ADMIN = "System Administrator"
    DEVELOPER = "Developer"
    PROJECT_MANAGER = "Project Manager"
    IT_SUPPORT = "IT Support"
    UNIVERSITY_MANAGEMENT = "University Management"
    EXTERNAL_SYSTEM = "External System"
    OTHER = "Other"


# ============================================================
# 2. STAKEHOLDER TYPE
# ============================================================

class StakeholderType(Enum):
    """Classification of stakeholders."""

    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    INTERNAL = "Internal"
    EXTERNAL = "External"


# ============================================================
# 3. STAKEHOLDER PRIORITY
# ============================================================

class StakeholderPriority(Enum):
    """Priority levels for stakeholder engagement."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


# ============================================================
# 4. STAKEHOLDER MODEL
# ============================================================

@dataclass
class Stakeholder:
    """
    Represent one stakeholder in the ULMS project.

    Attributes:
        stakeholder_id: Unique stakeholder identifier.
        name: Stakeholder name or group name.
        role: Role played in the project.
        stakeholder_type: Primary, secondary, internal, or external.
        interest: Level of interest in the project (1-5).
        influence: Level of influence over the project (1-5).
        responsibilities: Responsibilities related to the system.
        needs: Main needs or expectations.
        contact: Optional contact information.
        priority: Stakeholder engagement priority.
        notes: Additional information.
    """

    stakeholder_id: str
    name: str
    role: StakeholderRole

    stakeholder_type: StakeholderType = StakeholderType.PRIMARY

    interest: int = 3
    influence: int = 3

    responsibilities: str = ""
    needs: str = ""
    contact: str = ""

    priority: StakeholderPriority = StakeholderPriority.MEDIUM
    notes: str = ""

    def __post_init__(self):
        """Normalize and validate stakeholder information."""

        # Validate text fields.
        if not isinstance(self.stakeholder_id, str):
            raise TypeError("Stakeholder ID must be a string.")

        if not isinstance(self.name, str):
            raise TypeError("Stakeholder name must be a string.")

        # Normalize text fields.
        self.stakeholder_id = self.stakeholder_id.strip().upper()
        self.name = self.name.strip()

        # Check required fields.
        if not self.stakeholder_id:
            raise ValueError("Stakeholder ID cannot be empty.")

        if not self.name:
            raise ValueError("Stakeholder name cannot be empty.")

        # Validate enum fields.
        if not isinstance(self.role, StakeholderRole):
            raise TypeError(
                "role must be a StakeholderRole value."
            )

        if not isinstance(self.stakeholder_type, StakeholderType):
            raise TypeError(
                "stakeholder_type must be a StakeholderType value."
            )

        if not isinstance(self.priority, StakeholderPriority):
            raise TypeError(
                "priority must be a StakeholderPriority value."
            )

        # Validate interest and influence.
        if (
            not isinstance(self.interest, int)
            or isinstance(self.interest, bool)
            or not 1 <= self.interest <= 5
        ):
            raise ValueError(
                "Interest must be an integer between 1 and 5."
            )

        if (
            not isinstance(self.influence, int)
            or isinstance(self.influence, bool)
            or not 1 <= self.influence <= 5
        ):
            raise ValueError(
                "Influence must be an integer between 1 and 5."
            )

    # --------------------------------------------------------
    # STAKEHOLDER ANALYSIS
    # --------------------------------------------------------

    def is_high_influence(self) -> bool:
        """Check whether the stakeholder has high influence."""

        return self.influence >= 4

    def is_high_interest(self) -> bool:
        """Check whether the stakeholder has high interest."""

        return self.interest >= 4

    def engagement_strategy(self) -> str:
        """
        Suggest an engagement strategy based on interest
        and influence.

        This is a basic stakeholder-analysis heuristic.
        """

        if self.is_high_influence() and self.is_high_interest():
            return "Manage closely"

        if self.is_high_influence() and not self.is_high_interest():
            return "Keep satisfied"

        if not self.is_high_influence() and self.is_high_interest():
            return "Keep informed"

        return "Monitor"

    def is_complete(self) -> bool:
        """Check whether the main stakeholder data is available."""

        return all([
            self.stakeholder_id,
            self.name,
            self.role,
            self.stakeholder_type,
            self.priority,
        ])

    # --------------------------------------------------------
    # DATA CONVERSION
    # --------------------------------------------------------

    def to_dict(self) -> dict:
        """Convert the stakeholder into a dictionary."""

        return {
            "stakeholder_id": self.stakeholder_id,
            "name": self.name,
            "role": self.role.value,
            "stakeholder_type": self.stakeholder_type.value,
            "interest": self.interest,
            "influence": self.influence,
            "responsibilities": self.responsibilities,
            "needs": self.needs,
            "contact": self.contact,
            "priority": self.priority.value,
            "engagement_strategy": self.engagement_strategy(),
            "notes": self.notes,
        }

    def __str__(self) -> str:
        """Return a readable representation of the stakeholder."""

        return (
            f"[{self.stakeholder_id}] {self.name} "
            f"({self.role.value}, "
            f"Interest={self.interest}, "
            f"Influence={self.influence})"
        )


# ============================================================
# 5. STAKEHOLDER SET
# ============================================================

@dataclass
class StakeholderSet:
    """
    Manage a collection of stakeholders in the ULMS project.
    """

    name: str
    stakeholders: List[Stakeholder] = field(default_factory=list)

    def __post_init__(self):
        """Validate the collection and prevent duplicate IDs."""

        if not isinstance(self.name, str):
            raise TypeError(
                "Stakeholder set name must be a string."
            )

        self.name = self.name.strip()

        if not self.name:
            raise ValueError(
                "Stakeholder set name cannot be empty."
            )

        if not isinstance(self.stakeholders, list):
            raise TypeError(
                "Stakeholders must be provided as a list."
            )

        initial_stakeholders = list(self.stakeholders)
        self.stakeholders = []

        for stakeholder in initial_stakeholders:
            self.add(stakeholder)

    # --------------------------------------------------------
    # ADD STAKEHOLDER
    # --------------------------------------------------------

    def add(self, stakeholder: Stakeholder) -> None:
        """Add a stakeholder while preventing duplicate IDs."""

        if not isinstance(stakeholder, Stakeholder):
            raise TypeError(
                "Only Stakeholder objects can be added."
            )

        if self.get(stakeholder.stakeholder_id) is not None:
            raise ValueError(
                "Duplicate stakeholder ID: "
                f"{stakeholder.stakeholder_id}"
            )

        self.stakeholders.append(stakeholder)

    # --------------------------------------------------------
    # FIND AND REMOVE STAKEHOLDERS
    # --------------------------------------------------------

    def get(self, stakeholder_id: str) -> Optional[Stakeholder]:
        """Find a stakeholder by ID."""

        if not isinstance(stakeholder_id, str):
            return None

        normalized_id = stakeholder_id.strip().upper()

        for stakeholder in self.stakeholders:
            if stakeholder.stakeholder_id == normalized_id:
                return stakeholder

        return None

    def remove(self, stakeholder_id: str) -> bool:
        """Remove a stakeholder by ID."""

        stakeholder = self.get(stakeholder_id)

        if stakeholder is None:
            return False

        self.stakeholders.remove(stakeholder)
        return True

    # --------------------------------------------------------
    # FILTER STAKEHOLDERS
    # --------------------------------------------------------

    def by_role(
        self,
        role: StakeholderRole
    ) -> List[Stakeholder]:
        """Return stakeholders with a specific role."""

        return [
            stakeholder
            for stakeholder in self.stakeholders
            if stakeholder.role == role
        ]

    def by_type(
        self,
        stakeholder_type: StakeholderType
    ) -> List[Stakeholder]:
        """Return stakeholders of a specific type."""

        return [
            stakeholder
            for stakeholder in self.stakeholders
            if stakeholder.stakeholder_type == stakeholder_type
        ]

    def by_priority(
        self,
        priority: StakeholderPriority
    ) -> List[Stakeholder]:
        """Return stakeholders with a specific priority."""

        return [
            stakeholder
            for stakeholder in self.stakeholders
            if stakeholder.priority == priority
        ]

    def high_influence(self) -> List[Stakeholder]:
        """Return stakeholders with high influence."""

        return [
            stakeholder
            for stakeholder in self.stakeholders
            if stakeholder.is_high_influence()
        ]

    def high_interest(self) -> List[Stakeholder]:
        """Return stakeholders with high interest."""

        return [
            stakeholder
            for stakeholder in self.stakeholders
            if stakeholder.is_high_interest()
        ]

    # --------------------------------------------------------
    # STAKEHOLDER STATISTICS
    # --------------------------------------------------------

    def count_by_role(self) -> dict:
        """Count stakeholders by role."""

        return {
            role.value: len(self.by_role(role))
            for role in StakeholderRole
        }

    def count_by_type(self) -> dict:
        """Count stakeholders by type."""

        return {
            stakeholder_type.value: len(
                self.by_type(stakeholder_type)
            )
            for stakeholder_type in StakeholderType
        }

    def count_by_priority(self) -> dict:
        """Count stakeholders by priority."""

        return {
            priority.value: len(self.by_priority(priority))
            for priority in StakeholderPriority
        }

    # --------------------------------------------------------
    # COLLECTION OPERATIONS
    # --------------------------------------------------------

    def __len__(self) -> int:
        """Return the total number of stakeholders."""

        return len(self.stakeholders)

    def __iter__(self):
        """Allow iteration over the stakeholder collection."""

        return iter(self.stakeholders)

    def __contains__(self, stakeholder_id: str) -> bool:
        """Check whether a stakeholder ID exists."""

        return self.get(stakeholder_id) is not None

    def __str__(self) -> str:
        """Return a readable summary of the stakeholder set."""

        return (
            f"StakeholderSet(name='{self.name}', "
            f"total_stakeholders={len(self.stakeholders)})"
        )