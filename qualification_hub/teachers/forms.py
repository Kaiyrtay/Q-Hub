from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Teacher
from departments.models import Department


class UserTeacherForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    middle_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    role = forms.CharField(initial="Teacher")
    hire_date = forms.DateField(required=False)
    subject_taught = forms.CharField(required=False)
    room_number = forms.CharField(required=False)

    class Meta:
        model = Teacher
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'middle_name', 'phone_number', 'department', 'role',
            'hire_date', 'subject_taught', 'room_number'
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

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        user_pk = self.instance.user.pk if self.instance and hasattr(self.instance, 'user') else None

        if User.objects.filter(email=email).exclude(pk=user_pk).exists():
            raise ValidationError("A user with this email already exists.")

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        user_pk = self.instance.user.pk if self.instance and hasattr(self.instance, 'user') else None

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
