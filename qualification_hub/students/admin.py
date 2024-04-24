from django.contrib import admin
from .models import Student

# Registering the Student model in the admin interface


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('full_name', 'role', 'department', 'enrollment_date')
    search_fields = ('user__username', 'user__first_name',
                     'user__last_name')  # Allow search by these fields
    # Add filters for these fields
    list_filter = ('department', 'enrollment_date')
