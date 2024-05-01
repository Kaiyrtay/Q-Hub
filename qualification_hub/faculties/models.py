"""
Faculty Model Definition

This file defines the `Faculty` model, representing academic faculties in a Django project.
Each `Faculty` has attributes like name, description, dean, creation date, website, 
contact email, and location. It has a relationship with `User` to represent the dean of 
the faculty.

Key Attributes:
- `name`: A unique field representing the faculty's name.
- `description`: A textual description of the faculty.
- `dean`: A foreign key linking to the `User` who serves as the dean of the faculty. 
  This relationship uses `on_delete=models.SET_NULL` to retain the faculty even if 
  the user is deleted.
- `created_at`: Automatically set to the date and time the faculty is created.
- `website`: An optional URL field for the faculty's website.
- `contact_email`: An optional email field for the faculty's contact information.
- `location`: An optional field for the faculty's location.

Important Methods:
- `__str__()`: Returns the faculty's name, providing a string representation of the `Faculty`.

Dependencies:
- Relies on `User` from `django.contrib.auth.models` to establish a relationship with the dean.
- Uses common Django field types such as `CharField`, `TextField`, `DateTimeField`, and 
  `ForeignKey`.

Author: Kaiyrtay
"""

from django.db import models
from django.contrib.auth.models import User


class Faculty(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    dean = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="dean_of_faculty"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
