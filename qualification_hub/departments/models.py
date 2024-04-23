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
