"""
Safety and Hazard Management Module for ULMS Online.

This module supports:
- Hazard identification
- Risk assessment
- Safety mitigation tracking
- Hazard status management
- Safety requirement traceability
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ==================================================
# ENUMS
# ==================================================

class HazardCategory(str, Enum):
    """Categories of hazards that may affect the system."""

    DATA_LOSS = "DATA_LOSS"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    DATA_CORRUPTION = "DATA_CORRUPTION"
    SYSTEM_FAILURE = "SYSTEM_FAILURE"
    INCORRECT_PROCESSING = "INCORRECT_PROCESSING"
    PRIVACY_BREACH = "PRIVACY_BREACH"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    USER_ERROR = "USER_ERROR"
    OTHER = "OTHER"


class RiskSeverity(str, Enum):
    """Severity of the consequences of a hazard."""

    NEGLIGIBLE = 1
    MINOR = 2
    MODERATE = 3
    MAJOR = 4
    CATASTROPHIC = 5


class RiskLikelihood(str, Enum):
    """Estimated likelihood that a hazard will occur."""

    RARE = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    ALMOST_CERTAIN = 5


class RiskLevel(str, Enum):
    """Overall risk classification."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class HazardStatus(str, Enum):
    """Lifecycle status of a hazard."""

    IDENTIFIED = "IDENTIFIED"
    UNDER_ASSESSMENT = "UNDER_ASSESSMENT"
    MITIGATION_PLANNED = "MITIGATION_PLANNED"
    MITIGATING = "MITIGATING"
    MITIGATED = "MITIGATED"
    ACCEPTED = "ACCEPTED"
    CLOSED = "CLOSED"


# ==================================================
# HAZARD
# ==================================================

