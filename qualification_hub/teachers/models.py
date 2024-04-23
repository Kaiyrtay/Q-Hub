from django.contrib.auth.models import User
from django.db import models
from departments.models import Department


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    role = models.CharField(max_length=100, default="Teacher")
    hire_date = models.DateField(null=True, blank=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    subject_taught = models.CharField(max_length=100, blank=True, null=True)
    room_number = models.CharField(max_length=10, blank=True, null=True)

    def full_name(self):
        """Returns the full name with middle name if available."""
        first_name = self.user.first_name
        last_name = self.user.last_name
        middle_name = self.middle_name
        return f"{first_name} {middle_name if middle_name else ''} {last_name if last_name else ''}".strip()

    def __str__(self):
        return f"{self.full_name()} - {self.role} ({self.department.name if self.department else 'No Department'})"
