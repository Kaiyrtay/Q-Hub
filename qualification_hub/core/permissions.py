from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from teachers.models import Teacher
from students.models import Student
from certificates.models import Certificate


def create_permissions():
    # Get content types for your models
    manager_content_type = ContentType.objects.get_for_model(Teacher)
    student_content_type = ContentType.objects.get_for_model(Student)
    certificate_content_type = ContentType.objects.get_for_model(Certificate)

    # Create permissions for managers
    can_add_teacher = Permission.objects.create(
        name="Can add teacher",
        content_type=manager_content_type,
        codename="add_teacher",
    )
    can_change_teacher = Permission.objects.create(
        name="Can change teacher",
        content_type=manager_content_type,
        codename="change_teacher",
    )
    can_delete_teacher = Permission.objects.create(
        name="Can delete teacher",
        content_type=manager_content_type,
        codename="delete_teacher",
    )
    can_add_student = Permission.objects.create(
        name="Can add student",
        content_type=student_content_type,
        codename="add_student",
    )
    can_change_student = Permission.objects.create(
        name="Can change student",
        content_type=manager_content_type,
        codename="change_student",
    )
    can_delete_student = Permission.objects.create(
        name="Can delete student",
        content_type=manager_content_type,
        codename="delete_student",
    )

    # Create permissions for teachers and students (assuming both can do same on certificates)
    can_add_certificate = Permission.objects.create(
        name="Can add certificate",
        content_type=certificate_content_type,
        codename="add_certificate",
    )
    can_change_certificate = Permission.objects.create(
        name="Can change certificate",
        content_type=certificate_content_type,
        codename="change_certificate",
    )
    can_delete_certificate = Permission.objects.create(
        name="Can delete certificate",
        content_type=certificate_content_type,
        codename="delete_certificate",
    )

# Define Groups


def create_groups():
    manager_group, created = Group.objects.get_or_create(name="Managers")
    teacher_group, created = Group.objects.get_or_create(name="Teachers")
    student_group, created = Group.objects.get_or_create(name="Students")

    # Assign permissions to groups
    manager_group.permissions.add(
        can_add_teacher, can_change_teacher, can_delete_teacher,
        can_add_student, can_change_student, can_delete_student
    )
    teacher_group.permissions.add(
        can_add_certificate, can_change_certificate, can_delete_certificate)
    student_group.permissions.add(
        can_add_certificate, can_change_certificate, can_delete_certificate)


# Call functions to create permissions and groups
create_permissions()
create_groups()
