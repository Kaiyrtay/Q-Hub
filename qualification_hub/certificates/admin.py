from django.contrib import admin
from .models import Certificate


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_name', 'organization', 'certificate_number',
                    'expiration_date', 'date_earned', 'updated_at')
    search_fields = ('certificate_name', 'certificate_number', 'organization')
    list_filter = ('organization', 'expiration_date', 'date_earned')
    ordering = ('-created_at',)


admin.site.register(Certificate, CertificateAdmin)
