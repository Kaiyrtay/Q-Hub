from django.contrib import admin
from .models import Faculty


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "dean", "created_at", "department_count")
    search_fields = ("name", "dean__username")
    list_filter = ("created_at",)
    ordering = ("name",)

    def department_count(self, obj):
        return obj.departments.count()
    department_count.short_description = 'Number of Departments'
