"""
Management Command to Create Initial Groups and Permissions

This file contains a Django management command that creates initial groups 
and sets specific permissions for those groups. It is used to set up user 
groups and associate them with appropriate permissions based on the 
`Teacher`, `Student`, and `Certificate` models.

Key Operations:
- Defines content types for `Teacher`, `Student`, and `Certificate` models.
- Creates or retrieves necessary permissions for adding, changing, and deleting 
  teachers, students, and certificates.
- Creates or retrieves the "Managers", "Teachers", and "Students" groups.
- Assigns appropriate permissions to each group:
  - "Managers" group receives permissions for managing teachers and students.
  - "Teachers" group receives permissions for managing certificates.
  - "Students" group also receives permissions for managing certificates.

Dependencies:
- Uses `ContentType` to retrieve the content types for models.
- Relies on `Group` and `Permission` from `django.contrib.auth.models` for 
  group and permission management.
- Interacts with the `Teacher`, `Student`, and `Certificate` models to create 
  and assign permissions.

How to Use:
- Run the command with `python manage.py <command_name>` to create the initial 
  groups and permissions.
- Ensure this command is executed during initial setup or when resetting permissions.

Author: Kaiyrtay
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from teachers.models import Teacher
from students.models import Student
from certificates.models import Certificate


class Command(BaseCommand):
    help = "Creates initial groups and permissions"

    def handle(self, *args, **kwargs):
        teacher_content_type = ContentType.objects.get_for_model(Teacher)
        student_content_type = ContentType.objects.get_for_model(Student)
        certificate_content_type = ContentType.objects.get_for_model(
            Certificate)

        can_add_teacher = Permission.objects.get_or_create(
            name="Can add teacher",
            content_type=teacher_content_type,
            codename="add_teacher",
        )[0]
        can_change_teacher = Permission.objects.get_or_create(
            name="Can change teacher",
            content_type=teacher_content_type,
            codename="change_teacher",
        )[0]
        can_delete_teacher = Permission.objects.get_or_create(
            name="Can delete teacher",
            content_type=teacher_content_type,
            codename="delete_teacher",
        )[0]
        can_add_student = Permission.objects.get_or_create(
            name="Can add student",
            content_type=student_content_type,
            codename="add_student",
        )[0]
        can_change_student = Permission.objects.get_or_create(
            name="Can change student",
            content_type=student_content_type,
            codename="change_student",
        )[0]
        can_delete_student = Permission.objects.get_or_create(
            name="Can delete student",
            content_type=student_content_type,
            codename="delete_student",
        )[0]

        can_add_certificate = Permission.objects.get_or_create(
            name="Can add certificate",
            content_type=certificate_content_type,
            codename="add_certificate",
        )[0]
        can_change_certificate = Permission.objects.get_or_create(
            name="Can change certificate",
            content_type=certificate_content_type,
            codename="change_certificate",
        )[0]
        can_delete_certificate = Permission.objects.get_or_create(
            name="Can delete certificate",
            content_type=certificate_content_type,
            codename="delete_certificate",
        )[0]

        manager_group, _ = Group.objects.get_or_create(name="Managers")
        teacher_group, _ = Group.objects.get_or_create(name="Teachers")
        student_group, _ = Group.objects.get_or_create(name="Students")

        manager_group.permissions.set([
            can_add_teacher, can_change_teacher, can_delete_teacher,
            can_add_student, can_change_student, can_delete_student,
        ])
        teacher_group.permissions.set([
            can_add_certificate, can_change_certificate, can_delete_certificate,
        ])
        student_group.permissions.set([
            can_add_certificate, can_change_certificate, can_delete_certificate,
        ])

        self.stdout.write(self.style.SUCCESS("Groups and permissions created"))
