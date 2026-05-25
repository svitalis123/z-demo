from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = ['email', 'role', 'is_staff']
    list_filter = ['role']
    fieldsets = BaseAdmin.fieldsets + (
        ('Role', {'fields': ('role', 'linked_student')}),
    )