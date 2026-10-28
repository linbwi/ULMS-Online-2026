"""
Process Management Module for ULMS Online.

This module manages the software requirements engineering process:
1. Elicitation
2. Analysis
3. Specification
4. Validation
5. Approval
6. Implementation
7. Verification

It tracks process steps, status, progress, and completion.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ProcessPhase(Enum):
    """Phases of the requirements engineering process."""

    ELICITATION = "Elicitation"
    ANALYSIS = "Analysis"
    SPECIFICATION = "Specification"
    VALIDATION = "Validation"
    APPROVAL = "Approval"
    IMPLEMENTATION = "Implementation"
    VERIFICATION = "Verification"


class ProcessStatus(Enum):
    """Status of a process step."""

    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    BLOCKED = "Blocked"
    SKIPPED = "Skipped"


@dataclass
class ProcessStep:
    """Represents one step in the requirements engineering process."""

    step_id: str
    name: str
    phase: ProcessPhase
    description: str = ""
    status: ProcessStatus = ProcessStatus.NOT_STARTED
    responsible: str = ""
    related_requirements: list[str] = field(default_factory=list)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    notes: str = ""

    def start(self) -> None:
        """Start a process step."""
        if self.status == ProcessStatus.COMPLETED:
            raise ValueError(
                f"Cannot start completed step '{self.step_id}'."
            )

        self.status = ProcessStatus.IN_PROGRESS

        if self.start_date is None:
            self.start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def complete(self) -> None:
        """Mark a process step as completed."""
        if self.status == ProcessStatus.BLOCKED:
            raise ValueError(
                f"Cannot complete blocked step '{self.step_id}'."
            )

        self.status = ProcessStatus.COMPLETED

        if self.end_date is None:
            self.end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def block(self, reason: str = "") -> None:
        """Mark a process step as blocked."""
        self.status = ProcessStatus.BLOCKED

        if reason:
            self.notes = reason

    def reset(self) -> None:
        """Reset the step to its initial state."""
        self.status = ProcessStatus.NOT_STARTED
        self.start_date = None
        self.end_date = None
        self.notes = ""

    @property
    def is_completed(self) -> bool:
        """Return True if the step is completed."""
        return self.status == ProcessStatus.COMPLETED

    @property
    def duration_seconds(self) -> Optional[float]:
        """Return the duration in seconds if both dates are available."""
        if not self.start_date or not self.end_date:
            return None

        start = datetime.strptime(
            self.start_date, "%Y-%m-%d %H:%M:%S"
        )
        end = datetime.strptime(
            self.end_date, "%Y-%m-%d %H:%M:%S"
        )

        return (end - start).total_seconds()

    def to_dict(self) -> dict:
        """Convert the process step to a dictionary."""
        return {
            "step_id": self.step_id,
            "name": self.name,
            "phase": self.phase.value,
            "description": self.description,
            "status": self.status.value,
            "responsible": self.responsible,
            "related_requirements": self.related_requirements.copy(),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "notes": self.notes,
            "duration_seconds": self.duration_seconds,
        }


class RequirementsProcess:
    """Manages the requirements engineering process."""

    def __init__(self, process_name: str = "ULMS Requirements Process"):
        self.process_name = process_name
        self.steps: list[ProcessStep] = []

    def add_step(self, step: ProcessStep) -> None:
        """Add a process step."""
        if self.get_step(step.step_id) is not None:
            raise ValueError(
                f"Step ID '{step.step_id}' already exists."
            )

        self.steps.append(step)

    def get_step(self, step_id: str) -> Optional[ProcessStep]:
        """Find a step by its ID."""
        for step in self.steps:
            if step.step_id == step_id:
                return step

        return None

    def remove_step(self, step_id: str) -> bool:
        """Remove a step by its ID."""
        step = self.get_step(step_id)

        if step is None:
            return False

        self.steps.remove(step)
        return True

    def start_step(self, step_id: str) -> bool:
        """Start a step by its ID."""
        step = self.get_step(step_id)

        if step is None:
            return False

        step.start()
        return True

    def complete_step(self, step_id: str) -> bool:
        """Complete a step by its ID."""
        step = self.get_step(step_id)

        if step is None:
            return False

        step.complete()
        return True

    def block_step(self, step_id: str, reason: str = "") -> bool:
        """Block a step by its ID."""
        step = self.get_step(step_id)

        if step is None:
            return False

        step.block(reason)
        return True

    def get_steps_by_status(
        self,
        status: ProcessStatus,
    ) -> list[ProcessStep]:
        """Return all steps with a specified status."""
        return [
            step for step in self.steps
            if step.status == status
        ]

    def get_steps_by_phase(
        self,
        phase: ProcessPhase,
    ) -> list[ProcessStep]:
        """Return all steps belonging to a phase."""
        return [
            step for step in self.steps
            if step.phase == phase
        ]

    @property
    def total_steps(self) -> int:
        return len(self.steps)

    @property
    def completed_steps(self) -> int:
        return sum(
            1 for step in self.steps
            if step.status == ProcessStatus.COMPLETED
        )

    @property
    def progress_percentage(self) -> float:
        """Calculate the percentage of completed process steps."""
        if not self.steps:
            return 0.0

        return round(
            self.completed_steps / self.total_steps * 100,
            2,
        )

    @property
    def is_completed(self) -> bool:
        """Return True if every step is completed or skipped."""
        return all(
            step.status in {
                ProcessStatus.COMPLETED,
                ProcessStatus.SKIPPED,
            }
            for step in self.steps
        )

    def get_next_step(self) -> Optional[ProcessStep]:
        """Return the first step that has not been completed or skipped."""
        for step in self.steps:
            if step.status in {
                ProcessStatus.NOT_STARTED,
                ProcessStatus.IN_PROGRESS,
            }:
                return step

        return None

    def get_blocked_steps(self) -> list[ProcessStep]:
        """Return all blocked steps."""
        return self.get_steps_by_status(ProcessStatus.BLOCKED)

    def get_summary(self) -> dict:
        """Return an overview of the process."""
        status_counts = {
            status.value: len(self.get_steps_by_status(status))
            for status in ProcessStatus
        }

        return {
            "process_name": self.process_name,
            "total_steps": self.total_steps,
            "completed_steps": self.completed_steps,
            "progress_percentage": self.progress_percentage,
            "is_completed": self.is_completed,
            "blocked_steps": len(self.get_blocked_steps()),
            "status_counts": status_counts,
        }

    def to_dict(self) -> dict:
        """Convert the complete process to a dictionary."""
        return {
            "process_name": self.process_name,
            "summary": self.get_summary(),
            "steps": [step.to_dict() for step in self.steps],
        }

    def print_report(self) -> None:
        """Print a readable process report."""
        summary = self.get_summary()

        print("\n" + "=" * 65)
        print(f"PROCESS REPORT: {self.process_name}")
        print("=" * 65)

        print(f"Total steps:       {summary['total_steps']}")
        print(f"Completed steps:   {summary['completed_steps']}")
        print(f"Progress:          {summary['progress_percentage']}%")
        print(f"Blocked steps:     {summary['blocked_steps']}")
        print(f"Process completed: {summary['is_completed']}")

        print("\nPROCESS STEPS")
        print("-" * 65)

        for step in self.steps:
            print(
                f"{step.step_id} | "
                f"{step.phase.value:<15} | "
                f"{step.name:<25} | "
                f"{step.status.value}"
            )

        next_step = self.get_next_step()

        print("-" * 65)

        if next_step:
            print(
                f"Next step: {next_step.step_id} - {next_step.name}"
            )
        else:
            print("No pending steps.")

        print("=" * 65)