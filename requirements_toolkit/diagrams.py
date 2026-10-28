"""
Diagram Generation Module for ULMS Online.

Supported diagrams:
- Use Case Diagram
- Activity Diagram
- Requirement Traceability Diagram
- Hazard Risk Diagram

The module generates Mermaid diagram definitions.
These definitions can be embedded in Markdown documentation
or rendered by a Mermaid-compatible viewer.
"""

from pathlib import Path
from typing import Any, Optional


class DiagramError(Exception):
    """Raised when diagram generation fails."""


class DiagramGenerator:
    """Generate Mermaid diagrams for requirements engineering."""


    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)


    # ==================================================
    # HELPER METHODS
    # ==================================================

    @staticmethod
    def _escape_text(value: Any) -> str:
        """Escape text for use in Mermaid labels."""

        text = str(value).strip()

        replacements = {
            '"': "'",
            "\n": " ",
            "\r": " ",
            "[": "(",
            "]": ")",
            "{": "(",
            "}": ")",
            "|": "/",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    @staticmethod
    def _get_value(
        item: Any,
        key: str,
        default: Any = "",
    ) -> Any:
        """Read a field from a dictionary or object."""

        if isinstance(item, dict):
            return item.get(key, default)

        return getattr(item, key, default)

    @classmethod
    def _label(
        cls,
        item: Any,
        key: str,
        default: str = "",
    ) -> str:
        """Get and escape a field for use as a diagram label."""

        value = cls._get_value(item, key, default)

        if hasattr(value, "value"):
            value = value.value

        return cls._escape_text(value)

    @staticmethod
    def _items(data: Any, *attributes: str) -> list:
        """
        Extract a list from a collection or accept a list directly.

        Example:
            _items(requirement_set, "requirements")
        """

        if isinstance(data, (list, tuple)):
            return list(data)

        for attribute in attributes:
            value = getattr(data, attribute, None)

            if isinstance(value, (list, tuple)):
                return list(value)

        raise DiagramError(
            "Expected a list, tuple, or supported collection object."
        )


    # ==================================================
    # USE CASE DIAGRAM
    # ==================================================

    def use_case_diagram(
        self,
        actors: list,
        use_cases: Any,
        title: str = "ULMS Online Use Case Diagram",
    ) -> str:
        """
        Generate a use case diagram.

        actors:
            A list of actor names or dictionaries with actor_id and name.

        use_cases:
            A list or UseCaseSet containing use cases.

        Expected use case fields:
            use_case_id, name, primary_actor, secondary_actors
        """

        cases = self._items(use_cases, "use_cases")

        lines = [
            "flowchart LR",
            f'    %% {self._escape_text(title)}',
            '    System["ULMS Online"]',
        ]

        actor_ids = {}
        case_ids = {}

        # Add actors.
        for index, actor in enumerate(actors, start=1):
            if isinstance(actor, str):
                actor_name = self._escape_text(actor)
                actor_key = f"ACTOR_{index}"
            else:
                actor_name = self._label(
                    actor,
                    "name",
                    f"Actor {index}",
                )
                actor_key = self._label(
                    actor,
                    "actor_id",
                    f"ACTOR_{index}",
                )

            # Mermaid identifiers must be unique and simple.
            node_id = f"A{index}"
            actor_ids[actor_name] = node_id

            lines.append(
                f'    {node_id}(["{actor_name}"])'
            )

        # Add use cases.
        for index, use_case in enumerate(cases, start=1):
            use_case_id = self._label(
                use_case,
                "use_case_id",
                f"UC-{index:02d}",
            )
            use_case_name = self._label(
                use_case,
                "name",
                f"Use Case {index}",
            )

            node_id = f"UC{index}"
            case_ids[use_case_id] = node_id

            lines.append(
                f'    {node_id}(("{use_case_name}"))'
            )

        # Connect actors to their use cases.
        for index, use_case in enumerate(cases, start=1):
            case_node = f"UC{index}"

            primary_actor = self._label(
                use_case,
                "primary_actor",
            )

            secondary_actors = self._get_value(
                use_case,
                "secondary_actors",
                [],
            ) or []

            if isinstance(secondary_actors, str):
                secondary_actors = [secondary_actors]

            all_actors = [primary_actor]

            all_actors.extend(
                self._escape_text(actor)
                for actor in secondary_actors
            )

            for actor_name in all_actors:
                if actor_name in actor_ids:
                    lines.append(
                        f"    {actor_ids[actor_name]} --- {case_node}"
                    )

        lines.append('    subgraph SYSTEM_BOUNDARY["System Boundary"]')
        for node_id in case_ids.values():
            lines.append(f"        {node_id}")
        lines.append("    end")

        return "\n".join(lines)


    # ==================================================
    # ACTIVITY DIAGRAM
    # ==================================================

    def activity_diagram(
        self,
        steps: list,
        title: str = "ULMS Online Activity Diagram",
    ) -> str:
        """
        Generate an activity diagram.

        Each step may be:
            "Enter search keyword"

        Or a dictionary:
            {
                "name": "Book available?",
                "type": "decision"
            }

        Supported step types:
            start, action, decision, end
        """

        if not steps:
            raise DiagramError(
                "At least one activity step is required."
            )

        lines = [
            "flowchart TD",
            f"    %% {self._escape_text(title)}",
        ]

        previous_node = None
        decision_node = None

        for index, step in enumerate(steps, start=1):
            if isinstance(step, str):
                name = self._escape_text(step)
                step_type = "action"
            else:
                name = self._label(step, "name", f"Step {index}")
                step_type = self._label(
                    step,
                    "type",
                    "action",
                ).lower()

            node_id = f"S{index}"

            if step_type == "start":
                lines.append(f'    {node_id}(["{name}"])')

            elif step_type == "decision":
                lines.append(f"    {node_id}{{{{{name}}}}}")
                decision_node = node_id

            elif step_type == "end":
                lines.append(f'    {node_id}(["{name}"])')

            else:
                lines.append(f'    {node_id}["{name}"]')

            if previous_node is not None:
                if decision_node == previous_node:
                    lines.append(
                        f"    {previous_node} --> {node_id}"
                    )
                else:
                    lines.append(
                        f"    {previous_node} --> {node_id}"
                    )

            previous_node = node_id

        return "\n".join(lines)


    # ==================================================
    # REQUIREMENT TRACEABILITY DIAGRAM
    # ==================================================

    def traceability_diagram(
        self,
        traceability: Any,
        title: str = "ULMS Requirement Traceability",
    ) -> str:
        """
        Generate a traceability diagram.

        Expected input:
            TraceabilityMatrix or a list of TraceabilityLink objects.

        Expected link fields:
            source_id, target_id, relationship
        """

        links = self._items(traceability, "links")

        lines = [
            "flowchart LR",
            f"    %% {self._escape_text(title)}",
        ]

        node_ids = {}

        def get_node_id(artifact_id: str) -> str:
            if artifact_id not in node_ids:
                node_ids[artifact_id] = f"N{len(node_ids) + 1}"

                lines.append(
                    f'    {node_ids[artifact_id]}["'
                    f'{self._escape_text(artifact_id)}"]'
                )

            return node_ids[artifact_id]

        for link in links:
            source = self._label(link, "source_id")
            target = self._label(link, "target_id")

            relationship = self._label(
                link,
                "relationship",
                "RELATED_TO",
            )

            if not source or not target:
                continue

            source_node = get_node_id(source)
            target_node = get_node_id(target)

            lines.append(
                f"    {source_node} -->|{relationship}| {target_node}"
            )

        if not links:
            lines.append('    EMPTY["No traceability links available"]')

        return "\n".join(lines)


    # ==================================================
    # HAZARD RISK DIAGRAM
    # ==================================================

    def hazard_risk_diagram(
        self,
        hazards: Any,
        title: str = "ULMS Hazard Risk Overview",
    ) -> str:
        """
        Generate a flowchart grouping hazards by risk level.

        Expected input:
            HazardSet or a list of Hazard objects.

        Hazard objects should provide:
            hazard_id, title, risk_level
        """

        hazard_items = self._items(hazards, "hazards")

        lines = [
            "flowchart TD",
            f"    %% {self._escape_text(title)}",
        ]

        risk_groups = {
            "LOW": [],
            "MEDIUM": [],
            "HIGH": [],
            "CRITICAL": [],
        }

        for hazard in hazard_items:
            hazard_id = self._label(
                hazard,
                "hazard_id",
                "HAZARD",
            )

            hazard_title = self._label(
                hazard,
                "title",
                hazard_id,
            )

            risk_level = self._label(
                hazard,
                "risk_level",
                "LOW",
            ).upper()

            if risk_level not in risk_groups:
                risk_level = "LOW"

            risk_groups[risk_level].append(
                (hazard_id, hazard_title)
            )

        lines.append('    ROOT["Hazard Risk Overview"]')

        for index, (risk_level, items) in enumerate(
            risk_groups.items(),
            start=1,
        ):
            group_id = f"RISK{index}"

            lines.append(
                f'    {group_id}["{risk_level} Risk"]'
            )

            lines.append(f"    ROOT --> {group_id}")

            for item_index, (hazard_id, title_text) in enumerate(
                items,
                start=1,
            ):
                node_id = f"H{index}_{item_index}"

                lines.append(
                    f'    {node_id}["{hazard_id}: {title_text}"]'
                )

                lines.append(
                    f"    {group_id} --> {node_id}"
                )

        return "\n".join(lines)


    # ==================================================
    # SAVE DIAGRAMS
    # ==================================================

    def save(
        self,
        diagram: str,
        filename: str,
    ) -> Path:
        """
        Save a Mermaid diagram definition to a text file.

        Example:
            generator.save(diagram, "use_case_diagram.mmd")
        """

        if not isinstance(diagram, str) or not diagram.strip():
            raise DiagramError(
                "Diagram content must not be empty."
            )

        output_path = self.output_dir / filename

        try:
            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            output_path.write_text(
                diagram,
                encoding="utf-8",
            )

            return output_path

        except OSError as exc:
            raise DiagramError(
                f"Could not save diagram to '{output_path}': {exc}"
            ) from exc