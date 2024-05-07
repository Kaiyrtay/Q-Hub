"""
UserManagerForm for Managing Manager Data

This file contains the `UserManagerForm` class, which handles form-based 
operations for creating and updating `Manager` instances. It includes 
user-related fields like username, email, first name, and last name, as 
well as manager-specific fields like department, role, and appointed date.

Key Features:
- The `clean_email()` method validates that the email is unique to avoid 
  conflicts with existing users.
- The `clean_username()` method ensures unique usernames for user creation 
  or updates.
- The `save()` method manages saving both `User` and `Manager` instances, 
  including password handling if provided.

Dependencies:
- Relies on `Manager` from the current module to create or update manager 
  records.
- Uses `User` from `django.contrib.auth.models` for user-related operations.
- Interacts with `Department` from `departments.models` to establish the 
  department association.

Author: Kaiyrtay
"""

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit
from crispy_forms.bootstrap import Tab, TabHolder
from .models import Manager
from departments.models import Department


class UserManagerForm(forms.ModelForm):
    # Form fields
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text="Leave blank to retain the existing password"
    )
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}), required=False)
    middle_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Middle Name'}), required=False)
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        required=False
    )
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    role = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Role'}), initial="Department Manager")
    appointed_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'datepicker', 'placeholder': 'Appointed Date'}
        )
    )
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Manager
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'middle_name', 'phone_number', 'department', 'role', 'appointed_date', 'avatar'
        ]

    # Initialize the form with existing data
    def __init__(self, *args, **kwargs):
        manager = kwargs.get('instance', None)
        initial = kwargs.get('initial', {})

        if manager and hasattr(manager, 'user'):
            user = manager.user
            initial.update({
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'middle_name': manager.middle_name,
                'phone_number': manager.phone_number,
                'department': manager.department,
                'role': manager.role,
                'appointed_date': manager.appointed_date,
            })
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('username', css_class='form-control'),
                Field('email', css_class='form-control'),
                Field('password', css_class='form-control'),
                Field('first_name', css_class='form-control'),
                Field('last_name', css_class='form-control'),
                Field('middle_name', css_class='form-control'),
                Field('phone_number', css_class='form-control'),
                Field('department', css_class='form-select'),  # Dropdown
                Field('role', css_class='form-control'),
                Field('appointed_date', css_class='datepicker',
                      placeholder='Appointed Date'),
                Field('avatar', css_class='form-control'),
                Submit('submit', 'Save Changes', css_class='btn btn-primary')
            )
        )

    # Validate email uniqueness

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        user_pk = self.instance.user.pk if hasattr(
            self.instance, 'user') else None

        if User.objects.filter(email=email).exclude(pk=user_pk).exists():
            raise ValidationError("A user with this email already exists.")

        return email

    # Validate username uniqueness
    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        user_pk = self.instance.user.pk if hasattr(
            self.instance, 'user') else None

        if User.objects.filter(username=username).exclude(pk=user_pk).exists():
            raise ValidationError("A user with this username already exists.")

        return username

    # Save the Manager and User instances
    def save(self, commit=True):
        manager = super().save(commit=False)
        user = manager.user if hasattr(manager, 'user') else User()

        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]

        # If password provided, set it
        password = self.cleaned_data.get("password", None)
        if password:
            user.set_password(password)

        user.first_name = self.cleaned_data["first_name"]
        user.last_name

        if commit:
            user.save()  # Save the User
            manager.user = user  # Link the User with the Manager
            manager.save()  # Save the Manager

        return manager
