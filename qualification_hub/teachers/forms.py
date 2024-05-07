"""
UserTeacherForm for Managing Teacher Information

This file contains the `UserTeacherForm` class, which is used to create and update 
`Teacher` instances. It also handles the associated `User` object for teacher-related 
user management, including username, email, and password validation. 

Key Features:
- Validates unique usernames and emails to avoid conflicts.
- Supports updating existing teacher information and creating new entries.
- Includes user information like first name, last name, middle name, phone number, 
  department, role, hire date, subject taught, and room number.

Important Methods:
- `clean_email()`: Ensures email uniqueness during form validation.
- `clean_username()`: Ensures username uniqueness during form validation.
- `save()`: Handles saving the associated `User` and `Teacher` instances.

Dependencies:
- Requires the `Teacher` model from the current module.
- Interacts with the `User` model from `django.contrib.auth.models`.
- Requires the `Department` model from `departments.models`.

Author: Kaiyrtay
"""

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit
from .models import Teacher
from departments.models import Department


class UserTeacherForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(required=False, widget=forms.PasswordInput(
    ), help_text="Leave blank to retain the existing password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    middle_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), required=False)
    role = forms.CharField(initial="Teacher")
    hire_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'datepicker', 'placeholder': 'Hire Date'})
    )
    subject_taught = forms.CharField(required=False)
    room_number = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Teacher
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'middle_name', 'phone_number', 'department', 'role',
            'hire_date', 'subject_taught', 'room_number', 'avatar'
        ]

    def __init__(self, *args, **kwargs):
        # Initialize form data for editing an existing teacher
        teacher = kwargs.get('instance', None)
        initial = kwargs.get('initial', {})

        if teacher and hasattr(teacher, 'user'):
            user = teacher.user
            initial.update({
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'middle_name': teacher.middle_name,
                'phone_number': teacher.phone_number,
                'department': teacher.department,
                'role': teacher.role,
                'hire_date': teacher.hire_date,
                'subject_taught': teacher.subject_taught,
                'room_number': teacher.room_number,
            })

        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('username', css_class='form-control',
                      placeholder='Username'),
                Field('first_name', css_class='form-control',
                      placeholder='First Name'),
                Field('last_name', css_class='form-control',
                      placeholder='Last Name'),
                Field('middle_name', css_class='form-control',
                      placeholder='Middle Name'),
                Field('email', css_class='form-control', placeholder='Email'),
                Field('phone_number', css_class='form-control',
                      placeholder='Phone Number'),
                Field('department', css_class='form-select'),
                Field('role', css_class='form-control'),
                Field('hire_date', css_class='datepicker',
                      placeholder='Hire Date'),  # Trigger Flatpickr
                Field('subject_taught', css_class='form-control',
                      placeholder='Subject Taught'),
                Field('room_number', css_class='form-control',
                      placeholder='Room Number'),
                Field('avatar', css_class='form-control'),
                Submit('submit', 'Save Changes', css_class='btn btn-primary'),
            )
        )

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        user_pk = self.instance.user.pk if self.instance and hasattr(
            self.instance, 'user') else None

        if User.objects.filter(email=email).exclude(pk=user_pk).exists():
            raise ValidationError("A user with this email already exists.")

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        user_pk = self.instance.user.pk if self.instance and hasattr(
            self.instance, 'user') else None

        if User.objects.filter(username=username).exclude(pk=user_pk).exists():
            raise ValidationError("A user with this username already exists.")

        return username

    def save(self, commit=True):
        teacher = super().save(commit=False)

        # Handle User object
        user = teacher.user if hasattr(teacher, 'user') else User()

        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]

        # Update the password if provided
        password = self.cleaned_data.get("password", None)
        if password:
            user.set_password(password)

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()  # Save the user
            teacher.user = user  # Assign user to teacher
            teacher.save()  # Save the teacher

        return teacher
