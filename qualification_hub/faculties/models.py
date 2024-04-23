from django.db import models
from django.contrib.auth.models import User
from departments.models import Department


class Faculty(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    dean = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="dean_of_faculty"
    )
    departments = models.ManyToManyField(
        Department, related_name="faculties", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
