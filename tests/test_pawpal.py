from datetime import date, timedelta

from pawpal_system import Pet, Scheduler, ScheduledTask, Task


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


def test_sort_by_time_orders_tasks_chronologically() -> None:
	pet = Pet(name="Gummi", gender="female", breed="Shiba Inu")

	evening_task = Task(
		description="Evening medication",
		priority="medium",
		duration_minutes=10,
		frequency="daily",
	)
	morning_task = Task(
		description="Morning walk",
		priority="high",
		duration_minutes=30,
		frequency="daily",
	)
	midday_task = Task(
		description="Lunch feeding",
		priority="high",
		duration_minutes=15,
		frequency="daily",
	)

	scheduler = Scheduler(
		scheduled_tasks=[
			ScheduledTask(pet=pet, task=evening_task, start_time="18:00", end_time="18:10"),
			ScheduledTask(pet=pet, task=morning_task, start_time="07:00", end_time="07:30"),
			ScheduledTask(pet=pet, task=midday_task, start_time="12:00", end_time="12:15"),
		]
	)

	sorted_schedule = scheduler.sort_by_time()

	assert [entry.start_time for entry in sorted_schedule] == ["07:00", "12:00", "18:00"]


def test_mark_complete_on_daily_task_creates_next_day_occurrence() -> None:
	today = date(2026, 7, 7)
	task = Task(
		description="Morning walk",
		priority="high",
		duration_minutes=30,
		frequency="daily",
		due_date=today,
	)

	next_task = task.mark_complete()

	assert task.status is True
	assert next_task is not None
	assert next_task.status is False
	assert next_task.due_date == today + timedelta(days=1)
	assert next_task.description == task.description
	assert next_task.priority == task.priority
	assert next_task.duration_minutes == task.duration_minutes
	assert next_task.frequency == task.frequency


def test_detect_conflicts_flags_overlapping_scheduled_times() -> None:
	gummi = Pet(name="Gummi", gender="female", breed="Shiba Inu")
	mocha = Pet(name="Mocha", gender="male", breed="Tabby Cat")

	grooming = Task(
		description="Brush coat",
		priority="low",
		duration_minutes=20,
		frequency="daily",
		scheduled_time="07:00",
	)
	nail_trim = Task(
		description="Nail trim",
		priority="high",
		duration_minutes=15,
		frequency="daily",
		scheduled_time="07:00",
	)

	scheduler = Scheduler(
		scheduled_tasks=[
			ScheduledTask(pet=gummi, task=grooming, start_time="07:00", end_time="07:20"),
			ScheduledTask(pet=mocha, task=nail_trim, start_time="07:00", end_time="07:15"),
		]
	)

	conflicts = scheduler.detect_conflicts()

	assert len(conflicts) == 1
	assert "Gummi" in conflicts[0]
	assert "Mocha" in conflicts[0]


def test_detect_conflicts_ignores_back_to_back_non_overlapping_times() -> None:
	pet = Pet(name="Gummi", gender="female", breed="Shiba Inu")

	first_task = Task(
		description="Morning walk",
		priority="high",
		duration_minutes=15,
		frequency="daily",
		scheduled_time="07:00",
	)
	second_task = Task(
		description="Breakfast feeding",
		priority="high",
		duration_minutes=15,
		frequency="daily",
		scheduled_time="07:15",
	)

	scheduler = Scheduler(
		scheduled_tasks=[
			ScheduledTask(pet=pet, task=first_task, start_time="07:00", end_time="07:15"),
			ScheduledTask(pet=pet, task=second_task, start_time="07:15", end_time="07:30"),
		]
	)

	conflicts = scheduler.detect_conflicts()

	assert conflicts == []
