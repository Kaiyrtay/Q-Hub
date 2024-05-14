"""
Manager Model Definition

This file defines the `Manager` model, representing department managers in the system.
Each `Manager` has a one-to-one relationship with a `User` and belongs to a `Department`.
The model includes additional information like role, appointed date, middle name, phone 
number, and contact email.

Key Features:
- The `save()` method ensures that the associated `User` is added to the "Managers" 
  group by default if not already in a group.
- The `full_name()` method returns the complete name of the manager, including 
  the middle name if available.
- The `__str__()` method provides a string representation of the manager, typically
  including the full name and role.

Dependencies:
- Relies on `User` from `django.contrib.auth.models` for user-related information.
- Uses `Department` from `departments.models` to establish a department association.
- Utilizes `Group` from `django.contrib.auth.models` for managing user groups.

Author: Kaiyrtay
"""

from django.contrib.auth.models import User, Group
from django.db import models
from departments.models import Department


def manager_avatar_upload_to(instance, filename):
    # This function creates a dynamic upload path based on the manager's user ID
    return f'avatars/managers/{instance.user.id}/{filename}'


class Manager(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="manager")
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="managers")
    role = models.CharField(max_length=100, default="Department Manager")
    appointed_date = models.DateField(null=True, blank=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    avatar = models.ImageField(
        upload_to=manager_avatar_upload_to,
        default="assets/images/default_account.png",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['user__first_name', 'middle_name', 'user__last_name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.user.groups.exists():
            default_group = Group.objects.get(name='Managers')
            self.user.groups.add(default_group)

        super().save(*args, **kwargs)

    def full_name(self):
        """Returns the full name with middle name if available."""
        first_name = self.user.first_name
        last_name = self.user.last_name
        middle_name = self.middle_name
        return f" {last_name if last_name else ''} {first_name} {middle_name if middle_name else ''}".strip()

    def __str__(self):
        return f"{self.full_name()} - {self.role}"
