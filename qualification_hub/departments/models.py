"""
Department Model Definition

This file defines the `Department` model, representing academic departments 
within a Django project. Each `Department` has a unique name, a head (linked 
to a `User`), and belongs to a `Faculty`. It also allows for optional 
relationships by using `SET_NULL` on deletion.

Key Attributes:
- `name`: A unique field representing the department's name.
- `head`: A foreign key linking to the `User` who serves as the head of the 
  department. This relationship uses `on_delete=models.SET_NULL` to allow 
  null values if the associated user is deleted.
- `faculty`: A foreign key to the `Faculty` model, representing the faculty 
  to which the department belongs. This also uses `SET_NULL`.

Important Methods:
- `__str__()`: Returns the department's name as its string representation.

Dependencies:
- Relies on `User` from `django.contrib.auth.models` for user-related operations.
- Uses `Faculty` from `faculties.models` to establish the department-faculty relationship.
- Employs common Django field types like `CharField` and `ForeignKey`.

Author: Kaiyrtay
"""

from django.db import models
from django.contrib.auth.models import User
from faculties.models import Faculty


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    head = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="head_of_department"
    )
    faculty = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name="departments"
    )

    def __str__(self):
        return self.name
