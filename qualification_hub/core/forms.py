"""
User Registration Form for Django Project

This file defines the `UserRegistrationForm` class, an extension of Django's 
`UserCreationForm`, designed to handle user registration with additional fields 
like first name, last name, email, and role (student or teacher). It also 
incorporates the `Crispy Forms` library to customize the form layout and 
presentation.

Key Features:
- Supports user registration with roles, allowing the user to choose between 
  "Student" and "Teacher".
- Utilizes `Crispy Forms` for a flexible and customizable form layout, 
  with improved styling and structure.
- Inherits from `UserCreationForm`, providing built-in validation for 
  common user registration requirements (like password confirmation).

Dependencies:
- Inherits from `UserCreationForm` from `django.contrib.auth.forms`.
- Relies on `User` from `django.contrib.auth.models` for user-related operations.
- Utilizes `Crispy Forms` for custom form layouts and styling, providing a 
  consistent and enhanced user interface.

Custom Layout:
- The `FormHelper` from `Crispy Forms` is used to define a custom layout with 
  Bootstrap styling.
- The layout includes form fields for username, first name, last name, email, 
  password1, password2, and role.
- The form uses radio buttons for the role selection and a submit button styled 
  with Bootstrap.

Author: Kaiyrtay
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML


class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="Register as",
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Field('username', css_class='form-control',
                      placeholder='Username'),
                Field('first_name', css_class='form-control',
                      placeholder='First Name'),
                Field('last_name', css_class='form-control',
                      placeholder='Last Name'),
                Field('email', css_class='form-control', placeholder='Email'),
                Field('password1', css_class='form-control',
                      placeholder='Password'),
                Field('password2', css_class='form-control',
                      placeholder='Confirm Password'),
                Field('role', css_class='form-check-input'),
                css_class='mb-3'  # Margin-bottom for spacing
            ),
            Submit('submit', 'Register', css_class='btn btn-primary btn-block'),
        )
