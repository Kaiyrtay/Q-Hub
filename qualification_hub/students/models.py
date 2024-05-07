"""
Student Model Definition

This file defines the `Student` model, representing students in the system.
Each `Student` has a one-to-one relationship with a `User` and can belong 
to a `Department`. The model also includes additional information like role, 
enrollment date, graduation date, middle name, phone number, contact email, 
and major.

Key Features:
- `full_name()`: Returns the full name of the student, including the middle name if available.
- `save()`: Ensures the associated `User` is added to the "Students" group by default if not already in a group.
- `__str__()`: Returns a string representation of the student, including their full name, role, and department.

Dependencies:
- Requires `User` from `django.contrib.auth.models` to manage user-related information.
- Uses `Department` from `departments.models` for the department association.
- Utilizes `Group` from `django.contrib.auth.models` to manage user groups.

Author: Kaiyrtay
"""

from django.contrib.auth.models import User, Group
from django.db import models
from departments.models import Department


def student_avatar_upload_to(instance, filename):
    # This function creates a dynamic upload path based on the manager's user ID
    return f'avatars/students/{instance.user.id}/{filename}'


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student")
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    role = models.CharField(max_length=100, default="Student")
    enrollment_date = models.DateField(
        null=True, blank=True)
    graduation_date = models.DateField(null=True, blank=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    contact_email = models.EmailField(
        blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)

    avatar = models.ImageField(
        upload_to=student_avatar_upload_to,
        default="assets/images/default_account.png",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['user__first_name', 'middle_name', 'user__last_name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.user.groups.exists():
            default_group = Group.objects.get(name='Students')
            self.user.groups.add(default_group)

        super().save(*args, **kwargs)

    def full_name(self):
        """Returns the full name with the middle name if available."""
        first_name = self.user.first_name
        last_name = self.user.last_name
        middle_name = self.middle_name
        return f"{first_name} {middle_name if middle_name else ''} {last_name}".strip()

    def __str__(self):
        return f"{self.full_name()} - {self.role} ({self.department.name if self.department else 'No Department'})"
