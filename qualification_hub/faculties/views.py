"""
Faculty Views for Managing Faculty Data in Django

This file contains views for listing, creating, updating, and deleting `Faculty` 
instances, as well as displaying detailed information about specific faculties. 
The views use Django's generic class-based view system for common operations, 
including list, detail, create, update, and delete views.

Key Classes:
- `FacultyListView`: Lists all faculties in the system.
- `FacultyDetailView`: Displays detailed information about a specific faculty, 
  including related departments and department count.
- `FacultyCreateView`: Allows the creation of new faculties. Requires staff-level 
  permissions.
- `FacultyUpdateView`: Updates existing faculty data. Requires staff-level permissions.
- `FacultyDeleteView`: Handles the deletion of faculty records. Requires superuser-level 
  permissions.

Key Features:
- The `FacultyDetailView` provides additional context data, including related 
  departments and their count.
- The `FacultyCreateView` and `FacultyUpdateView` require staff-level permissions, 
  ensuring only authorized users can create or update faculties.
- The `FacultyDeleteView` requires superuser-level permissions, adding an extra layer 
  of security for deletion operations.

Dependencies:
- Uses the `Faculty` model from the current module.
- Relies on `User` from `django.contrib.auth.models` for user-related information.
- Utilizes mixins like `StaffRequiredMixin` and `SuperuserRequiredMixin` to enforce 
  access control and permissions.

Author: Kaiyrtay
"""

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Faculty
from core.mixins import StaffRequiredMixin, SuperuserRequiredMixin


class FacultyListView(ListView):
    model = Faculty
    template_name = "faculties/faculty_list.html"
    context_object_name = "faculties"


class FacultyDetailView(DetailView):
    model = Faculty
    template_name = "faculties/faculty_detail.html"
    context_object_name = "faculty"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculty = self.get_object()
        context['departments'] = faculty.departments.all()
        context['department_count'] = faculty.departments.count()

        return context


class FacultyCreateView(StaffRequiredMixin, CreateView):
    model = Faculty
    fields = ["name", "description", "dean",
              "website", "contact_email", "location"]
    template_name = "faculties/faculty_form.html"
    success_url = reverse_lazy("faculties:list")


class FacultyUpdateView(StaffRequiredMixin, UpdateView):
    model = Faculty
    fields = ["name", "description", "dean",
              "website", "contact_email", "location"]
    template_name = "faculties/faculty_form.html"
    success_url = reverse_lazy("faculties:list")


class FacultyDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Faculty
    template_name = "faculties/faculty_confirm_delete.html"
    success_url = reverse_lazy("faculties:list")
