from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class AvailabilityWindow:
    start_time: str
    end_time: str


@dataclass
class Task:
    description: str
    priority: str
    duration_minutes: int
    frequency: str
    preferred_window: Optional[str] = None
    status: bool = False
    due_date: Optional[date] = None
    scheduled_time: Optional[str] = None

    def mark_complete(self) -> Optional["Task"]:
        """Mark the task as completed.

        If the task recurs ("daily" or "weekly"), return a new Task instance
        for the next occurrence so it can be re-added to the pet's task list.
        """
        self.status = True
        return self.next_occurrence()

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.status = False

    def next_occurrence(self) -> Optional["Task"]:
        """Return a new Task for the next due date, or None if not recurring."""
        if self.frequency == "daily":
            next_due_date = (self.due_date or date.today()) + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due_date = (self.due_date or date.today()) + timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            priority=self.priority,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            preferred_window=self.preferred_window,
            due_date=next_due_date,
            scheduled_time=self.scheduled_time,
        )

    def edit_description(self, new_description: str) -> None:
        """Update the task description."""
        self.description = new_description

    def is_due_for(self, schedule_type: str) -> bool:
        """Return whether the task should be included for the schedule type."""
        if self.status:
            return False
        if self.frequency == "daily":
            return True
        if self.frequency == "weekly" and schedule_type == "weekly":
            return True
        if self.frequency == "one-off":
            return True
        return False


@dataclass
class ScheduledTask:
    pet: "Pet"
    task: Task
    start_time: str
    end_time: str


@dataclass
class Pet:
    name: str
    gender: str
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet if it is not already assigned."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet if it is assigned."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return a copy of the pet's tasks."""
        return self.tasks.copy()

    def get_incomplete_tasks(self) -> List[Task]:
        """Return the pet's tasks that are not yet completed."""
        return [task for task in self.tasks if not task.status]

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete and add its next occurrence, if any.

        Returns the newly created Task for the next occurrence, or None if
        the task does not recur.
        """
        next_task = task.mark_complete()
        if next_task is not None:
            self.add_task(next_task)
        return next_task


@dataclass
class Owner:
    name: str
    preferences: str
    availability_windows: List[AvailabilityWindow] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner if it is not already tracked."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner if it is currently tracked."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task assigned across all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_all_incomplete_tasks(self) -> List[Task]:
        """Return every incomplete task across all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_incomplete_tasks())
        return all_tasks

    def find_pet_for_task(self, task: Task) -> Optional["Pet"]:
        """Return the pet associated with a task, if one exists."""
        for pet in self.pets:
            if task in pet.tasks:
                return pet
        return None


