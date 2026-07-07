from pawpal_system import Pet, Task


def test_mark_complete_sets_task_status_to_true() -> None:
	task = Task(
		description="Morning walk",
		priority="high",
		duration_minutes=30,
		frequency="daily",
	)

	task.mark_complete()

	assert task.status is True


def test_add_task_increases_pet_task_count() -> None:
	pet = Pet(name="Gummi", gender="female", breed="Shiba Inu")
	task = Task(
		description="Breakfast feeding",
		priority="high",
		duration_minutes=15,
		frequency="daily",
	)

	starting_count = len(pet.get_tasks())

	pet.add_task(task)

	assert len(pet.get_tasks()) == starting_count + 1
