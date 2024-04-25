from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "core"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', TemplateView.as_view(template_name='temp.html'), name='register'),
    path('register-student/', views.StudentRegisterView.as_view(),
         name='register-student'),
    path('register-teacher/', views.TeacherRegisterView.as_view(),
         name='register-teacher'),
]
