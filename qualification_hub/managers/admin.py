from django.contrib import admin
from .models import Manager


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'phone_number', 'contact_email')
    search_fields = ('user__first_name',  'middle_name', 'user__last_name',
                     'phone_number', 'contact_email')


admin.site.register(Manager, ManagerAdmin)
