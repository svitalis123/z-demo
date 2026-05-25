from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from .models import Assignment, Submission, Feedback
from .permissions import IsInstructor, IsStudent
from .serializers import (
    AssignmentSerializer,
    SubmissionSerializer,
    FeedbackSerializer,
)


class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsInstructor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.INSTRUCTOR:
            return Assignment.objects.filter(
                instructor=user
            ).select_related('instructor')
        if user.role == User.Role.STUDENT:
            return Assignment.objects.filter(
                submissions__student=user
            ).select_related('instructor').distinct()
        if user.role == User.Role.OBSERVER:
            if not user.linked_student:
                return Assignment.objects.none()
            return Assignment.objects.filter(
                submissions__student=user.linked_student
            ).select_related('instructor').distinct()
        return Assignment.objects.none()

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class FeedbackDetailView(generics.RetrieveAPIView):
    serializer_class = FeedbackSerializer
    lookup_field = 'submission_id'
    lookup_url_kwarg = 'submission_id'

    def get_queryset(self):
        user = self.request.user
        qs = Feedback.objects.select_related(
            'submission__student',
            'submission__assignment__instructor',
            'instructor',
        )
        if user.role == User.Role.INSTRUCTOR:
            return qs.filter(
                submission__assignment__instructor=user
            )
        if user.role == User.Role.STUDENT:
            return qs.filter(submission__student=user)
        if user.role == User.Role.OBSERVER:
            if not user.linked_student:
                return Feedback.objects.none()
            return qs.filter(
                submission__student=user.linked_student
            )
        return Feedback.objects.none()

