"""
UserStudentForm for Managing Student Information

This file defines the `UserStudentForm` class, used for creating and updating
`Student` instances. It also handles related user information, including 
usernames, emails, passwords, and additional student-related fields like 
department, role, enrollment date, graduation date, and major.

Key Features:
- `clean_email()`: Validates email uniqueness to avoid conflicts.
- `clean_username()`: Ensures unique usernames for user creation or update.
- `save()`: Manages saving of both `User` and `Student` instances, updating 
  user-related information based on form data.

Important Methods:
- `__init__()`: Initializes the form with data for existing instances, allowing 
  pre-population of form fields when updating existing students.
- `save()`: Handles saving operations, including creating or updating the `User` 
  and `Student`.

Dependencies:
- Relies on the `Student` model to create or update student records.
- Uses `User` from `django.contrib.auth.models` to manage user-related operations.
- Interacts with `Department` from `departments.models` to set a student's department.

Author: Kaiyrtay
"""

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit
from crispy_forms.bootstrap import Tab, TabHolder
from .models import Student
from departments.models import Department


class UserStudentForm(forms.ModelForm):
    # Form fields with enhanced styling and default values
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        required=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text="Leave blank to retain the existing password"
    )
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}))
    middle_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Middle Name'}), required=False)
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Phone Number'}), required=False)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), required=False)
    role = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Role'}), initial="Student")
    enrollment_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'datepicker', 'placeholder': 'Enrollment Date'}
        )
    )
    graduation_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'datepicker', 'placeholder': 'Graduation Date'}
        )
    )
    major = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Major'}), required=False)

    class Meta:
        model = Student
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'middle_name', 'phone_number', 'department', 'role',
            'enrollment_date', 'graduation_date', 'major'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Field('username', css_class='form-control',
                      placeholder='Username'),
                Field('email', css_class='form-control', placeholder='Email'),
                Field('password', css_class='form-control',
                      placeholder='Password'),
                Field('first_name', css_class='form-control',
                      placeholder='First Name'),
                Field('last_name', css_class='form-control',
                      placeholder='Last Name'),
                Field('middle_name', css_class='form-control',
                      placeholder='Middle Name'),
                Field('phone_number', css_class='form-control',
                      placeholder='Phone Number'),
                # Dropdown for departments
                Field('department', css_class='form-select'),
                Field('role', css_class='form-control'),
                Field('enrollment_date', css_class='datepicker',
                      placeholder='Enrollment Date'),
                Field('graduation_date', css_class='datepicker',
                      placeholder='Graduation Date'),
                Field('major', css_class='form-control', placeholder='Major'),
                Submit('submit', 'Save Changes', css_class='btn btn-primary')
            )
        )

        student = kwargs.get('instance', None)
        initial = kwargs.get('initial', {})

        if student and hasattr(student, 'user'):
            user = student.user
            initial.update({
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'middle_name': student.middle_name,
                'phone_number': student.phone_number,
                'department': student.department,
                'role': student.role,
                'enrollment_date': student.enrollment_date,
                'graduation_date': student.graduation_date,
                'major': student.major,
            })

        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    # Validate unique email addresses
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        user_pk = self.instance.user.pk if self.instance and hasattr(
            self.instance, 'user'
        ) else None
        if User.objects.filter(email=email).exclude(pk=user_pk).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    # Validate unique usernames
    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        user_pk = self.instance.user.pk if self.instance and hasattr(
            self.instance, 'user'
        ) else None
        if User.objects.filter(username=username).exclude(pk=user_pk).exists():
            raise ValidationError("A user with this username already exists.")
        return username

    # Save the Student and User instances
    def save(self, commit=True):
        student = super().save(commit=False)

        user = student.user if hasattr(student, 'user') else User()

        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]

        password = self.cleaned_data.get("password", None)
        if password:
            user.set_password(password)

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()  # Save the User
            student.user = user  # Link User to Student
            student.save()  # Save the Student

        return student
