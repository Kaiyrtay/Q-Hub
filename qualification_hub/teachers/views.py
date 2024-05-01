"""
Teachers Management Views

This file contains views for managing the Teacher model in the Django application.
It includes the following:
- ListView for displaying a list of teachers, with grouping and pagination.
- DetailView for showing the details of a specific teacher.
- CreateView for adding new teachers.
- UpdateView for editing existing teachers.
- DeleteView for deleting a teacher and associated user account.

Dependencies:
- Django: This file uses Django's generic class-based views.
- Department Model: To relate teachers to their departments.
- Core Mixins: Custom mixins for role-based permissions (e.g., ManagerGroupRequiredMixin).
- UserTeacherForm: The form used for creating and updating teachers.

Author: Kaiyrtay

Notes:
- The ListView includes pagination for grouped teachers.
- The CreateView creates a new User and links it to a Teacher.
- The DeleteView deletes both the Teacher and associated User.
"""

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Teacher
from .forms import UserTeacherForm
from departments.models import Department
from collections import defaultdict
from core.mixins import ManagerGroupRequiredMixin, ManagerOrOwnerRequiredMixin
from django.core.paginator import Paginator


class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        grouped_teachers = defaultdict(list)
        for teacher in Teacher.objects.all():
            if teacher.department:
                grouped_teachers[teacher.department.id].append(teacher)

        teachers_grouped = []
        for dept_id, teachers in grouped_teachers.items():
            paginator = Paginator(teachers, 5)  # Paginate by 5
            page_number = self.request.GET.get(f'page_dept_{dept_id}')
            teachers_paginated = paginator.get_page(page_number)
            department = Department.objects.get(id=dept_id)
            teachers_grouped.append((department, teachers_paginated))

        without_departments = Teacher.objects.filter(department=None)
        paginator_without_departments = Paginator(
            without_departments, 5
        )
        page_number = self.request.GET.get('page_without_dept')
        without_departments_paginated = paginator_without_departments.get_page(
            page_number
        )

        context['teachers_grouped'] = teachers_grouped
        context['without_departments_paginated'] = without_departments_paginated

        return context


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'teachers/teacher_detail.html'
    context_object_name = 'teacher'


class TeacherCreateView(ManagerGroupRequiredMixin, CreateView):
    model = Teacher
    form_class = UserTeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teachers:list')

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data.get(
                'password', '')  # Add password support
        )
        form.instance.user = user
        return super().form_valid(form)


class TeacherUpdateView(ManagerOrOwnerRequiredMixin, UpdateView):
    model = Teacher
    form_class = UserTeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teachers:list')

    def get_object(self):
        return super().get_object()

    def form_valid(self, form):
        teacher = self.get_object()
        user = teacher.user

        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']

        if form.cleaned_data.get("password"):
            user.set_password(form.cleaned_data["password"])

        user.save()

        return super().form_valid(form)


class TeacherDeleteView(ManagerOrOwnerRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'teachers/teacher_confirm_delete.html'
    success_url = reverse_lazy('teachers:list')

    def get_object(self):
        return super().get_object()

    def post(self, request, *args, **kwargs):
        teacher = self.get_object()
        response = super().post(request, *args, **kwargs)
        teacher.user.delete()
        return response
