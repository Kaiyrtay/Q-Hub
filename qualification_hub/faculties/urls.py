from django.urls import path
from .views import FacultyListView, FacultyDetailView, FacultyCreateView, FacultyUpdateView, FacultyDeleteView

app_name = "faculties"

urlpatterns = [
    path("", FacultyListView.as_view(), name="list"),
    path("<int:pk>/", FacultyDetailView.as_view(), name="detail"),
    path("create/", FacultyCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", FacultyUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", FacultyDeleteView.as_view(), name="delete"),
]
