"""
SRS Generator for University Library Management System Online.

This module generates a Software Requirements Specification (SRS)
from requirements, non-functional requirements, stakeholders,
use cases, and traceability data.

Supported output formats:
- Markdown (.md)
- HTML (.html)
- Plain text (.txt)
"""

from dataclasses import dataclass, field
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Optional


# ============================================================
# 1. SRS DOCUMENT METADATA
# ============================================================

@dataclass
class SRSMetadata:
    """Metadata describing the SRS document."""

    project_name: str = "University Library Management System Online"
    document_title: str = "Software Requirements Specification"
    version: str = "1.0"
    author: str = ""
    organization: str = ""
    status: str = "Draft"
    creation_date: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d")
    )

    def __post_init__(self):
        self.project_name = str(self.project_name).strip()
        self.document_title = str(self.document_title).strip()
        self.version = str(self.version).strip()
        self.author = str(self.author).strip()
        self.organization = str(self.organization).strip()
        self.status = str(self.status).strip()
        self.creation_date = str(self.creation_date).strip()

        if not self.project_name:
            raise ValueError("Project name cannot be empty.")

        if not self.document_title:
            raise ValueError("Document title cannot be empty.")

        if not self.version:
            raise ValueError("Document version cannot be empty.")


# ============================================================
# 2. SRS GENERATOR
# ============================================================