@dataclass
class Scheduler:
    scheduled_tasks: List[ScheduledTask] = field(default_factory=list)

    def retrieve_schedule(self) -> List[ScheduledTask]:
        """Return a copy of the scheduled task entries."""
        return self.scheduled_tasks.copy()

    def _time_to_minutes(self, time_value: str) -> int:
        """Convert an HH:MM time string into total minutes."""
        hours_text, minutes_text = time_value.split(":")
        return int(hours_text) * 60 + int(minutes_text)

    def _minutes_to_time(self, total_minutes: int) -> str:
        """Convert total minutes into an HH:MM time string."""
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"

    def generate_schedule(
        self,
        owner: Owner,
        pet: Optional[Pet] = None,
        schedule_type: str = "daily",
    ) -> List[ScheduledTask]:
        """Build a schedule by fitting due tasks into the owner's time windows."""
        if pet is not None:
            candidate_tasks = pet.get_incomplete_tasks()
        else:
            candidate_tasks = owner.get_all_incomplete_tasks()

        due_tasks = [
            task for task in candidate_tasks
            if task.is_due_for(schedule_type)
        ]

        priority_order = {"high": 0, "medium": 1, "low": 2}

        scheduled_tasks = []

        fixed_time_tasks = [task for task in due_tasks if task.scheduled_time is not None]
        auto_pack_tasks = [task for task in due_tasks if task.scheduled_time is None]

        for task in fixed_time_tasks:
            task_pet = pet if pet is not None else owner.find_pet_for_task(task)
            if task_pet is None:
                continue

            task_start = self._time_to_minutes(task.scheduled_time)
            task_end = task_start + task.duration_minutes

            fits_in_a_window = any(
                task_start >= self._time_to_minutes(window.start_time)
                and task_end <= self._time_to_minutes(window.end_time)
                for window in owner.availability_windows
            )
            if not fits_in_a_window:
                continue

            scheduled_tasks.append(
                ScheduledTask(
                    pet=task_pet,
                    task=task,
                    start_time=task.scheduled_time,
                    end_time=self._minutes_to_time(task_end),
                )
            )

        auto_pack_tasks.sort(
            key=lambda task: (
                priority_order.get(task.priority.lower(), 99),
                task.duration_minutes,
            )
        )

        remaining_tasks = auto_pack_tasks.copy()

        for window in owner.availability_windows:
            current_time = self._time_to_minutes(window.start_time)
            window_end = self._time_to_minutes(window.end_time)
            remaining_minutes = window_end - current_time

            if remaining_minutes <= 0:
                continue

            unscheduled_tasks = []
            for task in remaining_tasks:
                if task.duration_minutes > remaining_minutes:
                    unscheduled_tasks.append(task)
                    continue

                task_pet = pet if pet is not None else owner.find_pet_for_task(task)
                if task_pet is None:
                    unscheduled_tasks.append(task)
                    continue

                task_start = current_time
                task_end = task_start + task.duration_minutes
                scheduled_tasks.append(
                    ScheduledTask(
                        pet=task_pet,
                        task=task,
                        start_time=self._minutes_to_time(task_start),
                        end_time=self._minutes_to_time(task_end),
                    )
                )
                current_time = task_end
                remaining_minutes = window_end - current_time

            remaining_tasks = unscheduled_tasks

            if not remaining_tasks:
                break

        self.scheduled_tasks = scheduled_tasks
        return self.retrieve_schedule()

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for any scheduled tasks whose times overlap.

        This is a lightweight, quadratic pairwise check over the current
        scheduled_tasks list. It never raises; it just reports overlaps
        (same pet or different pets) as human-readable warning strings.
        """
        warnings = []
        entries = self.scheduled_tasks

        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                first = entries[i]
                second = entries[j]

                first_start = self._time_to_minutes(first.start_time)
                first_end = self._time_to_minutes(first.end_time)
                second_start = self._time_to_minutes(second.start_time)
                second_end = self._time_to_minutes(second.end_time)

                overlaps = first_start < second_end and second_start < first_end
                if not overlaps:
                    continue

                warnings.append(
                    f"Conflict: {first.pet.name}'s '{first.task.description}' "
                    f"({first.start_time}-{first.end_time}) overlaps with "
                    f"{second.pet.name}'s '{second.task.description}' "
                    f"({second.start_time}-{second.end_time})."
                )

        return warnings

    def sort_by_time(self) -> List[ScheduledTask]:
        """Sort the scheduled tasks in place by their start time (HH:MM)."""
        self.scheduled_tasks.sort(key=lambda scheduled_task: self._time_to_minutes(scheduled_task.start_time))
        return self.retrieve_schedule()

    def filter_by_status(self, completed: bool) -> List[ScheduledTask]:
        """Return scheduled tasks whose task completion status matches."""
        return [
            scheduled_task for scheduled_task in self.scheduled_tasks
            if scheduled_task.task.status == completed
        ]

    def filter_by_pet(self, pet_name: str) -> List[ScheduledTask]:
        """Return scheduled tasks belonging to the pet with the given name."""
        return [
            scheduled_task for scheduled_task in self.scheduled_tasks
            if scheduled_task.pet.name == pet_name
        ]

    def explain_schedule(self) -> str:
        """Explain why each scheduled task was included in the plan."""
        if not self.scheduled_tasks:
            return "No tasks are currently scheduled."

        explanations = []
        for scheduled_task in self.scheduled_tasks:
            explanations.append(
                f"{scheduled_task.start_time}-{scheduled_task.end_time}: "
                f"{scheduled_task.task.description} for {scheduled_task.pet.name} was scheduled because it is "
                f"{scheduled_task.task.frequency}, has "
                f"{scheduled_task.task.priority} priority, and fit in the "
                f"available time window."
            )

        return "\n".join(explanations)


def print_schedule(entries: List[ScheduledTask]) -> None:
    """Print a list of scheduled tasks, or a message if there are none."""
    if not entries:
        print("No tasks fit in the available time windows.")
        return

    for scheduled_task in entries:
        task = scheduled_task.task
        print(
            f"{scheduled_task.start_time}-{scheduled_task.end_time} | "
            f"{scheduled_task.pet.name}: {task.description} "
            f"({task.duration_minutes} min, {task.priority} priority)"
        )