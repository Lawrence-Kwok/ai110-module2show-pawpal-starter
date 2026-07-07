from dataclasses import dataclass, field
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

    def mark_complete(self) -> None:
        self.status = True

    def mark_incomplete(self) -> None:
        self.status = False

    def edit_description(self, new_description: str) -> None:
        self.description = new_description

    def is_due_for(self, schedule_type: str) -> bool:
        if self.status:
            return False
        if self.frequency == "daily":
            return True
        if self.frequency == "weekly" and schedule_type == "weekly":
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
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks.copy()

    def get_incomplete_tasks(self) -> List[Task]:
        return [task for task in self.tasks if not task.status]


@dataclass
class Owner:
    name: str
    preferences: str
    availability_windows: List[AvailabilityWindow] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_all_incomplete_tasks(self) -> List[Task]:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_incomplete_tasks())
        return all_tasks

    def find_pet_for_task(self, task: Task) -> Optional["Pet"]:
        for pet in self.pets:
            if task in pet.tasks:
                return pet
        return None


@dataclass
class Scheduler:
    scheduled_tasks: List[ScheduledTask] = field(default_factory=list)

    def retrieve_schedule(self) -> List[ScheduledTask]:
        return self.scheduled_tasks.copy()

    def _time_to_minutes(self, time_value: str) -> int:
        hours_text, minutes_text = time_value.split(":")
        return int(hours_text) * 60 + int(minutes_text)

    def _minutes_to_time(self, total_minutes: int) -> str:
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"

    def generate_schedule(
        self,
        owner: Owner,
        pet: Optional[Pet] = None,
        schedule_type: str = "daily",
    ) -> List[ScheduledTask]:
        if pet is not None:
            candidate_tasks = pet.get_incomplete_tasks()
        else:
            candidate_tasks = owner.get_all_incomplete_tasks()

        due_tasks = [
            task for task in candidate_tasks
            if task.is_due_for(schedule_type)
        ]

        priority_order = {"high": 0, "medium": 1, "low": 2}

        due_tasks.sort(
            key=lambda task: (
                priority_order.get(task.priority.lower(), 99),
                task.duration_minutes,
            )
        )

        scheduled_tasks = []
        remaining_tasks = due_tasks.copy()

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

    def explain_schedule(self) -> str:
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