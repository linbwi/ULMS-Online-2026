"""
Traceability Management Module for ULMS Online.

This module provides:
- Traceability links between requirements, use cases and test cases
- Traceability link validation
- Forward and backward traceability
- Orphan and uncovered item detection
- Traceability matrix generation
- Impact analysis for requirement changes
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ============================================================
# 1. ENUMS
# ============================================================

class TraceabilityType(Enum):
    """Types of traceability relationships."""

    REQUIREMENT_TO_USE_CASE = "Requirement -> Use Case"
    REQUIREMENT_TO_TEST_CASE = "Requirement -> Test Case"
    USE_CASE_TO_TEST_CASE = "Use Case -> Test Case"
    REQUIREMENT_TO_REQUIREMENT = "Requirement -> Requirement"


class TraceabilityDirection(Enum):
    """Direction of a traceability query."""

    FORWARD = "Forward"
    BACKWARD = "Backward"


# ============================================================
# 2. TRACEABILITY LINK
# ============================================================

@dataclass
class TraceabilityLink:
    """
    Represents a relationship between two project artifacts.

    Examples:
        REQ-01 -> UC-01
        REQ-01 -> TC-01
        UC-01 -> TC-01
    """

    source_id: str
    target_id: str
    relationship: TraceabilityType
    description: str = ""

    def __post_init__(self):
        """Normalize values and validate the link."""
        self.source_id = str(self.source_id).strip().upper()
        self.target_id = str(self.target_id).strip().upper()
        self.description = str(self.description).strip()

        if not self.source_id:
            raise ValueError("Source ID cannot be empty.")

        if not self.target_id:
            raise ValueError("Target ID cannot be empty.")

        if self.source_id == self.target_id:
            raise ValueError(
                "Source ID and target ID cannot be identical."
            )

        if not isinstance(self.relationship, TraceabilityType):
            try:
                self.relationship = TraceabilityType(
                    self.relationship
                )
            except ValueError:
                raise ValueError(
                    f"Invalid traceability relationship: "
                    f"{self.relationship}"
                )

    def to_dict(self) -> dict:
        """Convert the link to a dictionary."""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship": self.relationship.value,
            "description": self.description,
        }

    def __str__(self) -> str:
        return (
            f"{self.source_id} -> {self.target_id} "
            f"({self.relationship.value})"
        )


# ============================================================
# 3. TRACEABILITY MATRIX
# ============================================================

@dataclass
class TraceabilityMatrix:
    """
    Store traceability relationships between project artifacts.

    This class records links. It does not automatically verify
    that IDs exist in the Excel workbook or project database.
    """

    name: str
    links: list[TraceabilityLink] = field(default_factory=list)

    def __post_init__(self):
        self.name = str(self.name).strip()

        if not self.name:
            raise ValueError("Traceability matrix name cannot be empty.")

        if not isinstance(self.links, list):
            raise ValueError("links must be a list.")

        seen = set()

        for link in self.links:
            if not isinstance(link, TraceabilityLink):
                raise TypeError(
                    "Every item in links must be a TraceabilityLink."
                )

            key = (
                link.source_id,
                link.target_id,
                link.relationship,
            )

            if key in seen:
                raise ValueError(
                    f"Duplicate traceability link: {link}"
                )

            seen.add(key)

    # --------------------------------------------------------
    # ADD AND REMOVE LINKS
    # --------------------------------------------------------

    def add_link(self, link: TraceabilityLink) -> None:
        """Add a link if the same relationship does not exist."""
        if not isinstance(link, TraceabilityLink):
            raise TypeError("link must be a TraceabilityLink.")

        if self.has_link(
            link.source_id,
            link.target_id,
            link.relationship,
        ):
            raise ValueError(
                f"Traceability link already exists: {link}"
            )

        self.links.append(link)

    def remove_link(
        self,
        source_id: str,
        target_id: str,
        relationship: Optional[TraceabilityType] = None,
    ) -> bool:
        """
        Remove a link.

        If relationship is omitted, remove all links matching
        the source and target IDs.
        """
        source_id = str(source_id).strip().upper()
        target_id = str(target_id).strip().upper()

        original_count = len(self.links)

        self.links = [
            link
            for link in self.links
            if not (
                link.source_id == source_id
                and link.target_id == target_id
                and (
                    relationship is None
                    or link.relationship == relationship
                )
            )
        ]

        return len(self.links) < original_count

    def has_link(
        self,
        source_id: str,
        target_id: str,
        relationship: Optional[TraceabilityType] = None,
    ) -> bool:
        """Check whether a specified relationship exists."""
        source_id = str(source_id).strip().upper()
        target_id = str(target_id).strip().upper()

        return any(
            link.source_id == source_id
            and link.target_id == target_id
            and (
                relationship is None
                or link.relationship == relationship
            )
            for link in self.links
        )

    # --------------------------------------------------------
    # TRACEABILITY QUERIES
    # --------------------------------------------------------

    def forward(self, artifact_id: str) -> list[TraceabilityLink]:
        """
        Return links starting from an artifact.

        Example:
            forward("REQ-01") returns links originating from REQ-01.
        """
        artifact_id = str(artifact_id).strip().upper()

        return [
            link
            for link in self.links
            if link.source_id == artifact_id
        ]

    def backward(self, artifact_id: str) -> list[TraceabilityLink]:
        """
        Return links ending at an artifact.

        Example:
            backward("TC-01") returns links pointing to TC-01.
        """
        artifact_id = str(artifact_id).strip().upper()

        return [
            link
            for link in self.links
            if link.target_id == artifact_id
        ]

    def related_to(self, artifact_id: str) -> list[TraceabilityLink]:
        """Return every link involving the specified artifact."""
        artifact_id = str(artifact_id).strip().upper()

        return [
            link
            for link in self.links
            if (
                link.source_id == artifact_id
                or link.target_id == artifact_id
            )
        ]

    def by_relationship(
        self,
        relationship: TraceabilityType,
    ) -> list[TraceabilityLink]:
        """Filter links by relationship type."""
        if not isinstance(relationship, TraceabilityType):
            relationship = TraceabilityType(relationship)

        return [
            link
            for link in self.links
            if link.relationship == relationship
        ]

    # --------------------------------------------------------
    # ARTIFACT COLLECTIONS
    # --------------------------------------------------------

    def artifact_ids(self) -> set[str]:
        """Return all artifact IDs mentioned in the matrix."""
        result = set()

        for link in self.links:
            result.add(link.source_id)
            result.add(link.target_id)

        return result

    def source_ids(self) -> set[str]:
        """Return all source artifact IDs."""
        return {link.source_id for link in self.links}

    def target_ids(self) -> set[str]:
        """Return all target artifact IDs."""
        return {link.target_id for link in self.links}

    # --------------------------------------------------------
    # TRACEABILITY CHECKS
    # --------------------------------------------------------

    def find_unlinked_sources(
        self,
        artifact_ids: list[str],
    ) -> list[str]:
        """
        Find artifacts that have no outgoing traceability links.

        This is useful for finding requirements that are not
        connected to downstream artifacts.
        """
        linked_sources = self.source_ids()

        return [
            str(artifact_id).strip().upper()
            for artifact_id in artifact_ids
            if str(artifact_id).strip().upper() not in linked_sources
        ]

    def find_unlinked_targets(
        self,
        artifact_ids: list[str],
    ) -> list[str]:
        """
        Find artifacts that have no incoming traceability links.

        This is useful for finding test cases that do not trace
        back to requirements or use cases.
        """
        linked_targets = self.target_ids()

        return [
            str(artifact_id).strip().upper()
            for artifact_id in artifact_ids
            if str(artifact_id).strip().upper() not in linked_targets
        ]

    def find_unknown_artifacts(
        self,
        known_artifact_ids: list[str] | set[str],
    ) -> list[str]:
        """
        Find IDs used in links that are absent from the supplied
        list of known artifact IDs.
        """
        known_ids = {
            str(artifact_id).strip().upper()
            for artifact_id in known_artifact_ids
        }

        return sorted(self.artifact_ids() - known_ids)

    def validate_links(
        self,
        known_artifact_ids: list[str] | set[str],
    ) -> list[str]:
        """
        Validate links against known artifact IDs.

        Returns a list of validation messages.
        """
        known_ids = {
            str(artifact_id).strip().upper()
            for artifact_id in known_artifact_ids
        }

        issues = []

        for link in self.links:
            if link.source_id not in known_ids:
                issues.append(
                    f"Unknown source artifact: {link.source_id}"
                )

            if link.target_id not in known_ids:
                issues.append(
                    f"Unknown target artifact: {link.target_id}"
                )

        return issues

    # --------------------------------------------------------
    # IMPACT ANALYSIS
    # --------------------------------------------------------

    def direct_impact(self, artifact_id: str) -> set[str]:
        """
        Return artifacts directly connected to the specified ID.

        This checks one link away; it does not recursively follow
        chains of relationships.
        """
        artifact_id = str(artifact_id).strip().upper()
        impacted = set()

        for link in self.links:
            if link.source_id == artifact_id:
                impacted.add(link.target_id)

            if link.target_id == artifact_id:
                impacted.add(link.source_id)

        return impacted

    def transitive_impact(self, artifact_id: str) -> set[str]:
        """
        Find all artifacts reachable through traceability links.

        Relationships are treated as undirected for impact
        analysis: following a link in either direction identifies
        a potentially related artifact.
        """
        artifact_id = str(artifact_id).strip().upper()

        visited = set()
        pending = [artifact_id]

        while pending:
            current_id = pending.pop()

            if current_id in visited:
                continue

            visited.add(current_id)

            for related_id in self.direct_impact(current_id):
                if related_id not in visited:
                    pending.append(related_id)

        visited.discard(artifact_id)
        return visited

    # --------------------------------------------------------
    # MATRIX REPRESENTATION
    # --------------------------------------------------------

    def to_matrix(self) -> dict[str, list[str]]:
        """
        Return a dictionary mapping each source ID to its targets.

        Example:
            {
                "REQ-01": ["UC-01", "TC-01"],
                "UC-01": ["TC-01"]
            }
        """
        matrix = {}

        for link in self.links:
            matrix.setdefault(link.source_id, [])

            if link.target_id not in matrix[link.source_id]:
                matrix[link.source_id].append(link.target_id)

        return matrix

    def to_list(self) -> list[dict]:
        """Convert all links to a list of dictionaries."""
        return [link.to_dict() for link in self.links]

    def __len__(self) -> int:
        return len(self.links)

    def __iter__(self):
        return iter(self.links)

    def __str__(self) -> str:
        return (
            f"TraceabilityMatrix(name='{self.name}', "
            f"links={len(self.links)})"
        )