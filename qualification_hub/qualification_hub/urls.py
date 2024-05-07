"""
URL Configuration for Django Project

This file contains the URL patterns for the Django project. It includes routing
for various applications, password reset views, and a home page. The `path` and 
`re_path` functions are used to define the URL patterns, while views from the 
Django framework and custom applications are included as needed.

Key Features:
- **Admin URL**: The Django admin site is accessible via 'admin/'.
- **App-Specific URLs**: Applications such as 'faculties', 'departments', 'managers', 
  'teachers', 'students', 'certificates', and 'core' each have their own URL configurations.
- **Password Reset URLs**: Provides the necessary views for password reset, including 
  password reset form, done, confirm, and complete.
- **Home Page**: The root URL ('') maps to a template-based home page.

Notes:
- The password reset URLs use both `path` and `re_path` to handle complex patterns, 
  especially with `re_path` for the confirmation link with unique tokens.
- Each included app URL configuration should define its own `urlpatterns` to be 
  included in the main project.

Author: Kaiyrtay
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('faculties/', include('faculties.urls')),
    path('departments/', include('departments.urls')),
    path('managers/', include('managers.urls')),
    path('teachers/', include('teachers.urls')),
    path('students/', include('students.urls')),
    path('certificates/', include('certificates.urls')),
    path('core/', include('core.urls')),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    re_path(
        r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('copy-right/', TemplateView.as_view(template_name='copy-right.html'),
         name='copy-right'),
    path('rosetta/', include('rosetta.urls')),
]
# Translated
urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
