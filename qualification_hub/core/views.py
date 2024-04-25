from students.models import Student
from teachers.models import Teacher
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

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


class StudentRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        student = Student(user=user)
        student.save()
        return super().form_valid(form)


class TeacherRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        teacher = Teacher(user=user)
        teacher.save()
        return super().form_valid(form)