@dataclass
class Hazard:
    """Represent an identified hazard and its risk assessment."""

    hazard_id: str
    title: str
    description: str
    category: HazardCategory = HazardCategory.OTHER

    severity: RiskSeverity = RiskSeverity.MINOR
    likelihood: RiskLikelihood = RiskLikelihood.UNLIKELY

    status: HazardStatus = HazardStatus.IDENTIFIED

    affected_components: list[str] = field(default_factory=list)
    affected_requirement_ids: list[str] = field(default_factory=list)

    causes: list[str] = field(default_factory=list)
    consequences: list[str] = field(default_factory=list)
    mitigation_measures: list[str] = field(default_factory=list)

    owner: str = ""
    residual_severity: Optional[RiskSeverity] = None
    residual_likelihood: Optional[RiskLikelihood] = None

    notes: str = ""

    def __post_init__(self):
        """Normalize and validate the hazard data."""

        self.hazard_id = str(self.hazard_id).strip()
        self.title = str(self.title).strip()
        self.description = str(self.description).strip()
        self.owner = str(self.owner).strip()
        self.notes = str(self.notes).strip()

        if not self.hazard_id:
            raise ValueError("hazard_id must not be empty.")

        if not self.title:
            raise ValueError("title must not be empty.")

        if not self.description:
            raise ValueError("description must not be empty.")

        self.category = self._convert_enum(
            self.category,
            HazardCategory,
            "category",
        )

        self.severity = self._convert_enum(
            self.severity,
            RiskSeverity,
            "severity",
        )

        self.likelihood = self._convert_enum(
            self.likelihood,
            RiskLikelihood,
            "likelihood",
        )

        self.status = self._convert_enum(
            self.status,
            HazardStatus,
            "status",
        )

        if self.residual_severity is not None:
            self.residual_severity = self._convert_enum(
                self.residual_severity,
                RiskSeverity,
                "residual_severity",
            )

        if self.residual_likelihood is not None:
            self.residual_likelihood = self._convert_enum(
                self.residual_likelihood,
                RiskLikelihood,
                "residual_likelihood",
            )

        self.affected_components = self._normalize_list(
            self.affected_components
        )

        self.affected_requirement_ids = self._normalize_list(
            self.affected_requirement_ids
        )

        self.causes = self._normalize_list(self.causes)
        self.consequences = self._normalize_list(self.consequences)
        self.mitigation_measures = self._normalize_list(
            self.mitigation_measures
        )

    @staticmethod
    def _convert_enum(value, enum_class, field_name):
        """Convert a string or integer to an enum value."""

        if isinstance(value, enum_class):
            return value

        try:
            if enum_class in (RiskSeverity, RiskLikelihood):
                if isinstance(value, str) and not value.strip().isdigit():
                    return enum_class[value.strip().upper()]

                return enum_class(int(value))

            return enum_class(str(value).strip().upper())

        except (ValueError, KeyError, TypeError) as exc:
            raise ValueError(
                f"Invalid {field_name}: {value}"
            ) from exc

    @staticmethod
    def _normalize_list(values) -> list[str]:
        """Normalize a list of strings and remove empty entries."""

        result = []
        seen = set()

        for value in values:
            value = str(value).strip()

            if value and value not in seen:
                result.append(value)
                seen.add(value)

        return result

    # --------------------------------------------------
    # RISK ASSESSMENT
    # --------------------------------------------------

    @property
    def risk_score(self) -> int:
        """
        Calculate the initial risk score.

        Risk score = severity * likelihood.
        """
        return self.severity.value * self.likelihood.value

    @property
    def risk_level(self) -> RiskLevel:
        """
        Convert the risk score into a risk category.

        1-4: LOW
        5-9: MEDIUM
        10-16: HIGH
        17-25: CRITICAL
        """
        score = self.risk_score

        if score <= 4:
            return RiskLevel.LOW

        if score <= 9:
            return RiskLevel.MEDIUM

        if score <= 16:
            return RiskLevel.HIGH

        return RiskLevel.CRITICAL

    @property
    def residual_risk_score(self) -> Optional[int]:
        """Calculate residual risk when both residual values exist."""

        if (
            self.residual_severity is None
            or self.residual_likelihood is None
        ):
            return None

        return (
            self.residual_severity.value
            * self.residual_likelihood.value
        )

    @property
    def residual_risk_level(self) -> Optional[RiskLevel]:
        """Return the residual risk category, if assessed."""

        score = self.residual_risk_score

        if score is None:
            return None

        if score <= 4:
            return RiskLevel.LOW

        if score <= 9:
            return RiskLevel.MEDIUM

        if score <= 16:
            return RiskLevel.HIGH

        return RiskLevel.CRITICAL

    # --------------------------------------------------
    # HAZARD INFORMATION
    # --------------------------------------------------

    def is_high_risk(self) -> bool:
        """Return True for HIGH or CRITICAL initial risk."""

        return self.risk_level in {
            RiskLevel.HIGH,
            RiskLevel.CRITICAL,
        }

    def is_critical(self) -> bool:
        """Return True if the initial risk is critical."""

        return self.risk_level == RiskLevel.CRITICAL

    def has_mitigation(self) -> bool:
        """Check whether mitigation measures are documented."""

        return bool(self.mitigation_measures)

    def has_affected_requirements(self) -> bool:
        """Check whether affected requirements are recorded."""

        return bool(self.affected_requirement_ids)

    def is_residual_risk_assessed(self) -> bool:
        """Check whether both residual risk values are available."""

        return (
            self.residual_severity is not None
            and self.residual_likelihood is not None
        )

    # --------------------------------------------------
    # UPDATE OPERATIONS
    # --------------------------------------------------

    def add_mitigation(self, measure: str) -> None:
        """Add a mitigation measure."""

        measure = str(measure).strip()

        if not measure:
            raise ValueError("Mitigation measure must not be empty.")

        if measure not in self.mitigation_measures:
            self.mitigation_measures.append(measure)

    def add_cause(self, cause: str) -> None:
        """Add a potential cause."""

        cause = str(cause).strip()

        if not cause:
            raise ValueError("Cause must not be empty.")

        if cause not in self.causes:
            self.causes.append(cause)

    def add_consequence(self, consequence: str) -> None:
        """Add a potential consequence."""

        consequence = str(consequence).strip()

        if not consequence:
            raise ValueError("Consequence must not be empty.")

        if consequence not in self.consequences:
            self.consequences.append(consequence)

    def add_affected_requirement(self, req_id: str) -> None:
        """Associate a requirement with this hazard."""

        req_id = str(req_id).strip()

        if not req_id:
            raise ValueError("Requirement ID must not be empty.")

        if req_id not in self.affected_requirement_ids:
            self.affected_requirement_ids.append(req_id)

    def set_residual_risk(
        self,
        severity: RiskSeverity,
        likelihood: RiskLikelihood,
    ) -> None:
        """Record risk estimates after mitigation."""

        self.residual_severity = self._convert_enum(
            severity,
            RiskSeverity,
            "residual_severity",
        )

        self.residual_likelihood = self._convert_enum(
            likelihood,
            RiskLikelihood,
            "residual_likelihood",
        )

    def update_status(self, status: HazardStatus) -> None:
        """Update the hazard lifecycle status."""

        self.status = self._convert_enum(
            status,
            HazardStatus,
            "status",
        )

    # --------------------------------------------------
    # QUALITY CHECKS
    # --------------------------------------------------

    def quality_issues(self) -> list[str]:
        """Identify missing or potentially inconsistent information."""

        issues = []

        if not self.causes:
            issues.append("No hazard causes have been recorded.")

        if not self.consequences:
            issues.append("No hazard consequences have been recorded.")

        if not self.affected_components:
            issues.append("No affected components have been recorded.")

        if self.is_high_risk() and not self.mitigation_measures:
            issues.append(
                "High-risk hazard has no documented mitigation measures."
            )

        if self.status in {
            HazardStatus.MITIGATION_PLANNED,
            HazardStatus.MITIGATING,
            HazardStatus.MITIGATED,
            HazardStatus.CLOSED,
        } and not self.mitigation_measures:
            issues.append(
                "Hazard status indicates mitigation, "
                "but no mitigation measures are recorded."
            )

        if self.is_residual_risk_assessed():
            if (
                self.residual_risk_score is not None
                and self.residual_risk_score > self.risk_score
            ):
                issues.append(
                    "Residual risk score is higher than initial risk score."
                )

        return issues

    # --------------------------------------------------
    # SERIALIZATION
    # --------------------------------------------------

    def to_dict(self) -> dict:
        """Convert the hazard to a dictionary."""

        return {
            "hazard_id": self.hazard_id,
            "title": self.title,
            "description": self.description,
            "category": self.category.value,
            "severity": self.severity.name,
            "likelihood": self.likelihood.name,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level.value,
            "status": self.status.value,
            "affected_components": self.affected_components.copy(),
            "affected_requirement_ids": (
                self.affected_requirement_ids.copy()
            ),
            "causes": self.causes.copy(),
            "consequences": self.consequences.copy(),
            "mitigation_measures": self.mitigation_measures.copy(),
            "owner": self.owner,
            "residual_severity": (
                self.residual_severity.name
                if self.residual_severity is not None
                else None
            ),
            "residual_likelihood": (
                self.residual_likelihood.name
                if self.residual_likelihood is not None
                else None
            ),
            "residual_risk_score": self.residual_risk_score,
            "residual_risk_level": (
                self.residual_risk_level.value
                if self.residual_risk_level is not None
                else None
            ),
            "notes": self.notes,
        }

    def __str__(self) -> str:
        return (
            f"{self.hazard_id} | {self.title} | "
            f"Risk: {self.risk_level.value} "
            f"({self.risk_score}) | {self.status.value}"
        )


