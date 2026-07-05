# PawPal+ Project Reflection

## 1. System Design

What Actions Should Users Be Able to Perform:
1. Add or Remove Pet Entries 
2. Edit Pet and User Information
3. Add or Remove Tasks
4. Edit Task Information and Duration
5. Create and/or Remove Schedules
6. Edit Schedules/Plans

What Entities Need to Exist:
1. Pets
2. Owners
3. Tasks
4. Schedules

**a. Initial design**

As part of the initial design, the base 4 classes were included: Owner, Pet, Task, and the Scheduler. For the first three, each functioned as entities with their own properties, where the owner has a list of pets that they could have ownership over and pets with a list of tasks associated with them. In terms of responsibilities, tasks are the inherent basic entity which the entire project is dependent on, containing the information of importance, length, and status in order to be organized into the schedule for the owner. Pets also contain their own inherent traits to be used in other tasks should they be deemed relevant. Owner while not containing much beyond the list of pets, have a unique field for containing the owners perferences to add context for the scheduler to use.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

One change suggested during the skeleton implementation is adding a field for time availability for the owner, which was overlooked in the initial iteration. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
