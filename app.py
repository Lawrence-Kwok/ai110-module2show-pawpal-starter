from datetime import time

import streamlit as st
from pawpal_system import AvailabilityWindow, Pet, Task, Owner, Scheduler

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", preferences="")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.divider()

st.subheader("Add a new pet")
owner_name = st.text_input(
    "Owner name",
    value=st.session_state.owner.name or "Jordan",
)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
gender = st.selectbox("Gender", ["male", "female", "other"])
st.session_state.owner.name = owner_name

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, gender=gender, breed=species)
    st.session_state.owner.add_pet(new_pet)

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": pet.name, "breed": pet.breed, "gender": pet.gender}
            for pet in st.session_state.owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

pet_options = {
    f"{index + 1}. {pet.name} ({pet.breed})": pet
    for index, pet in enumerate(st.session_state.owner.pets)
}

selected_pet_label = None
if pet_options:
    selected_pet_label = st.selectbox("Assign task to pet", list(pet_options.keys()))

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    scheduled_time = st.time_input("Scheduled time (optional)", value=None)

if st.button("Add task"):
    if selected_pet_label is None:
        st.warning("Add a pet before adding tasks.")
    else:
        task = Task(
            description=task_title,
            priority=priority,
            duration_minutes=int(duration),
            frequency="daily",
            scheduled_time=scheduled_time.strftime("%H:%M") if scheduled_time else None,
        )
        pet_options[selected_pet_label].add_task(task)

priority_order = {"high": 0, "medium": 1, "low": 2}

all_tasks_with_sort_keys = [
    (
        (
            0 if task.scheduled_time else 1,
            task.scheduled_time or "",
            priority_order.get(task.priority.lower(), 99),
        ),
        {
            "pet": pet.name,
            "title": task.description,
            "duration_minutes": task.duration_minutes,
            "priority": task.priority,
            "scheduled_time": task.scheduled_time or "auto",
        },
    )
    for pet in st.session_state.owner.pets
    for task in pet.tasks
]
all_tasks_with_sort_keys.sort(key=lambda entry: entry[0])
all_tasks = [row for _, row in all_tasks_with_sort_keys]

if all_tasks:
    st.write("Current tasks:")
    st.table(all_tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Auto-packed tasks (no scheduled time) are fit into this availability window.")

window_col1, window_col2 = st.columns(2)
with window_col1:
    window_start = st.time_input("Availability start", value=time(7, 0))
with window_col2:
    window_end = st.time_input("Availability end", value=time(8, 0))

if st.button("Generate schedule"):
    st.session_state.owner.availability_windows = [
        AvailabilityWindow(
            start_time=window_start.strftime("%H:%M"),
            end_time=window_end.strftime("%H:%M"),
        )
    ]
    scheduler = st.session_state.scheduler
    scheduler.generate_schedule(st.session_state.owner)
    scheduler.sort_by_time()
    st.session_state.schedule_generated = True

if st.session_state.get("schedule_generated"):
    scheduler = st.session_state.scheduler
    schedule = scheduler.retrieve_schedule()

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.markdown("#### ⚠️ Conflicts")
        for warning in conflicts:
            st.warning(warning)

    if not schedule:
        st.info("No tasks fit in the available time windows.")
    else:
        pet_filter_options = ["All pets"] + [pet.name for pet in st.session_state.owner.pets]
        pet_filter = st.selectbox("Filter schedule by pet", pet_filter_options)

        if pet_filter == "All pets":
            filtered_schedule = schedule
        else:
            filtered_schedule = scheduler.filter_by_pet(pet_filter)

        st.markdown("#### Generated schedule")
        if not filtered_schedule:
            st.info(f"No scheduled tasks for {pet_filter}.")
        else:
            st.table(
                [
                    {
                        "start_time": scheduled_task.start_time,
                        "end_time": scheduled_task.end_time,
                        "pet": scheduled_task.pet.name,
                        "task": scheduled_task.task.description,
                        "priority": scheduled_task.task.priority,
                    }
                    for scheduled_task in filtered_schedule
                ]
            )

    if not conflicts:
        st.success("No scheduling conflicts detected.")

