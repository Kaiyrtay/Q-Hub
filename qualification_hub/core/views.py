"""
Core Views and Search Logic for Django Project

This file contains various views and functions for handling user authentication 
(login, logout, and registration), as well as search logic across multiple models. 
It includes class-based views for creating and managing users and custom logic for 
searching through different entities like teachers, students, managers, certificates, 
and departments.

Key Functions:
- `login_view`: Handles user authentication with a login form, supporting login by 
  username or email.
- `logout_view`: Logs out the current user and redirects to the home page.
- `search_view`: Implements search logic to find users, certificates, and other 
  entities based on a query parameter.
- `get_user_or_none`: Helper function to get a `User` by username, returning `None` 
  if the user does not exist.

Key Classes:
- `RegisterView`: A `CreateView` for user registration, allowing creation of 
  users with different roles (e.g., student, teacher).
- `DepartmentListView`, `DepartmentDetailView`, etc.: Views for handling departments.

Dependencies:
- Uses `User` from `django.contrib.auth.models` for user-related operations.
- Requires models from different apps like `Teacher`, `Student`, `Manager`, 
  `Department`, `Faculty`, and `Certificate`.
- Employs Django's authentication system for login and logout operations.
- Utilizes Django's generic class-based views for list, detail, create, update, 
  and delete operations.

Author: Kaiyrtay
"""

from django.urls import reverse
from django.conf import settings
from django.utils import translation
from django.http import HttpResponseRedirect
from students.models import Student
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# local import
from .forms import UserRegistrationForm
# search logic import
from teachers.models import Teacher
from students.models import Student
from managers.models import Manager
from departments.models import Department
from faculties.models import Faculty
from certificates.models import Certificate
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


def get_user_or_none(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def user_redirect(username):
    user = get_user_or_none(username)
    if user:
        if hasattr(user, 'manager'):
            return redirect('managers:detail', pk=user.manager.pk)
        elif hasattr(user, 'teacher'):
            return redirect('teachers:detail', pk=user.teacher.pk)
        elif hasattr(user, 'student'):
            return redirect('students:detail', pk=user.student.pk)
        else:
            return {"message": "Access denied. You don't have the required permissions."}
    return {"message": f"User with username '{username}' not found."}


def get_certificate_by_number(number):
    try:
        certificate = Certificate.objects.get(certificate_number=number)
        return redirect('certificates:detail', pk=certificate.pk)
    except Certificate.DoesNotExist:
        return {"message": f"Certificate with number '{number}' not found."}


def get_organization_certificates(organization):
    query = Certificate.objects.filter(organization=organization)
    return query


def get_department_by_name(name):
    try:
        department = Department.objects.get(name=name)
        return redirect('departments:detail', pk=department.pk)
    except Department.DoesNotExist:
        return {"message": f"Department with name '{name}' not found."}


def get_certificates(text: str):
    certificates = Certificate.objects.filter(
        Q(certificate_name__icontains=text) |
        Q(description__icontains=text)
    )
    organization_certificates = get_organization_certificates(text)
    merged_certificates = certificates | organization_certificates
    return merged_certificates


def full_search(query):
    context = {}

    teachers = Teacher.objects.filter(
        Q(user__first_name__icontains=query) |
        Q(middle_name__icontains=query) |
        Q(user__last_name__icontains=query)
    )
    if teachers:
        context['teachers'] = teachers

    students = Student.objects.filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(middle_name__icontains=query)
    )
    if students:
        context['students'] = students

    managers = Manager.objects.filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(middle_name__icontains=query)
    )
    if managers:
        context['managers'] = managers

    certificates = get_certificates(query)
    if certificates:
        context['certificates'] = certificates

    departments = Department.objects.filter(
        name__icontains=query
    )
    if departments:
        context['departments'] = departments

    return context


def search_view(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        if not q:
            return render(request, 'core/search.html', {"message": f"No search term was specified."})
        if q:
            context = {}
            if q[0] == '@':
                result = user_redirect(q[1:])
                if isinstance(result, dict) and "message" in result:
                    return render(request, 'core/search.html', result)
                return result

            elif q[0] == '*':
                result = get_certificate_by_number(q[1:])
                if isinstance(result, dict) and "message" in result:
                    return render(request, 'core/search.html', result)
                return result

            elif q[0] == '#':
                context['organization_certificates'] = get_organization_certificates(
                    q[1:])
                context['organization'] = q[1:]
                return render(request, 'core/search.html', context)

            elif q[0] == '!':
                result = get_department_by_name(q[1:])
                if isinstance(result, dict) and "message" in result:
                    return render(request, 'core/search.html', result)
                return result
            elif q[0] == '$':
                result = get_certificates(q[1:])
                if result:
                    return render(request, 'core/search.html', {"certificates": result})
            else:
                result = full_search(q)
                if not result:
                    result = {
                        "message": f"No matches found for the search term: {q}."}

                return render(request, 'core/search.html', result)

        return render(request, 'core/search.html', {"message": f"No matches found for the search term: {q}."})

    return render(request, 'core/search.html')


def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username_or_email).first(
        ) or User.objects.filter(email=username_or_email).first()

        if user:
            user_authenticated = authenticate(
                username=user.username, password=password)

            if user_authenticated:
                login(request, user_authenticated)
                return redirect('/')
            else:
                messages.error(
                    request, "Incorrect password. Please try again.")

        else:
            messages.error(
                request, "User not found. Please check your username or email.")

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        if form.cleaned_data['role'] == 'student':
            student = Student(user=user)
            student.save()
        elif form.cleaned_data['role'] == 'teacher':
            teacher = Teacher(user=user)
            teacher.save()

        return super().form_valid(form)


def set_language(request):
    if request.method == 'POST':
        lang_code = request.POST.get('language')
        if lang_code in dict(settings.LANGUAGES).keys():
            translation.activate(lang_code)
            request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseRedirect(reverse('home'))
