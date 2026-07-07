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

The constraints that the scheduler is considering is time in HH:MM format and priority. Preferences hasn't been applied
as of the time of posting which maybe improved in future iterations. Time and priority were considered most since those
were the most deterministic of the three, with preference requiring more thinking in the future for implementation (whether
it is a deterministic task or if it supersedes priority). With the other two its more black and white in terms of determination
with either the tasks cannot co-exist or if the task has been assigned the appropriate order of priority. Priority and then time
is considered.

**b. Tradeoffs**

A tradeoff the scheduler makes is scheduling by priority first by default; this makes sense since normally tasks are not of equal importance, and tasks that are important
should be handled first rather than just slotting as first come first serve by time.

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

I'm somewhat satisfied with the changing of the project as new constraints or information came to play, as prompting
allowed me to make changes to accomodate these new requirements and force me to think of what areas need to be adjusted.
I cannot say the same for the quality of the project, as I still believe it can be furthered refined or be started as a
stronger more clean system from scratch. 

**b. What you would improve**

If I had another iteration, I would spend more time redesigning the system to focus more on the scheduling aspect by date
rather than the vague daily and weekly system with the HH:MM system that is currently scaffolded together, as I don't think
the current solution is as elegant or robust as it can be. What held me back from completing the project in a timely manner
is the lack of a good mental model of the entire system, which I should've approached in two different methods: either spend
more time reading all the steps rather than follow step by step which would've helped me to understand what future requirements
I need to account for rather than changing an initial model since it messes up the mental model alot more and thus my understanding
of the system; or quickly make a throwaway prototype to improve my understanding via trial and error, as it would allow me to firsthand
understand the pitfalls and where my understanding is lacking. 


**c. Key takeaway**

Most important part of designing systems and working with AI on this project is the fact that the project is
only as good as the programmer is on developing the actual system. I'm not particularly proud of the implementation
since I delegated a huge portion of the programming to the LLM with more vague prompting and not fully understanding
the entire scope of the project before starting, which required a huge amount of finagling with the time system and
refactoring to address additional constraints and other nuances. If you have a clear idea or are able to catch systematic
issues before other systems are integrated with such work, it makes it alot easier to modify the files, but if refactoring
or the mental model changes late, then much more refactoring is needed, often times system-wide.