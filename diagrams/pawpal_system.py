from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    priority: str
    duration: int
    status: bool = False

    def mark_complete(self) -> None:
        pass

    def edit_description(self, new_description: str) -> None:
        pass


@dataclass
class Pet:
    name: str
    gender: str
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    preferences: str
    available_minutes: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass


@dataclass
class Scheduler:
    scheduled_tasks: List[Task] = field(default_factory=list)

    def retrieve_schedule(self) -> List[Task]:
        pass

    def generate_schedule(self, owner: Owner, pet: Pet) -> List[Task]:
        pass

    def explain_schedule(self) -> str:
        pass