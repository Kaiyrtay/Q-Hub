from django.db import models
from teachers.models import Teacher
from students.models import Student


class Certificate(models.Model):
    certificate_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    issuing_authority = models.CharField(max_length=100, blank=True)
    certificate_number = models.CharField(max_length=50, unique=True)
    verification_url = models.URLField(blank=True, null=True)
    date_earned = models.DateField(blank=True, null=True)

    student_owner = models.ForeignKey(
        Student, on_delete=models.SET_NULL, null=True, related_name='certificates')
    teacher_owner = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name='certificates')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.certificate_name} - {self.organization}"
