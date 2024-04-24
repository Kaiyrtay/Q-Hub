from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from collections import defaultdict
from .models import Student
from .forms import UserStudentForm
from departments.models import Department


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

        context['students_grouped'] = [
            (Department.objects.get(id=dept_id), students)
            for dept_id, students in grouped_students.items()
        ]
        context['without_departments_students'] = Student.objects.filter(
            department=None)
        return context


class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'


class StudentCreateView(CreateView):
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


class StudentUpdateView(UpdateView):
    model = Student
    form_class = UserStudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')

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


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:list')

    def post(self, request, *args, **kwargs):
        student = self.get_object()
        response = super().post(request, *args, **kwargs)
        student.user.delete()
        return response
