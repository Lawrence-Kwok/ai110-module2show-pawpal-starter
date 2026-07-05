from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AvailabilityWindow:
    start_time: str   # example: "07:00"
    end_time: str     # example: "08:00"


@dataclass
class Task:
    description: str
    priority: str
    duration_minutes: int
    frequency: str
    preferred_window: Optional[str] = None   # "morning", "afternoon", "evening"
    status: bool = False

    def mark_complete(self) -> None:
        self.status = True

    def edit_description(self, new_description: str) -> None:
        self.description = new_description


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


@dataclass
class Scheduler:
    scheduled_tasks: List[Task] = field(default_factory=list)

    def retrieve_schedule(self) -> List[Task]:
        pass

    def generate_schedule(self, owner: Owner, pet: Pet) -> List[Task]:
        pass

    def explain_schedule(self) -> str:
        pass