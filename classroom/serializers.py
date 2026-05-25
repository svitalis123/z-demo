from rest_framework import serializers
from .models import Assignment, Submission, Feedback


class AssignmentSerializer(serializers.ModelSerializer):
    instructor_email = serializers.EmailField(
        source='instructor.email', read_only=True
    )

    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description',
            'instructor_email',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubmissionSerializer(serializers.ModelSerializer):
    student_email = serializers.EmailField(
        source='student.email', read_only=True
    )

    class Meta:
        model = Submission
        fields = [
            'id', 'assignment', 'student_email',
            'content', 'submitted_at',
        ]
        read_only_fields = ['id', 'submitted_at']


class FeedbackSerializer(serializers.ModelSerializer):
    instructor_email = serializers.EmailField(
        source='instructor.email', read_only=True
    )

    class Meta:
        model = Feedback
        fields = [
            'id', 'submission', 'instructor_email',
            'comment', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
