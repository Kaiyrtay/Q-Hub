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
        # Later
        context["teacher_count"] = department.teachers.count()
        context["manager_count"] = department.managers.count()
        # context["student_count"] = department.students.count()
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
