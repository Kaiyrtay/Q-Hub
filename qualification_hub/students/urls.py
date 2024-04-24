from django.urls import path
from .views import StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView

app_name = "students"

urlpatterns = [
    path("", StudentListView.as_view(), name="list"),
    path("<int:pk>/", StudentDetailView.as_view(), name="detail"),
    path("create/", StudentCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", StudentUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", StudentDeleteView.as_view(), name="delete"),
]
