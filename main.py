from pawpal_system import (
	AvailabilityWindow,
	Owner,
	Pet,
	Scheduler,
	Task,
	print_schedule,
)

def build_sample_schedule() -> None:
	owner = Owner(
		name="Jordan",
		preferences="Prefers care tasks to be finished early when possible.",
		availability_windows=[
			AvailabilityWindow(start_time="07:00", end_time="08:00"),
			AvailabilityWindow(start_time="18:00", end_time="19:00"),
		],
	)

	gummi = Pet(name="Gummi", gender="female", breed="Shiba Inu")
	mocha = Pet(name="Mocha", gender="male", breed="Tabby Cat")

	owner.add_pet(gummi)
	owner.add_pet(mocha)

	morning_walk = Task(
		description="Morning walk",
		priority="high",
		duration_minutes=30,
		frequency="daily",
	)
	breakfast = Task(
		description="Breakfast feeding",
		priority="high",
		duration_minutes=15,
		frequency="daily",
	)
	medication = Task(
		description="Evening medication",
		priority="medium",
		duration_minutes=10,
		frequency="daily",
	)
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
	# Tasks are added out of order on purpose to exercise sort_by_time().
	mocha.add_task(nail_trim)
	mocha.add_task(medication)
	gummi.add_task(breakfast)
	mocha.add_task(grooming)
	gummi.add_task(morning_walk)

	scheduler = Scheduler()
	schedule = scheduler.generate_schedule(owner)

	print("Today's Schedule (generated order)")
	print("-" * 34)
	print_schedule(schedule)

	print("\nToday's Schedule (sorted by time)")
	print("-" * 34)
	print_schedule(scheduler.sort_by_time())

	print("\nIncomplete Tasks Only")
	print("-" * 34)
	print_schedule(scheduler.filter_by_status(completed=False))

	print("\nCompleted Tasks Only")
	print("-" * 34)
	print_schedule(scheduler.filter_by_status(completed=True))

	print("\nTasks for Mocha")
	print("-" * 34)
	print_schedule(scheduler.filter_by_pet("Mocha"))

	print("\nSchedule Conflicts")
	print("-" * 34)
	conflicts = scheduler.detect_conflicts()
	if not conflicts:
		print("No conflicts detected.")
	else:
		for warning in conflicts:
			print(warning)


if __name__ == "__main__":
	build_sample_schedule()
