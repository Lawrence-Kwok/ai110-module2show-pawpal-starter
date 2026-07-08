# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Today's Schedule
----------------
07:00-07:15 | Gummi: Breakfast feeding (15 min, high priority)
07:15-07:45 | Gummi: Morning walk (30 min, high priority)
07:45-07:55 | Mocha: Evening medication (10 min, medium priority)

## 🧪 Testing PawPal+

Run the test suite from the project root with:

```bash
python -m pytest
```

The suite (`tests/test_pawpal.py`) covers the following scheduling behaviors:

- **Task completion** — marking a task complete sets its status correctly.
- **Recurrence logic** — completing a "daily" task creates a new, incomplete `Task` instance due the following day with the same description, priority, duration, and frequency.
- **Pet task management** — adding a task to a `Pet` increases its task count.
- **Chronological sorting** — `Scheduler.sort_by_time` orders scheduled tasks by start time regardless of the order they were added.
- **Conflict detection** — `Scheduler.detect_conflicts` flags overlapping scheduled times across different pets, and correctly ignores back-to-back tasks that touch but don't overlap (boundary case).

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.10.7, pytest-9.0.3, pluggy-1.6.0 -- /usr/local/bin/python3
cachedir: .pytest_cache
rootdir: /Users/lawrence/Documents/GitHub/ai110-module2show-pawpal-starter
plugins: anyio-4.0.0
collecting ... collected 6 items

tests/test_pawpal.py::test_mark_complete_sets_task_status_to_true PASSED [ 16%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 33%]
tests/test_pawpal.py::test_sort_by_time_orders_tasks_chronologically PASSED [ 50%]
tests/test_pawpal.py::test_mark_complete_on_daily_task_creates_next_day_occurrence PASSED [ 66%]
tests/test_pawpal.py::test_detect_conflicts_flags_overlapping_scheduled_times PASSED [ 83%]
tests/test_pawpal.py::test_detect_conflicts_ignores_back_to_back_non_overlapping_times PASSED [100%]

============================== 6 passed in 0.01s ===============================
```

**Confidence Level:** ⭐⭐☆☆☆ (2/5)

All 6 tests pass, and the bare minimum recurrence, sorting, and conflict-detection logic. However, coverage isn't comprehensive enough with the dropping tasks that don't fit, putting behavior into correct windows, and other edge cases that are still to be determined.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.generate_schedule` | Auto-pack tasks are sorted by priority (high → medium → low), then by shorter duration first, before being fit into the owner's availability windows. |
| Filtering | `Task.is_due_for`, `Pet.get_incomplete_tasks`, `Owner.get_all_incomplete_tasks` | Only incomplete tasks due for the requested schedule type ("daily"/"weekly"/"one-off") are considered candidates; tasks that no longer fit in a window's remaining time are pushed to `unscheduled_tasks` and skipped. |
| Conflict handling | `Scheduler.detect_conflicts` | After a schedule is generated, a pairwise (O(n²)) check compares every pair of `ScheduledTask` start/end times and reports human-readable overlap warnings (does not prevent the overlap, just flags it). |
| Recurring tasks | `Task.next_occurrence`, `Task.mark_complete`, `Pet.mark_task_complete` | Completing a "daily" or "weekly" task automatically creates and re-adds a new `Task` for the next due date; one-off tasks return `None` and are not recreated. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Create an entry for a pet with an owner
2. Select pet to add task to 
3. Fill out task information (scheduled time is optional, it will autoslot into
available timeslots if available)
4. Select window of availability (start, end)
5. Generate schedule
6. Click filter by pet to filter for a specific pet

