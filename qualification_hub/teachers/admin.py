from django.contrib import admin
from .models import Teacher


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'role',
                    'hire_date', 'certificate_count')

    search_fields = ('full_name', 'role', 'department__name')

    list_filter = ('department', 'role', 'hire_date')

    fieldsets = (
        (None, {
            'fields': ('user', 'department', 'role', 'hire_date', 'phone_number', 'contact_email'),
        }),
    )

    def full_name(self, obj):
        return obj.full_name()
    full_name.short_description = 'Full Name'

    def certificate_count(self, obj):
        return obj.certificates.count()
    certificate_count.short_description = 'Number of Certificates'


admin.site.register(Teacher, TeacherAdmin)
