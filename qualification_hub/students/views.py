"""
Student Views for Managing Students in Django

This file contains views for listing, creating, updating, and deleting `Student`
instances, as well as displaying details of individual students.

Key Classes:
- `StudentListView`: Lists all students with pagination and grouping by department.
- `StudentDetailView`: Displays detailed information about a specific student.
- `StudentCreateView`: Allows creation of new student entries, along with associated user data.
- `StudentUpdateView`: Updates existing student data, including user details.
- `StudentDeleteView`: Handles deletion of student records and associated user data.

Important Features:
- The `StudentListView` groups students by department and provides pagination.
- The `StudentCreateView` creates a new `User` when adding a student.
- The `StudentUpdateView` supports updating user-related fields like username, email, and password.
- The `StudentDeleteView` removes the associated user upon student deletion.

Dependencies:
- Relies on the `Student` model from the current module.
- Uses `User` from `django.contrib.auth.models` for user-related operations.
- Requires the `Department` model to associate students with departments.
- Uses `ManagerGroupRequiredMixin` and `ManagerOrOwnerRequiredMixin` for permission control.

Author: Kaiyrtay
"""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from collections import defaultdict
from .models import Student
from .forms import UserStudentForm
from departments.models import Department
from core.mixins import ManagerGroupRequiredMixin, ManagerOrOwnerRequiredMixin
from django.core.paginator import Paginator


class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        grouped_students = defaultdict(list)

        for student in Student.objects.all():
            if student.department:
                grouped_students[student.department.id].append(student)

        students_grouped = []
        for dept_id, students in grouped_students.items():
            paginator = Paginator(students, 5)  # Paginate by 5
            page_number = self.request.GET.get(f'page_dept_{dept_id}')
            students_paginated = paginator.get_page(page_number)
            department = Department.objects.get(id=dept_id)
            students_grouped.append((department, students_paginated))

        without_departments = Student.objects.filter(department=None)
        paginator_without_departments = Paginator(
            without_departments, 5)  # Paginate by 5
        page_number = self.request.GET.get('page_without_dept')
        without_departments_paginated = paginator_without_departments.get_page(
            page_number)

        context['students_grouped'] = students_grouped
        context['without_departments_paginated'] = without_departments_paginated

        return context


class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'


class StudentCreateView(ManagerGroupRequiredMixin, CreateView):
    model = Student
    form_class = UserStudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data.get('password', '')
        )
        form.instance.user = user
        return super().form_valid(form)


class StudentUpdateView(ManagerOrOwnerRequiredMixin, UpdateView):
    model = Student
    form_class = UserStudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')

    def get_object(self):
        return super().get_object()

    def form_valid(self, form):
        student = self.get_object()
        user = student.user

        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']

        if form.cleaned_data.get("password"):
            user.set_password(form.cleaned_data["password"])

        user.save()

        return super().form_valid(form)


class StudentDeleteView(ManagerOrOwnerRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:list')

    def get_object(self):
        return super().get_object()

    def post(self, request, *args, **kwargs):
        student = self.get_object()
        response = super().post(request, *args, **kwargs)
        student.user.delete()
        return response
