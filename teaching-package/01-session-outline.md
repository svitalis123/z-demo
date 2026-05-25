# Session Outline: Authentication & Authorization with Django REST Framework

## Session Flow (60 minutes)

### 0:00–0:05 — Hook: "What stops anyone from seeing your data?"

Open Postman. Hit the assignments endpoint WITHOUT a token.
Show the 401 response. Ask: "What just happened? Why were
you rejected?" This motivates the entire session — security
is not abstract, it is the first thing the API enforces.

### 0:05–0:15 — Concept: Authentication vs Authorization

Teach the core distinction using the building analogy:
- Authentication = showing your ID badge at the front door
- Authorization = which rooms your badge grants access to

Show a diagram of the flow: request → authentication
middleware → permission check → view → response.

### 0:15–0:25 — Live Demo: JWT Login + Token Decode

Walk through the demo app in Postman:
1. POST to /login/ with instructor credentials
2. Copy the access token
3. Paste into jwt.io — decode and inspect the payload
4. Show the role claim embedded in the token
5. Use the token to hit /assignments/ — it works
6. Try with an expired/invalid token — 401

### 0:25–0:35 — Guided Practice: Implement Login Together

Learners follow along on their machines:
1. Install SimpleJWT
2. Add the settings configuration
3. Create the login URL
4. Test in Postman

This is the "we do it together" phase. Mistakes are
expected and encouraged — retry until it works.

### 0:35–0:50 — Practice Problem: Build a Permission Class

Learners work independently to create an `IsStudent`
permission class and apply it to a view. This is a
Practice Problem, not an assessment — unlimited retries.

Success criteria: when they hit the endpoint as an
Instructor, they get 403. As a Student, they get 200.

Circulate the room. Help anyone stuck. Celebrate when
it clicks.

### 0:50–0:55 — Stretch: Row-Level vs Role-Level Permissions

Show the Observer scenario. Ask: "If we only check
role == OBSERVER, what goes wrong?" Let them think.
Then show: Observer A could see Observer B's student.
Introduce has_object_permission as the fix.

This is a stretch concept — not everyone will fully
grasp it today, and that is fine. Plant the seed.

### 0:55–1:00 — Recap + Take-Home Practice

Summarize the three layers: authentication (who are you),
role-level authorization (what type are you), row-level
authorization (what specific data is yours). Point to
the concept explainer document for review.

## Why This Order

The session follows the "motivation → concept → demo →
guided practice → independent practice" progression.
Learners see the WHY before the HOW. They see a working
version before building their own. They practice with
support before working alone. Each step builds on the
previous one, and no step requires knowledge that has
not yet been introduced.
