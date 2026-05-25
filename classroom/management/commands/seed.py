from django.core.management.base import BaseCommand
from accounts.models import User
from classroom.models import Assignment, Submission, Feedback


class Command(BaseCommand):
    help = 'Populate database with demo data.'

    def handle(self, *args, **options):
        if User.objects.filter(
            email='instructor@demo.dev'
        ).exists():
            self.stdout.write(self.style.WARNING(
                'Demo data already exists. Skipping.'
            ))
            return

        instructor = User.objects.create_user(
            username='instructor',
            email='instructor@demo.dev',
            password='Demo@1234',
            role=User.Role.INSTRUCTOR,
        )
        student = User.objects.create_user(
            username='student',
            email='student@demo.dev',
            password='Demo@1234',
            role=User.Role.STUDENT,
        )
        User.objects.create_user(
            username='observer',
            email='observer@demo.dev',
            password='Demo@1234',
            role=User.Role.OBSERVER,
            linked_student=student,
        )

        a1 = Assignment.objects.create(
            title='Build a REST API',
            description='Create a CRUD API using DRF.',
            instructor=instructor,
        )
        a2 = Assignment.objects.create(
            title='Add JWT Authentication',
            description='Secure your API with JWT tokens.',
            instructor=instructor,
        )

        s1 = Submission.objects.create(
            assignment=a1,
            student=student,
            content='Implemented ViewSet with CRUD actions.',
        )
        s2 = Submission.objects.create(
            assignment=a2,
            student=student,
            content='Added SimpleJWT login and refresh.',
        )
        Submission.objects.create(
            assignment=a1,
            student=student,
            content='Revised: added pagination and filters.',
        )

        Feedback.objects.create(
            submission=s1,
            instructor=instructor,
            comment='Good start! Add error handling.',
        )
        Feedback.objects.create(
            submission=s2,
            instructor=instructor,
            comment='Token refresh works. Add blacklisting.',
        )

        self.stdout.write(self.style.SUCCESS(
            'Demo data seeded successfully.'
        ))
