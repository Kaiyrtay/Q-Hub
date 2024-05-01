"""
Department Views for Managing Departments in Django

This file contains views for listing, creating, updating, and deleting 
`Department` instances, as well as displaying detailed information about 
individual departments. It uses Django's generic class-based views for 
common operations like `ListView`, `DetailView`, `CreateView`, `UpdateView`, 
and `DeleteView`.

Key Classes:
- `DepartmentListView`: Lists all departments.
- `DepartmentDetailView`: Displays detailed information about a specific department.
- `DepartmentCreateView`: Allows creation of new departments. Requires staff-level permissions.
- `DepartmentUpdateView`: Updates existing department data. Requires staff-level permissions.
- `DepartmentDeleteView`: Handles the deletion of department records. Requires staff-level permissions.

Key Features:
- The `DepartmentDetailView` provides additional context, such as counts of related 
  teachers, managers, and students.
- The `DepartmentCreateView` and `DepartmentUpdateView` allow staff to create and 
  update departments, including setting the faculty and head.
- The `DepartmentDeleteView` requires staff-level permissions, ensuring that only 
  authorized users can delete departments.

Dependencies:
- Uses the `Department` model from the current module.
- Relies on `StaffRequiredMixin` to enforce staff-level permissions for create, 
  update, and delete operations.
- Interacts with the `Faculty` model, which establishes a relationship between 
  departments and faculties.

Author: Kaiyrtay
"""

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Department
from core.mixins import StaffRequiredMixin


class DepartmentListView(ListView):
    model = Department
    template_name = "departments/department_list.html"
    context_object_name = "departments"


class DepartmentDetailView(DetailView):
    model = Department
    template_name = "departments/department_detail.html"
    context_object_name = "department"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        context["teacher_count"] = department.teachers.count()
        context["manager_count"] = department.managers.count()
        context["student_count"] = department.students.count()
        return context


class DepartmentCreateView(StaffRequiredMixin, CreateView):
    model = Department
    fields = ['faculty', 'name', 'head']
    template_name = "departments/department_form.html"
    success_url = reverse_lazy("departments:list")


class DepartmentUpdateView(StaffRequiredMixin, UpdateView):
    model = Department
    fields = ['faculty', 'name', 'head']
    template_name = "departments/department_form.html"
    success_url = reverse_lazy("departments:list")


class DepartmentDeleteView(StaffRequiredMixin, DeleteView):
    model = Department
    template_name = "departments/department_confirm_delete.html"
    success_url = reverse_lazy("departments:list")
