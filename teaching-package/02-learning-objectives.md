# Learning Objectives

By the end of this session, learners will be able to:

## 1. Implement a JWT login endpoint that returns tokens containing the user's
role

The learner configures SimpleJWT, creates a custom token
serializer that embeds the role claim, and wires up the
login URL.

**Assessment:** The learner's /login/ endpoint returns a
JWT that, when decoded at jwt.io, shows a "role" field
matching the logged-in user.

## 2. Protect an API endpoint using a custom DRF permission class

The learner writes a permission class (e.g., IsStudent)
that checks request.user.role and applies it to a view
using permission_classes.

**Assessment:** Hitting the endpoint with Postman as the
wrong role returns 403 Forbidden. As the correct role,
it returns 200 OK.

## 3. Explain the difference between authentication and authorization

The learner can articulate: authentication verifies
identity (who are you), authorization controls access
(what can you do). They are separate concerns enforced
at separate layers.

**Assessment:** Given a scenario ("a logged-in Student
tries to create an assignment"), the learner correctly
identifies which layer rejects the request (authorization,
not authentication) and why (role check fails, not
token validation).

## 4. Demonstrate token refresh without re-entering credentials

The learner sends a refresh token to the /refresh/
endpoint and receives a new access token.

**Assessment:** In Postman, the learner shows the full
flow: login → use access token → call refresh → use
the new access token to make a request.

## 5. Distinguish between role-level and row-level permission checks

The learner can explain why checking role alone is
insufficient for the Observer scenario, and why
has_object_permission exists separately from
has_permission.

**Assessment:** The learner explains what would go wrong
if Observer permissions only checked the role field,
using the linked_student example.