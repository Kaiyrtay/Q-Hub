from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from teachers.models import Teacher
from students.models import Student
from certificates.models import Certificate


class Command(BaseCommand):
    help = "Creates initial groups and permissions"

    def handle(self, *args, **kwargs):
        # Get content types for models
        teacher_content_type = ContentType.objects.get_for_model(Teacher)
        student_content_type = ContentType.objects.get_for_model(Student)
        certificate_content_type = ContentType.objects.get_for_model(
            Certificate)

        # Create permissions
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

        # Create groups and assign permissions
        manager_group, _ = Group.objects.get_or_create(name="Managers")
        teacher_group, _ = Group.objects.get_or_create(name="Teachers")
        student_group, _ = Group.objects.get_or_create(name="Students")

        # Assign permissions to groups
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
