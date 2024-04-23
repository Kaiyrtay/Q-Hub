from django.contrib import admin
from .models import Teacher  # Assuming 'Teacher' is the model for your teachers


class TeacherAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('full_name', 'department', 'role', 'hire_date')

    # Fields to search for in the admin search box
    # Adjust according to your model fields
    search_fields = ('full_name', 'role', 'department__name')

    # Filters to apply in the admin list view
    # Customizable filters
    list_filter = ('department', 'role', 'hire_date')

    # Fieldsets for customizing the layout of the admin detail view (optional)
    fieldsets = (
        (None, {
            'fields': ('user', 'department', 'role', 'hire_date', 'phone_number', 'contact_email'),
        }),
    )

    # Function to return the full name (if not directly available in the model)
    def full_name(self, obj):
        return obj.full_name()

    # Short description for the full name function
    full_name.short_description = 'Full Name'


# Register the model with the admin site
admin.site.register(Teacher, TeacherAdmin)
