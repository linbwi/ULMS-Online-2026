"""
Requirement Validation Module for University Library Management System Online (ULMS).

This module checks requirement quality, completeness, testability,
dependency integrity, and common requirement-writing problems.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set

from requirements_toolkit.requirement import (
    Requirement,
    RequirementSet,
)


# ============================================================
# 1. VALIDATION ISSUE
# ============================================================

@dataclass
class ValidationIssue:
    """
    Represent one problem found during requirement validation.

    Attributes:
        req_id: ID of the requirement containing the issue.
        category: Type of validation issue.
        message: Explanation of the issue.
        severity: Issue severity (ERROR, WARNING, or INFO).
    """

    req_id: str
    category: str
    message: str
    severity: str = "WARNING"

    def __str__(self) -> str:
        """Return a readable validation message."""

        return (
            f"[{self.severity}] "
            f"{self.req_id} - {self.category}: {self.message}"
        )

    def to_dict(self) -> dict:
        """Convert the validation issue to a dictionary."""

        return {
            "req_id": self.req_id,
            "category": self.category,
            "message": self.message,
            "severity": self.severity,
        }


# ============================================================
# 2. VALIDATION REPORT
# ============================================================

@dataclass
class ValidationReport:
    """
    Store and summarize the results of requirement validation.
    """

    issues: List[ValidationIssue] = field(default_factory=list)

    def add_issue(
        self,
        req_id: str,
        category: str,
        message: str,
        severity: str = "WARNING",
    ) -> None:
        """Add a validation issue to the report."""

        self.issues.append(
            ValidationIssue(
                req_id=req_id,
                category=category,
                message=message,
                severity=severity,
            )
        )

    @property
    def errors(self) -> List[ValidationIssue]:
        """Return issues classified as errors."""

        return [
            issue for issue in self.issues
            if issue.severity == "ERROR"
        ]

    @property
    def warnings(self) -> List[ValidationIssue]:
        """Return issues classified as warnings."""

        return [
            issue for issue in self.issues
            if issue.severity == "WARNING"
        ]

    @property
    def infos(self) -> List[ValidationIssue]:
        """Return issues classified as informational."""

        return [
            issue for issue in self.issues
            if issue.severity == "INFO"
        ]

    @property
    def is_valid(self) -> bool:
        """
        Return True if no ERROR-level issues were found.

        Warnings and informational messages do not automatically
        make a requirement set invalid.
        """

        return len(self.errors) == 0

    def summary(self) -> Dict[str, int]:
        """Return the validation statistics."""

        return {
            "total_issues": len(self.issues),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "infos": len(self.infos),
        }

    def print_report(self) -> None:
        """Print all issues and a summary."""

        print("=" * 65)
        print("ULMS REQUIREMENT VALIDATION REPORT")
        print("=" * 65)

        if not self.issues:
            print("No validation issues found.")
        else:
            for issue in self.issues:
                print(issue)

        print("-" * 65)
        print("Summary:", self.summary())
        print("Valid:", self.is_valid)
        print("=" * 65)

    def to_list(self) -> List[dict]:
        """Convert all issues to a list of dictionaries."""

        return [
            issue.to_dict()
            for issue in self.issues
        ]


# ============================================================
# 3. REQUIREMENT VALIDATOR
# ============================================================

class RequirementValidator:
    """
    Validate individual requirements and complete requirement sets.

    The validator performs preliminary quality checks. It does not
    replace manual review by the project team or stakeholders.
    """

    VAGUE_TERMS = [
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
        "soon",
        "normally",
        "adequate",
        "sufficient",
    ]

    def validate_requirement(
        self,
        requirement: Requirement,
    ) -> ValidationReport:
        """Validate one requirement."""

        if not isinstance(requirement, Requirement):
            raise TypeError(
                "validate_requirement expects a Requirement object."
            )

        report = ValidationReport()

        # Check completeness.
        if not requirement.is_complete():
            report.add_issue(
                req_id=requirement.req_id,
                category="Completeness",
                message=(
                    "The requirement is missing one or more "
                    "required fields."
                ),
                severity="ERROR",
            )

        # Check testability.
        if not requirement.is_testable():
            report.add_issue(
                req_id=requirement.req_id,
                category="Testability",
                message=(
                    "The requirement may not be testable. "
                    "Check whether it contains 'shall' and "
                    "whether its expected result is measurable."
                ),
                severity="WARNING",
            )

        # Check vague wording.
        statement = requirement.statement.lower()

        found_terms = [
            term for term in self.VAGUE_TERMS
            if term in statement
        ]

        if found_terms:
            report.add_issue(
                req_id=requirement.req_id,
                category="Ambiguity",
                message=(
                    "Potentially vague terms found: "
                    + ", ".join(found_terms)
                    + ". Consider defining measurable criteria."
                ),
                severity="WARNING",
            )

        # Check self-dependency.
        if requirement.has_self_dependency():
            report.add_issue(
                req_id=requirement.req_id,
                category="Dependency",
                message=(
                    "The requirement depends on itself."
                ),
                severity="ERROR",
            )

        # Check empty acceptance criteria.
        if not requirement.acceptance_criteria.strip():
            report.add_issue(
                req_id=requirement.req_id,
                category="Acceptance Criteria",
                message=(
                    "Acceptance criteria have not been specified."
                ),
                severity="WARNING",
            )

        # Check missing source.
        if not requirement.source.strip():
            report.add_issue(
                req_id=requirement.req_id,
                category="Source",
                message=(
                    "The source of the requirement has not been specified."
                ),
                severity="INFO",
            )

        return report

    def validate_requirement_set(
        self,
        requirements: RequirementSet,
    ) -> ValidationReport:
        """Validate all requirements in a RequirementSet."""

        if not isinstance(requirements, RequirementSet):
            raise TypeError(
                "validate_requirement_set expects a RequirementSet object."
            )

        report = ValidationReport()

        # Collect requirement IDs for dependency checks.
        requirement_ids: Set[str] = {
            requirement.req_id
            for requirement in requirements
        }

        # Validate each requirement.
        for requirement in requirements:
            individual_report = self.validate_requirement(requirement)

            report.issues.extend(individual_report.issues)

            # Check dependencies that reference missing IDs.
            for dependency_id in requirement.dependencies:
                if dependency_id not in requirement_ids:
                    report.add_issue(
                        req_id=requirement.req_id,
                        category="Dependency",
                        message=(
                            f"Dependency '{dependency_id}' does not "
                            "match any requirement ID in this set."
                        ),
                        severity="ERROR",
                    )

        # Check duplicate IDs defensively.
        seen_ids = set()

        for requirement in requirements:
            if requirement.req_id in seen_ids:
                report.add_issue(
                    req_id=requirement.req_id,
                    category="Duplicate ID",
                    message=(
                        "More than one requirement uses this ID."
                    ),
                    severity="ERROR",
                )

            seen_ids.add(requirement.req_id)

        return report

    def validate_dict(
        self,
        requirement_data: dict,
    ) -> ValidationReport:
        """
        Validate a requirement represented as a dictionary.

        The dictionary must contain the fields required to create
        a Requirement object.
        """

        if not isinstance(requirement_data, dict):
            raise TypeError(
                "validate_dict expects a dictionary."
            )

        try:
            requirement = Requirement(
                req_id=requirement_data["req_id"],
                title=requirement_data["title"],
                statement=requirement_data["statement"],
                req_type=requirement_data["req_type"],
                priority=requirement_data.get(
                    "priority"
                ) or __import__(
                    "requirements_toolkit.requirement",
                    fromlist=["Priority"],
                ).Priority.SHOULD,
                status=requirement_data.get(
                    "status"
                ) or __import__(
                    "requirements_toolkit.requirement",
                    fromlist=["RequirementStatus"],
                ).RequirementStatus.PROPOSED,
                source=requirement_data.get("source", ""),
                rationale=requirement_data.get("rationale", ""),
                owner=requirement_data.get("owner", ""),
                release=requirement_data.get("release", ""),
                acceptance_criteria=requirement_data.get(
                    "acceptance_criteria", ""
                ),
                verification_method=requirement_data.get(
                    "verification_method", "Test"
                ),
                complexity=requirement_data.get("complexity", ""),
                dependencies=requirement_data.get("dependencies", []),
                tags=requirement_data.get("tags", []),
            )

        except (KeyError, TypeError, ValueError) as error:
            report = ValidationReport()
            report.add_issue(
                req_id=str(requirement_data.get("req_id", "UNKNOWN")),
                category="Input Data",
                message=str(error),
                severity="ERROR",
            )
            return report

        return self.validate_requirement(requirement)


# ============================================================
# 4. CONVENIENCE FUNCTIONS
# ============================================================

def validate_requirement(
    requirement: Requirement,
) -> ValidationReport:
    """Validate one requirement without creating a validator manually."""

    validator = RequirementValidator()
    return validator.validate_requirement(requirement)


def validate_requirement_set(
    requirements: RequirementSet,
) -> ValidationReport:
    """Validate a complete requirement set."""

    validator = RequirementValidator()
    return validator.validate_requirement_set(requirements)