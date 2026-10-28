"""
Export utilities for the University Library Management System Online.

Supported formats:
- JSON
- CSV
- Markdown

Supported data:
- Requirements
- Non-functional requirements (NFRs)
- Stakeholders
- Use cases
- Traceability links
"""

import csv
import json

from pathlib import Path
from typing import Any, Iterable


class ExportError(Exception):
    """Raised when exporting data fails."""


class DataExporter:
    """
    Export toolkit data to JSON, CSV, and Markdown files.

    Objects are expected to provide a to_dict() method.
    Dictionaries and lists of dictionaries are also supported.
    """

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # DATA CONVERSION
    # --------------------------------------------------

    @staticmethod
    def _to_dict(item: Any) -> dict:
        """
        Convert an object or dictionary into a dictionary.
        """
        if isinstance(item, dict):
            return item

        if hasattr(item, "to_dict") and callable(item.to_dict):
            result = item.to_dict()

            if isinstance(result, dict):
                return result

            raise ExportError(
                "The object's to_dict() method must return a dictionary."
            )

        raise ExportError(
            f"Unsupported data type: {type(item).__name__}"
        )

    @classmethod
    def _prepare_data(cls, data: Any) -> list[dict]:
        """
        Convert a collection or a single object into a list of dictionaries.

        Supported inputs:
        - A list or tuple of objects
        - A dictionary
        - An object with to_dict()
        - A toolkit collection exposing an attribute such as requirements,
          nfrs, stakeholders, use_cases, or links
        """
        if isinstance(data, dict):
            return [data]

        if isinstance(data, (list, tuple)):
            return [cls._to_dict(item) for item in data]

        # Handle toolkit collection classes.
        for attribute in (
            "requirements",
            "nfrs",
            "stakeholders",
            "use_cases",
            "links",
        ):
            if hasattr(data, attribute):
                items = getattr(data, attribute)

                if isinstance(items, (list, tuple)):
                    return [cls._to_dict(item) for item in items]

        # Handle a single data object.
        return [cls._to_dict(data)]

    # --------------------------------------------------
    # JSON EXPORT
    # --------------------------------------------------

    def export_json(
        self,
        data: Any,
        filename: str,
        indent: int = 4,
        encoding: str = "utf-8",
    ) -> Path:
        """
        Export data to a JSON file.

        Example:
            exporter.export_json(requirements, "requirements.json")
        """
        output_path = self.output_dir / filename

        try:
            records = self._prepare_data(data)

            with output_path.open(
                "w",
                encoding=encoding,
            ) as file:
                json.dump(
                    records,
                    file,
                    indent=indent,
                    ensure_ascii=False,
                    default=str,
                )

            return output_path

        except (OSError, TypeError, ValueError, ExportError) as exc:
            raise ExportError(
                f"Could not export JSON to '{output_path}': {exc}"
            ) from exc

    # --------------------------------------------------
    # CSV EXPORT
    # --------------------------------------------------

    def export_csv(
        self,
        data: Any,
        filename: str,
        encoding: str = "utf-8-sig",
    ) -> Path:
        """
        Export data to a CSV file.

        utf-8-sig helps Excel display Vietnamese text correctly.
        """
        output_path = self.output_dir / filename

        try:
            records = self._prepare_data(data)

            if not records:
                raise ExportError(
                    "Cannot export CSV because the dataset is empty."
                )

            # Combine fields from all records.
            fieldnames = []

            for record in records:
                for key in record.keys():
                    if key not in fieldnames:
                        fieldnames.append(key)

            with output_path.open(
                "w",
                newline="",
                encoding=encoding,
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=fieldnames,
                    extrasaction="ignore",
                )

                writer.writeheader()

                for record in records:
                    row = {
                        key: self._csv_value(record.get(key, ""))
                        for key in fieldnames
                    }
                    writer.writerow(row)

            return output_path

        except (OSError, TypeError, ValueError, ExportError) as exc:
            raise ExportError(
                f"Could not export CSV to '{output_path}': {exc}"
            ) from exc

    @staticmethod
    def _csv_value(value: Any) -> Any:
        """
        Convert nested values into strings suitable for CSV cells.
        """
        if isinstance(value, (dict, list, tuple, set)):
            return json.dumps(
                value,
                ensure_ascii=False,
                default=str,
            )

        return value

    # --------------------------------------------------
    # MARKDOWN EXPORT
    # --------------------------------------------------

    def export_markdown(
        self,
        data: Any,
        filename: str,
        title: str = "Exported Data",
    ) -> Path:
        """
        Export records as a Markdown table.
        """
        output_path = self.output_dir / filename

        try:
            records = self._prepare_data(data)

            lines = [
                f"# {title}",
                "",
                f"**Total records:** {len(records)}",
                "",
            ]

            if not records:
                lines.append("No data available.")
            else:
                fieldnames = []

                for record in records:
                    for key in record.keys():
                        if key not in fieldnames:
                            fieldnames.append(key)

                # Table header.
                lines.append(
                    "| " + " | ".join(
                        self._markdown_escape(key)
                        for key in fieldnames
                    ) + " |"
                )

                # Table separator.
                lines.append(
                    "| " + " | ".join("---" for _ in fieldnames) + " |"
                )

                # Table rows.
                for record in records:
                    values = [
                        self._markdown_escape(
                            self._markdown_value(record.get(key, ""))
                        )
                        for key in fieldnames
                    ]

                    lines.append("| " + " | ".join(values) + " |")

            output_path.write_text(
                "\n".join(lines) + "\n",
                encoding="utf-8",
            )

            return output_path

        except (OSError, TypeError, ValueError, ExportError) as exc:
            raise ExportError(
                f"Could not export Markdown to '{output_path}': {exc}"
            ) from exc

    @staticmethod
    def _markdown_value(value: Any) -> str:
        """
        Convert a value to readable text for Markdown.
        """
        if value is None:
            return ""

        if isinstance(value, (dict, list, tuple, set)):
            return json.dumps(
                value,
                ensure_ascii=False,
                default=str,
            )

        return str(value)

    @staticmethod
    def _markdown_escape(value: Any) -> str:
        """
        Escape characters that can break a Markdown table.
        """
        text = str(value)
        text = text.replace("\\", "\\\\")
        text = text.replace("|", "\\|")
        text = text.replace("\r\n", "<br>")
        text = text.replace("\n", "<br>")
        text = text.replace("\r", "<br>")
        return text

    # --------------------------------------------------
    # GENERIC EXPORT
    # --------------------------------------------------

    def export(
        self,
        data: Any,
        filename: str,
        file_format: str | None = None,
        title: str = "Exported Data",
    ) -> Path:
        """
        Export data based on the requested file format.

        If file_format is omitted, infer it from the filename extension.
        """
        if file_format is None:
            file_format = Path(filename).suffix.lstrip(".")

        file_format = file_format.lower().strip()

        if file_format == "json":
            return self.export_json(data, filename)

        if file_format == "csv":
            return self.export_csv(data, filename)

        if file_format in ("md", "markdown"):
            return self.export_markdown(
                data,
                filename,
                title=title,
            )

        raise ExportError(
            f"Unsupported export format: '{file_format}'. "
            "Supported formats are JSON, CSV, and Markdown."
        )


# --------------------------------------------------
# CONVENIENCE FUNCTIONS
# --------------------------------------------------

def export_requirements_json(
    requirements: Any,
    filename: str = "requirements.json",
    output_dir: str = "output",
) -> Path:
    """Export requirements to JSON."""
    return DataExporter(output_dir).export_json(
        requirements,
        filename,
    )


def export_nfrs_csv(
    nfrs: Any,
    filename: str = "nfrs.csv",
    output_dir: str = "output",
) -> Path:
    """Export NFRs to CSV."""
    return DataExporter(output_dir).export_csv(
        nfrs,
        filename,
    )


def export_stakeholders_csv(
    stakeholders: Any,
    filename: str = "stakeholders.csv",
    output_dir: str = "output",
) -> Path:
    """Export stakeholders to CSV."""
    return DataExporter(output_dir).export_csv(
        stakeholders,
        filename,
    )


def export_use_cases_markdown(
    use_cases: Any,
    filename: str = "use_cases.md",
    output_dir: str = "output",
) -> Path:
    """Export use cases to Markdown."""
    return DataExporter(output_dir).export_markdown(
        use_cases,
        filename,
        title="Use Cases",
    )