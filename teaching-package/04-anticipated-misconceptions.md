# Anticipated Misconceptions

## 1. "Authentication and authorization are the same thing"

### The misconception
Learners often use "auth" as a single concept. They think
that once a user is logged in, the security problem is
solved. They conflate "proving who you are" with "being
allowed to do something."

### Why learners naturally arrive here
Most tutorials bundle login and permissions into one
section called "Auth." The learner's first experience
is often: "add auth to your app" — one word for two
distinct problems. Also, in everyday life, showing your
ID and being granted access feel like one action.

### How to correct it without making the learner feel foolish
Start with validation: "This is a natural assumption —
the word 'auth' is genuinely ambiguous, and it trips up
professionals too."

Then use a concrete scenario: "You are logged in as a
Student. You try to create an assignment. What should
happen?" The learner will say "it should be rejected."
Ask: "But you ARE authenticated — the server knows who
you are. So which layer rejected you?" This creates the
distinction naturally. Authentication passed. Authorization
failed. Two different checks, two different error codes
(401 vs 403).

---

## 2. "Storing the JWT means my app is secure"

### The misconception
Learners believe that once they implement JWT login,
their application is secure. They focus on the token
mechanism and overlook everything around it: where the
token is stored, how long it lives, what happens when
it is stolen.

### Why learners naturally arrive here
JWT tutorials end with "you now have authentication!"
and the learner feels done. The token is cryptographically
signed, which sounds secure. They have not yet encountered
scenarios like token theft, XSS attacks extracting tokens
from localStorage, or the implications of long-lived tokens.

### How to correct it
Acknowledge the progress: "You have solved a real problem —
the server can now verify identity without a database
lookup on every request. That IS meaningful."

Then introduce a thought experiment: "Imagine someone
steals your access token. How long can they pretend to be
you?" Show that with a 15-minute token lifetime, the
damage window is small. With a 30-day token, it is
catastrophic. This leads naturally to: token lifetime
matters, refresh tokens reduce exposure, HTTPS prevents
interception, and where you store the token matters
(httpOnly cookies vs localStorage).

The goal is not to frighten them but to show that security
is layers, not a single mechanism.

---

## 3. "Checking the role in the view is enough for access control"

### The misconception
After learning role-based permissions, learners believe
that checking `if user.role == 'STUDENT'` in the view
function is sufficient to control access. They do not
see the need for object-level permission checks.

### Why learners naturally arrive here
For simple two-role systems (admin vs user), role checks
ARE sufficient. The learner has not yet encountered a
scenario where two users with the same role should see
different data. The Observer pattern — where Observer A
should see Student A's data but NOT Student B's data —
is their first exposure to this subtlety.

### How to correct it
Do not tell them they are wrong. Instead, create the bug
live. Set up two observers linked to different students.
Log in as Observer A and show that a role-only check
returns ALL students' data — including Student B's.

Ask: "Is this correct behavior?" They will see the
problem immediately. Then ask: "What additional check
would fix this?" Guide them to: "We need to check not
just the role, but whether this specific observer is
linked to this specific student."

This is the transition from role-level to row-level
thinking. Let the bug teach the lesson. The learner
discovers the need for has_object_permission through
a real failure, not a lecture.