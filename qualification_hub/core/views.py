from django.urls import reverse
from students.models import Student
from teachers.models import Teacher
from .forms import UserRegistrationForm
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username_or_email).first(
        ) or User.objects.filter(email=username_or_email).first()

        if user:
            user = authenticate(username=user.username, password=password)

            if user:
                login(request, user)
                return redirect('/')

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


class UserRegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        role = form.cleaned_data['role']
        user.save()

        if role == 'teacher':
            teacher = Teacher.objects.create(
                user=user) 
            detail_url = reverse('teachers:update', kwargs={'pk': teacher.id})
        elif role == 'student':
            student = Student.objects.create(
                user=user) 
            detail_url = reverse('students:update', kwargs={'pk': student.id})

        login(self.request, user) 
        return redirect(detail_url) 
