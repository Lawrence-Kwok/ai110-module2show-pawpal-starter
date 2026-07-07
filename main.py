from diagrams.pawpal_system import (
	AvailabilityWindow,
	Owner,
	Pet,
	Scheduler,
	Task,
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
	)
	grooming.mark_complete()

	gummi.add_task(morning_walk)
	gummi.add_task(breakfast)
	mocha.add_task(medication)
	mocha.add_task(grooming)

	scheduler = Scheduler()
	schedule = scheduler.generate_schedule(owner)

	print("Today's Schedule")
	print("-" * 16)

	if not schedule:
		print("No tasks fit in the available time windows.")
		return

	for scheduled_task in schedule:
		task = scheduled_task.task
		print(
			f"{scheduled_task.start_time}-{scheduled_task.end_time} | "
			f"{scheduled_task.pet.name}: {task.description} "
			f"({task.duration_minutes} min, {task.priority} priority)"
		)


if __name__ == "__main__":
	build_sample_schedule()
