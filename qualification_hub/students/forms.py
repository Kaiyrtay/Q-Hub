from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Student
from departments.models import Department


class UserStudentForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    middle_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), required=False)
    role = forms.CharField(initial="Student")
    enrollment_date = forms.DateField(required=False)
    graduation_date = forms.DateField(required=False)
    major = forms.CharField(required=False)

    class Meta:
        model = Student
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'middle_name', 'phone_number', 'department', 'role',
            'enrollment_date', 'graduation_date', 'major'
        ]

    def __init__(self, *args, **kwargs):
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
        student = super().save(commit=False)

        # Handle User object
        user = student.user if hasattr(student, 'user') else User()

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
            student.user = user  # Assign user to student
            student.save()  # Save the student

        return student
