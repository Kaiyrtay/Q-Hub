"""
Teacher Model Definition

This file defines the Teacher model, representing teachers in the system.
Each Teacher is associated with a User and can belong to a Department.
Additional attributes like middle name, phone number, contact email, 
subject taught, and room number are also included.

Important Notes:
- The `full_name()` method returns the full name of the teacher, including
  their middle name if available.
- The `save()` method ensures the associated User is added to the "Teachers" 
  group by default if not already in a group.
- The `__str__()` method provides a string representation of the teacher, 
  including the full name, role, and department.

Dependencies:
- Relies on Django's `User` model for user-related information.
- Relies on the `Department` model to represent a teacher's department.

Author: Kaiyrtay
"""

from django.contrib.auth.models import User, Group
from django.db import models
from departments.models import Department


def teacher_avatar_upload_to(instance, filename):
    # This function creates a dynamic upload path based on the manager's user ID
    return f'avatars/teachers/{instance.user.id}/{filename}'

class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="teacher")
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    role = models.CharField(max_length=100, default="Teacher")
    hire_date = models.DateField(null=True, blank=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    subject_taught = models.CharField(max_length=100, blank=True, null=True)
    room_number = models.CharField(max_length=10, blank=True, null=True)

    avatar = models.ImageField(
        upload_to=teacher_avatar_upload_to,
        default="assets/images/default_account.png",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['user__first_name', 'middle_name', 'user__last_name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.user.groups.exists():
            default_group = Group.objects.get(name='Teachers')
            self.user.groups.add(default_group)

        super().save(*args, **kwargs)

    def full_name(self):
        """Returns the full name with middle name if available."""
        first_name = self.user.first_name
        last_name = self.user.last_name
        middle_name = self.middle_name
        return f"{first_name} {middle_name if middle_name else ''} {last_name if last_name else ''}".strip()

    def __str__(self):
        return f"{self.full_name()} - {self.role} ({self.department.name if self.department else 'No Department'})"
