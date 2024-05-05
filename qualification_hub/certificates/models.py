"""
Certificate Model Definition

This file defines the `Certificate` model, representing certificates awarded 
to students and teachers. It contains attributes like certificate name, organization, 
description, expiration date, issuing authority, certificate number, verification 
URL, and date earned. The model has foreign key relationships with `Student` and 
`Teacher` to indicate ownership.

Key Attributes:
- `certificate_name`: The name of the certificate.
- `organization`: The name of the organization issuing the certificate.
- `description`: An optional field providing additional information about the certificate.
- `expiration_date`: An optional date indicating when the certificate expires.
- `issuing_authority`: An optional field representing the authority that issued the certificate.
- `certificate_number`: A unique identifier for the certificate.
- `verification_url`: An optional URL for verifying the certificate.
- `date_earned`: An optional date indicating when the certificate was earned.
- `student_owner`: A foreign key linking to `Student` to represent student ownership.
- `teacher_owner`: A foreign key linking to `Teacher` to represent teacher ownership.
- `updated_at`: A timestamp indicating when the certificate was last updated.
- `created_at`: A timestamp indicating when the certificate was created.

Important Methods:
- `__str__()`: Returns a string representation of the certificate, typically the 
  certificate name and organization.

Dependencies:
- Relies on `Teacher` from `teachers.models` for teacher-related operations.
- Uses `Student` from `students.models` for student-related operations.
- Utilizes common Django field types like `CharField`, `TextField`, `DateField`, 
  `URLField`, and `ForeignKey`.

Author: Kaiyrtay
"""

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

    class Meta:
        ordering = ['-date_earned', 'organization', 'certificate_name']

    def __str__(self):
        return f"{self.certificate_name} - {self.organization}"
