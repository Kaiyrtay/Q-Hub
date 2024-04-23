from django.contrib import admin
from .models import Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('faculty','name', 'manager_count',) #'teacher_count', 'student_count')
    list_filter = ('faculty','name',)
    search_fields = ('faculty', 'name',)

    
    def manager_count(self, obj):
        return obj.managers.count()
    manager_count.short_description = 'Number of Managers'

    # def teacher_count(self, obj):
    #     return obj.managers.count()
    # teacher_count.short_description = 'Number of Teachers'

    # def student_count(self, obj):
    #     return obj.managers.count()
    # student_count.short_description = 'Number of Students'


admin.site.register(Department, DepartmentAdmin)
