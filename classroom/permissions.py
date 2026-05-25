from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'INSTRUCTOR'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'STUDENT'


# ---------------------------------------------------------------
# TEACHING COMMENT — for the learner reading this code:
#
# Why do we need has_object_permission AND has_permission?
#
# has_permission() runs BEFORE Django fetches any object from
# the database. It answers: "Is this TYPE of user allowed to
# even attempt this action?"
#   Example: only Students may POST submissions.
#
# has_object_permission() runs AFTER an object is retrieved.
# It answers: "Is this specific user allowed to touch THIS
# specific row?"
#   Example: Observer can only see THEIR linked student.
#
# If you only use has_permission(), an Observer could see
# every student's submissions — not just the one they are
# linked to. That is a real security bug. Row-level checks
# close that gap.
# ---------------------------------------------------------------
class IsLinkedObserver(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'OBSERVER'

    def has_object_permission(self, request, view, obj):
        student = getattr(obj, 'student', None)
        if student is None:
            return False
        return request.user.linked_student == student