# ==================================================
# HAZARD COLLECTION
# ==================================================

@dataclass
class HazardSet:
    """Manage multiple hazards."""

    name: str = "ULMS Safety Hazards"
    hazards: list[Hazard] = field(default_factory=list)

    def __post_init__(self):
        self.name = str(self.name).strip()

        if not self.name:
            raise ValueError("Hazard set name must not be empty.")

        seen_ids = set()

        for hazard in self.hazards:
            if not isinstance(hazard, Hazard):
                raise TypeError(
                    "All entries must be Hazard objects."
                )

            if hazard.hazard_id in seen_ids:
                raise ValueError(
                    f"Duplicate hazard ID: {hazard.hazard_id}"
                )

            seen_ids.add(hazard.hazard_id)

    def add(self, hazard: Hazard) -> None:
        """Add a hazard with a unique ID."""

        if not isinstance(hazard, Hazard):
            raise TypeError("hazard must be a Hazard object.")

        if self.get(hazard.hazard_id) is not None:
            raise ValueError(
                f"Hazard ID '{hazard.hazard_id}' already exists."
            )

        self.hazards.append(hazard)

    def get(self, hazard_id: str) -> Optional[Hazard]:
        """Find a hazard by ID."""

        hazard_id = str(hazard_id).strip()

        for hazard in self.hazards:
            if hazard.hazard_id == hazard_id:
                return hazard

        return None

    def remove(self, hazard_id: str) -> bool:
        """Remove a hazard by ID."""

        hazard = self.get(hazard_id)

        if hazard is None:
            return False

        self.hazards.remove(hazard)
        return True

    def by_category(
        self,
        category: HazardCategory,
    ) -> list[Hazard]:
        """Return hazards in a category."""

        if not isinstance(category, HazardCategory):
            category = HazardCategory(str(category).strip().upper())

        return [
            hazard for hazard in self.hazards
            if hazard.category == category
        ]

    def by_status(
        self,
        status: HazardStatus,
    ) -> list[Hazard]:
        """Return hazards with a specific status."""

        if not isinstance(status, HazardStatus):
            status = HazardStatus(str(status).strip().upper())

        return [
            hazard for hazard in self.hazards
            if hazard.status == status
        ]

    def by_risk_level(
        self,
        risk_level: RiskLevel,
    ) -> list[Hazard]:
        """Return hazards at a specific initial risk level."""

        if not isinstance(risk_level, RiskLevel):
            risk_level = RiskLevel(str(risk_level).strip().upper())

        return [
            hazard for hazard in self.hazards
            if hazard.risk_level == risk_level
        ]

    def high_risk(self) -> list[Hazard]:
        """Return HIGH and CRITICAL hazards."""

        return [
            hazard for hazard in self.hazards
            if hazard.is_high_risk()
        ]

    def critical(self) -> list[Hazard]:
        """Return CRITICAL hazards."""

        return [
            hazard for hazard in self.hazards
            if hazard.is_critical()
        ]

    def without_mitigation(self) -> list[Hazard]:
        """Return hazards without documented mitigation."""

        return [
            hazard for hazard in self.hazards
            if not hazard.has_mitigation()
        ]

    def with_quality_issues(self) -> list[Hazard]:
        """Return hazards that have quality issues."""

        return [
            hazard for hazard in self.hazards
            if hazard.quality_issues()
        ]

    def find_by_requirement(self, req_id: str) -> list[Hazard]:
        """Find hazards associated with a requirement."""

        req_id = str(req_id).strip()

        return [
            hazard for hazard in self.hazards
            if req_id in hazard.affected_requirement_ids
        ]

    def count_by_risk_level(self) -> dict[str, int]:
        """Count hazards by risk level."""

        return {
            level.value: len(self.by_risk_level(level))
            for level in RiskLevel
        }

    def count_by_status(self) -> dict[str, int]:
        """Count hazards by status."""

        return {
            status.value: len(self.by_status(status))
            for status in HazardStatus
        }

    def __len__(self) -> int:
        return len(self.hazards)

    def __iter__(self):
        return iter(self.hazards)

    def __contains__(self, hazard_id: str) -> bool:
        return self.get(hazard_id) is not None

    def __str__(self) -> str:
        return f"{self.name}: {len(self.hazards)} hazard(s)"