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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
