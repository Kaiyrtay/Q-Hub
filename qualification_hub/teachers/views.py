from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Teacher
from .forms import UserTeacherForm
from departments.models import Department
from collections import defaultdict
from core.mixins import ManagerGroupRequiredMixin, ManagerOrOwnerRequiredMixin

# List View for displaying all teachers


class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Group teachers by their department
        grouped_teachers = defaultdict(list)
        for teacher in Teacher.objects.all():
            if teacher.department:  # Ensure department is not None
                grouped_teachers[teacher.department.id].append(teacher)

        # Convert the defaultdict to a list of tuples for template iteration
        context['teachers_grouped'] = [
            (Department.objects.get(id=dept_id), teachers)
            for dept_id, teachers in grouped_teachers.items()
        ]
        context['without_departments_teachers'] = Teacher.objects.filter(
            department=None)
        return context


# Detail View for a specific teacher
class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'teachers/teacher_detail.html'
    context_object_name = 'teacher'


# Form View for creating a new teacher
class TeacherCreateView(ManagerGroupRequiredMixin, CreateView):
    model = Teacher
    form_class = UserTeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teachers:list')

    def form_valid(self, form):
        # Create the User and link it to the Teacher
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data.get(
                'password', '')  # Add password support
        )
        form.instance.user = user  # Link the newly created user to the teacher
        return super().form_valid(form)


# Form View for updating an existing teacher
class TeacherUpdateView(ManagerOrOwnerRequiredMixin, UpdateView):
    model = Teacher
    form_class = UserTeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teachers:list')

    def get_object(self):
        return super().get_object()

    def form_valid(self, form):
        teacher = self.get_object()  # Get the existing teacher
        user = teacher.user  # Get the related User

        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']

        if form.cleaned_data.get("password"):
            # Update password if provided
            user.set_password(form.cleaned_data["password"])

        user.save()  # Save changes to the user

        return super().form_valid(form)


# Delete View for deleting a teacher
class TeacherDeleteView(ManagerOrOwnerRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'teachers/teacher_confirm_delete.html'
    success_url = reverse_lazy('teachers:list')

    def get_object(self):
        return super().get_object()

    def post(self, request, *args, **kwargs):
        teacher = self.get_object()  # Get the teacher instance
        response = super().post(request, *args, **kwargs)  # Perform the delete action
        teacher.user.delete()  # Delete the associated user account
        return response
