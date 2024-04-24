from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
]
