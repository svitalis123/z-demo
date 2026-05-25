# Concept Explainers

## 1. Authentication vs Authorization

These two words sound similar but solve different problems.

**Authentication** answers: "Who are you?"
When you POST to /api/v1/auth/login/ with your email and
password, the server verifies your identity. If valid,
it returns a token that proves who you are.

**Authorization** answers: "What are you allowed to do?"
When you send a request with your token, the server first
confirms your identity (authentication), then checks
whether your role permits the action (authorization).

**Analogy:** Think of a university building.
- Authentication = swiping your student ID at the entrance.
  The system confirms you are a real student.
- Authorization = which rooms your card opens. A student
  card opens the lab. A professor card also opens the
  faculty office. The janitor card opens everything.

In code, these map to two DRF concepts:
- Authentication classes verify the token →
  `JWTAuthentication`
- Permission classes check what the user can do →
  `IsInstructor`, `IsStudent`

```python
# This is authentication — verifying the token
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# This is authorization — checking the role
class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'INSTRUCTOR'

A request can be authenticated (valid token) but
unauthorized (wrong role). A 401 means "I don't know
who you are." A 403 means "I know who you are, but
you can't do this."

---
2. How JWTs Work

A JSON Web Token has three parts, separated by dots:

eyJhbGciOi...  .  eyJ1c2VyX2lk...  .  SflKxwRJSM...
[  HEADER  ]     [   PAYLOAD   ]     [ SIGNATURE ]

Header — says which algorithm was used to sign the
  token (e.g., HS256).

Payload — contains claims (data). In our app:
{
  "user_id": "a1b2c3...",
  "role": "STUDENT",
  "email": "student@demo.dev",
  "exp": 1716700000
}

The exp claim is the expiration timestamp. After this
time, the token is rejected.

Signature — the server signs header + payload with
a SECRET_KEY. If anyone tampers with the payload (e.g.,
changes role from STUDENT to INSTRUCTOR), the signature
won't match and the server rejects the token.

Why JWTs instead of session cookies for APIs:
Session Cookies: Server stores session data in a database
JWTs: Token is self-contained — no server storage
────────────────────────────────────────
Session Cookies: Tied to one server (or needs shared session store)
JWTs: Works across multiple servers
────────────────────────────────────────
Session Cookies: Browser sends automatically
JWTs: Client sends explicitly in Authorization header
────────────────────────────────────────
Session Cookies: Good for traditional web apps
JWTs: Good for APIs consumed by mobile, SPA, other services


The refresh flow:
1. Login → get access token (15 min) + refresh token (1 day)
2. Use access token for API requests
3. Access token expires → send refresh token to /refresh/
4. Get a new access token → continue working
5. Refresh token expires → user must log in again

This way, even if an access token is stolen, the attacker
only has 15 minutes. The refresh token is only sent to
one endpoint, reducing exposure.

---
3. Role-Based Access Control with DRF Permission Classes

DRF permission classes are Python classes with one or two
methods:

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        """Runs on EVERY request to this view."""
        return request.user.role == 'STUDENT'

You apply them to a view:
class SubmissionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsStudent]

DRF checks permissions in order. Both IsAuthenticated
AND IsStudent must return True. If either returns
False, the request gets 403.

For views that need different permissions for different
HTTP methods (e.g., anyone can GET but only Instructors
can POST):

def get_permissions(self):
    if self.request.method == 'POST':
        return [IsAuthenticated(), IsInstructor()]
    return [IsAuthenticated()]

The queryset also plays a role. Even if a Student passes
the permission check for GET, they should only see THEIR
data:

def get_queryset(self):
    user = self.request.user
    if user.role == 'STUDENT':
        return Assignment.objects.filter(
            submissions__student=user
        )

This is defense in depth: permissions gate access,
querysets filter data. Both must be correct.

---
4. Row-Level vs Role-Level Permissions: The Observer Example

Role-level permission checks one thing: what type of
user are you?

class IsObserver(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'OBSERVER'

This lets ANY Observer access the endpoint. But our system
has a rule: each Observer is linked to ONE specific student
and must only see that student's data.

If Observer A is linked to Student A, and Observer B is
linked to Student B, a role-only check would let Observer A
see Student B's data. That is a security vulnerability.

Row-level permission checks the specific data being
accessed:

class IsLinkedObserver(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'OBSERVER'

    def has_object_permission(self, request, view, obj):
        return request.user.linked_student == obj.student

Now Observer A can only access objects where the student
matches their linked_student. Observer B's student's data
returns 403.

When does has_object_permission run?
- NOT on list views (GET /assignments/) — Django does not
call it for every object in a list. Instead, you filter
the queryset.
- YES on detail views (GET /submissions/{id}/feedback/) —
Django retrieves the object, then calls
has_object_permission.

For list views, the queryset filter serves the same
purpose:

if user.role == 'OBSERVER':
    return qs.filter(
        submission__student=user.linked_student
    )

Both approaches enforce the same rule: an Observer only
sees their linked student's data. The queryset handles
lists, has_object_permission handles individual objects.