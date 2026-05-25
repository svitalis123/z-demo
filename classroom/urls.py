from django.urls import path
from .views import (
    AssignmentListCreateView,
    SubmissionCreateView,
    FeedbackDetailView,
)

urlpatterns = [
    path(
        'assignments/',
        AssignmentListCreateView.as_view(),
        name='assignment-list',
    ),
    path(
        'submissions/',
        SubmissionCreateView.as_view(),
        name='submission-create',
    ),
    path(
        'submissions/<uuid:submission_id>/feedback/',
        FeedbackDetailView.as_view(),
        name='feedback-detail',
    ),
]