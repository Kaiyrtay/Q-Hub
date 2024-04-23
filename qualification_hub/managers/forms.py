from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Manager
from departments.models import Department


class UserManagerForm(forms.ModelForm):
    # Extend fields for the user and manager
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    middle_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    role = forms.CharField(initial="Department Manager")
    appointed_date = forms.DateField(required=False)

    class Meta:
        model = Manager
        fields = ['username', 'email', 'last_name', 'first_name',
                  'middle_name', 'phone_number', 'department', 'role', 'appointed_date']

    def __init__(self, *args, **kwargs):
        # Ensure existing data is used when updating
        manager = kwargs.get('instance', None)
        if manager:
            user = manager.user
            kwargs['initial'] = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'middle_name': manager.middle_name,
                'phone_number': manager.phone_number,
                'department': manager.department,
                'role': manager.role,
                'appointed_date': manager.appointed_date,
            }
        super(UserManagerForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        # Avoid accessing `self.instance.user.pk` if it doesn't exist
        if self.instance.pk:  # Only if instance exists
            user_pk = self.instance.user.pk
        else:
            user_pk = None

        if User.objects.filter(email=email).exclude(pk=user_pk).exists():
            raise ValidationError("A user with this email already exists.")

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        if self.instance.pk:  # Only if instance exists
            user_pk = self.instance.user.pk
        else:
            user_pk = None

        if User.objects.filter(username=username).exclude(pk=user_pk).exists():
            raise ValidationError("A user with this username already exists.")

        return username
