from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Manager
from departments.models import Department


class UserManagerForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    middle_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    role = forms.CharField(initial="Department Manager")
    appointed_date = forms.DateField(required=False)
    password = forms.CharField(
        required=False, widget=forms.PasswordInput(), help_text="Leave blank to retain the existing password"
    )

    class Meta:
        model = Manager
        fields = [
            'username', 'email', 'first_name', 'last_name', 'middle_name',
            'phone_number', 'department', 'role', 'appointed_date', 'password'
        ]

    def __init__(self, *args, **kwargs):
        manager = kwargs.get('instance', None)
        initial = kwargs.get('initial', {})

        if manager:
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
        manager = super().save(commit=False)
        user = manager.user if hasattr(manager, 'user') else User()

        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]

        # Update the password if provided
        password = self.cleaned_data.get("password", None)
        if password:
            user.set_password(password)  # Hash the new password

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()  # Save the User instance
            manager.user = user  # Link the User with the Manager
            manager.save()  # Save the Manager instance

        return manager