class SRSGenerator:
    """
    Generate an SRS document from project artifacts.

    The generator accepts data objects from the other toolkit
    modules. These objects are optional, so a partial SRS can
    still be generated.
    """

    def __init__(
        self,
        metadata: Optional[SRSMetadata] = None,
        requirements=None,
        nfrs=None,
        stakeholders=None,
        use_cases=None,
        traceability=None,
    ):
        self.metadata = metadata or SRSMetadata()

        self.requirements = requirements
        self.nfrs = nfrs
        self.stakeholders = stakeholders
        self.use_cases = use_cases
        self.traceability = traceability

    # --------------------------------------------------------
    # INTERNAL HELPERS
    # --------------------------------------------------------

    @staticmethod
    def _items(collection, attribute: str) -> list:
        """
        Retrieve items from a collection.

        Supports:
        - None
        - A list or tuple
        - Toolkit collection objects with an attribute such as
          requirements, nfrs, stakeholders, use_cases or links.
        """
        if collection is None:
            return []

        if isinstance(collection, (list, tuple)):
            return list(collection)

        value = getattr(collection, attribute, None)

        if value is None:
            return []

        return list(value)

    @staticmethod
    def _value(obj, attribute: str, default=""):
        """Safely retrieve an attribute from an object."""
        return getattr(obj, attribute, default)

    @staticmethod
    def _enum_value(value) -> str:
        """Return an enum's display value when applicable."""
        return getattr(value, "value", value)

    @staticmethod
    def _format_list(values) -> str:
        """Format a list for inclusion in a document."""
        if not values:
            return "None specified"

        return "; ".join(str(value) for value in values)

    @staticmethod
    def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
        """Build a Markdown table."""
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]

        for row in rows:
            cleaned = [
                str(value).replace("|", "\\|").replace("\n", "<br>")
                for value in row
            ]
            lines.append("| " + " | ".join(cleaned) + " |")

        return "\n".join(lines)

    # --------------------------------------------------------
    # SECTION 1: TITLE AND DOCUMENT INFORMATION
    # --------------------------------------------------------

    def _section_title(self) -> str:
        metadata = self.metadata

        lines = [
            f"# {metadata.document_title}",
            "",
            f"**Project:** {metadata.project_name}",
            f"**Version:** {metadata.version}",
            f"**Status:** {metadata.status}",
            f"**Author:** {metadata.author or 'Not specified'}",
            f"**Organization:** {metadata.organization or 'Not specified'}",
            f"**Creation Date:** {metadata.creation_date}",
            "",
            "---",
            "",
        ]

        return "\n".join(lines)

    # --------------------------------------------------------
    # SECTION 2: INTRODUCTION
    # --------------------------------------------------------

    def _section_introduction(self) -> str:
        return "\n".join([
            "## 1. Introduction",
            "",
            "### 1.1 Purpose",
            "",
            (
                "This document specifies the requirements for "
                f"{self.metadata.project_name}. It provides a common "
                "reference for stakeholders, developers, testers, "
                "and other project participants."
            ),
            "",
            "### 1.2 Scope",
            "",
            (
                f"The scope of this document is the "
                f"{self.metadata.project_name} project. The detailed "
                "capabilities and constraints should be confirmed "
                "against the approved project requirements."
            ),
            "",
            "### 1.3 Document Overview",
            "",
            (
                "The document presents stakeholders, functional "
                "requirements, non-functional requirements, use cases, "
                "and traceability information when these data are supplied."
            ),
            "",
        ])

    # --------------------------------------------------------
    # SECTION 3: STAKEHOLDERS
    # --------------------------------------------------------

    def _section_stakeholders(self) -> str:
        stakeholders = self._items(
            self.stakeholders,
            "stakeholders",
        )

        lines = [
            "## 2. Stakeholders",
            "",
        ]

        if not stakeholders:
            lines.extend([
                "No stakeholder data supplied.",
                "",
            ])
            return "\n".join(lines)

        rows = []

        for stakeholder in stakeholders:
            rows.append([
                str(self._value(stakeholder, "stakeholder_id")),
                str(self._value(stakeholder, "name")),
                str(self._enum_value(
                    self._value(stakeholder, "role")
                )),
                str(self._enum_value(
                    self._value(stakeholder, "stakeholder_type")
                )),
                str(self._value(stakeholder, "responsibilities")),
                str(self._value(stakeholder, "needs")),
            ])

        lines.extend([
            self._markdown_table(
                [
                    "ID",
                    "Name",
                    "Role",
                    "Type",
                    "Responsibilities",
                    "Needs",
                ],
                rows,
            ),
            "",
        ])

        return "\n".join(lines)

    # --------------------------------------------------------
    # SECTION 4: FUNCTIONAL REQUIREMENTS
    # --------------------------------------------------------

    def _section_functional_requirements(self) -> str:
        requirements = self._items(
            self.requirements,
            "requirements",
        )

        functional = [
            req for req in requirements
            if "FUNCTIONAL" in str(
                self._enum_value(self._value(req, "req_type", ""))
            ).upper()
        ]

        lines = [
            "## 3. Functional Requirements",
            "",
        ]

        if not functional:
            lines.extend([
                "No functional requirements supplied.",
                "",
            ])
            return "\n".join(lines)

        rows = []

        for req in functional:
            rows.append([
                str(self._value(req, "req_id")),
                str(self._value(req, "title")),
                str(self._value(req, "statement")),
                str(self._enum_value(
                    self._value(req, "priority")
                )),
                str(self._enum_value(
                    self._value(req, "status")
                )),
                self._format_list(
                    self._value(req, "acceptance_criteria", [])
                ),
            ])

        lines.extend([
            self._markdown_table(
                [
                    "ID",
                    "Title",
                    "Requirement Statement",
                    "Priority",
                    "Status",
                    "Acceptance Criteria",
                ],
                rows,
            ),
            "",
        ])

        return "\n".join(lines)

    # --------------------------------------------------------
    # SECTION 5: NON-FUNCTIONAL REQUIREMENTS
    # --------------------------------------------------------

    def _section_non_functional_requirements(self) -> str:
        nfrs = self._items(self.nfrs, "nfrs")

        lines = [
            "## 4. Non-Functional Requirements",
            "",
        ]

        if not nfrs:
            lines.extend([
                "No non-functional requirements supplied.",
                "",
            ])
            return "\n".join(lines)

        rows = []

        for nfr in nfrs:
            rows.append([
                str(self._value(nfr, "nfr_id")),
                str(self._value(nfr, "title")),
                str(self._enum_value(
                    self._value(nfr, "category")
                )),
                str(self._value(nfr, "statement")),
                str(self._enum_value(
                    self._value(nfr, "priority")
                )),
                str(self._value(nfr, "metric")),
                str(self._value(nfr, "target_value")),
                str(self._value(nfr, "measurement_unit")),
            ])

        lines.extend([
            self._markdown_table(
                [
                    "ID",
                    "Title",
                    "Category",
                    "Requirement Statement",
                    "Priority",
                    "Metric",
                    "Target",
                    "Unit",
                ],
                rows,
            ),
            "",
        ])

        return "\n".join(lines)

    # --------------------------------------------------------
    # SECTION 6: USE CASES
    # --------------------------------------------------------

    def _section_use_cases(self) -> str:
        use_cases = self._items(
            self.use_cases,
            "use_cases",
        )

        lines = [
            "## 5. Use Cases",
            "",
        ]

        if not use_cases:
            lines.extend([
                "No use case data supplied.",
                "",
            ])
            return "\n".join(lines)

        for use_case in use_cases:
            use_case_id = self._value(
                use_case, "use_case_id"
            )
            name = self._value(use_case, "name")
            description = self._value(
                use_case, "description"
            )
            primary_actor = self._value(
                use_case, "primary_actor"
            )

            lines.extend([
                f"### {use_case_id}: {name}",
                "",
                f"**Description:** {description}",
                f"**Primary Actor:** {primary_actor}",
                f"**Priority:** {self._enum_value(self._value(use_case, 'priority'))}",
                f"**Status:** {self._enum_value(self._value(use_case, 'status'))}",
                "",
                "**Preconditions:**",
                "",
            ])

            preconditions = self._value(
                use_case, "preconditions", []
            )

            if preconditions:
                lines.extend([f"- {item}" for item in preconditions])
            else:
                lines.append("- Not specified")

            lines.extend([
                "",
                "**Main Flow:**",
                "",
            ])

            main_flow = self._value(
                use_case, "main_flow", []
            )

            if main_flow:
                lines.extend([f"{item}" for item in main_flow])
            else:
                lines.append("Not specified")

            lines.extend([
                "",
                "**Alternative Flows:**",
                "",
            ])

            alternative_flows = self._value(
                use_case, "alternative_flows", []
            )

            if alternative_flows:
                lines.extend([
                    f"- {item}" for item in alternative_flows
                ])
            else:
                lines.append("- Not specified")

            lines.extend([
                "",
                "**Postconditions:**",
                "",
            ])

            postconditions = self._value(
                use_case, "postconditions", []
            )

            if postconditions:
                lines.extend([
                    f"- {item}" for item in postconditions
                ])
            else:
                lines.append("- Not specified")

            lines.extend(["", "---", ""])

        return "\n".join(lines)

    # --------------------------------------------------------
    # SECTION 7: TRACEABILITY
    # --------------------------------------------------------

    def _section_traceability(self) -> str:
        links = self._items(self.traceability, "links")

        lines = [
            "## 6. Requirements Traceability",
            "",
        ]

        if not links:
            lines.extend([
                "No traceability links supplied.",
                "",
            ])
            return "\n".join(lines)

        rows = []

        for link in links:
            rows.append([
                str(self._value(link, "source_id")),
                str(self._value(link, "target_id")),
                str(self._enum_value(
                    self._value(link, "relationship")
                )),
                str(self._value(link, "description")),
            ])

        lines.extend([
            self._markdown_table(
                [
                    "Source ID",
                    "Target ID",
                    "Relationship",
                    "Description",
                ],
                rows,
            ),
            "",
        ])

        return "\n".join(lines)

    # --------------------------------------------------------
    # SECTION 8: DOCUMENT SUMMARY
    # --------------------------------------------------------

    def _section_summary(self) -> str:
        requirements = self._items(
            self.requirements, "requirements"
        )
        nfrs = self._items(self.nfrs, "nfrs")
        stakeholders = self._items(
            self.stakeholders, "stakeholders"
        )
        use_cases = self._items(
            self.use_cases, "use_cases"
        )
        links = self._items(self.traceability, "links")

        lines = [
            "## 7. Document Summary",
            "",
            "| Artifact Type | Count |",
            "|---|---:|",
            f"| Requirements | {len(requirements)} |",
            f"| Non-Functional Requirements | {len(nfrs)} |",
            f"| Stakeholders | {len(stakeholders)} |",
            f"| Use Cases | {len(use_cases)} |",
            f"| Traceability Links | {len(links)} |",
            "",
            "---",
            "",
            "*End of document.*",
            "",
        ]

        return "\n".join(lines)

    # --------------------------------------------------------
    # GENERATE MARKDOWN
    # --------------------------------------------------------

    def generate_markdown(self) -> str:
        """Generate the complete SRS as a Markdown string."""

        sections = [
            self._section_title(),
            self._section_introduction(),
            self._section_stakeholders(),
            self._section_functional_requirements(),
            self._section_non_functional_requirements(),
            self._section_use_cases(),
            self._section_traceability(),
            self._section_summary(),
        ]

        return "\n".join(sections)

    # --------------------------------------------------------
    # GENERATE HTML
    # --------------------------------------------------------

    def generate_html(self) -> str:
        """
        Generate an HTML document from the Markdown SRS.

        This implementation escapes the Markdown as plain text
        rather than converting Markdown syntax into HTML elements.
        """
        markdown = self.generate_markdown()

        safe_text = escape(markdown)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(self.metadata.document_title)}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1100px;
            margin: 40px auto;
            padding: 0 24px;
            line-height: 1.6;
            color: #222;
        }}
        h1 {{
            color: #17365D;
            border-bottom: 3px solid #4472C4;
            padding-bottom: 12px;
        }}
        pre {{
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            background: #f5f7fa;
            border: 1px solid #ddd;
            padding: 24px;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <pre>{safe_text}</pre>
</body>
</html>
"""

    # --------------------------------------------------------
    # GENERATE PLAIN TEXT
    # --------------------------------------------------------

    def generate_text(self) -> str:
        """Generate a plain-text version of the SRS."""

        return self.generate_markdown()

    # --------------------------------------------------------
    # SAVE TO FILE
    # --------------------------------------------------------

    def save(
        self,
        output_path: str,
        file_format: Optional[str] = None,
    ) -> Path:
        """
        Generate and save the SRS.

        Supported formats:
            md / markdown
            html / htm
            txt / text
        """
        path = Path(output_path)

        output_format = (
            file_format or path.suffix.lstrip(".")
        ).lower()

        if output_format in {"md", "markdown"}:
            content = self.generate_markdown()

        elif output_format in {"html", "htm"}:
            content = self.generate_html()

        elif output_format in {"txt", "text"}:
            content = self.generate_text()

        else:
            raise ValueError(
                f"Unsupported SRS format: {output_format}. "
                "Use md, html, or txt."
            )

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

        return path