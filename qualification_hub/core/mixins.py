# Owner = super user
# Admin = staff member, have access to managers, departments, faculties
# Manager = Manager, have access to teachers,students
# Teacher = Teacher, have access to certificates
# Student = Student, have access to certificates
# Guest = not authenticated , can only view

from django.http import Http404
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

"""
    Apps:
    Faculties - FacultyDeleteView
    Departments - 
    Managers -
    Teachers -
    Students -
    Certificates -
"""


class SuperuserRequiredMixin(AccessMixin):
    """
    Mixin that requires the user to be a superuser.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            if not request.user.is_authenticated:
                return self.handle_no_permission()
            else:
                raise PermissionDenied(
                    "You do not have permission to access this page.")

        return super().dispatch(request, *args, **kwargs)


"""
    Apps:
    Faculties - FacultyCreateView,FacultyUpdateView
    Departments - DepartmentCreateView, DepartmentUpdateView, DepartmentDeleteView
    Managers - ManagerCreateView
    Teachers -
    Students -
    Certificates -
"""


class StaffRequiredMixin(AccessMixin):
    """
    Mixin that requires the user to be a staff member.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            if not request.user.is_authenticated:
                return self.handle_no_permission()
            else:
                raise PermissionDenied(
                    "You do not have permission to access this page.")

        return super().dispatch(request, *args, **kwargs)


"""
    Apps:
    Faculties - 
    Departments - 
    Managers -
    Teachers -TeacherCreateView
    Students - StudentCreateView
    Certificates -
"""


class ManagerGroupRequiredMixin(AccessMixin):
    """
    Mixin that requires the user to be in the "Managers" group.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.groups.filter(name='Managers').exists():
            raise PermissionDenied(
                "You do not have permission to access this page.")

        return super().dispatch(request, *args, **kwargs)


"""
    Apps:
    Faculties - 
    Departments - 
    Managers -
    Teachers -
    Students -
    Certificates - CertificateCreateView
"""


class TeacherOrStudentRequiredMixin(AccessMixin):
    """
    Mixin that requires the user to be in the "Teachers" or "Students" group.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user_groups = request.user.groups.values_list('name', flat=True)
        if 'Teachers' not in user_groups and 'Students' not in user_groups:
            raise PermissionDenied(
                "You do not have permission to access this page.")

        return super().dispatch(request, *args, **kwargs)


"""
    Apps:
    Faculties - 
    Departments - 
    Managers - ManagerDeleteView,ManagerUpdateView
    Teachers -
    Students -
    Certificates -
"""


class OwnerOrStaffRequiredMixin(AccessMixin):
    """
    Mixin that allows access to the owner or a staff member.
    """

    owner_field = "user"
    model = None

    def get_owner(self, obj):
        """
        Return the owner of the object.
        """
        return getattr(obj, self.owner_field)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        obj = self.get_object()

        if self.get_owner(obj) != request.user and not request.user.is_staff:
            raise PermissionDenied(
                "You do not have permission to access this page.")

        return super().dispatch(request, *args, **kwargs)


"""
    Apps:
    Faculties - 
    Departments - 
    Managers -
    Teachers -TeacherUpdateView,TeacherDeleteView
    Students -StudentUpdateView,StudentDeleteView
    Certificates -
"""


class ManagerOrOwnerRequiredMixin(AccessMixin):
    """
    Mixin that grants access if the user is in the "Managers" group or is the owner.
    """

    owner_field = "user"

    def get_owner(self, obj):
        """
        Return the owner of the object.
        """
        return getattr(obj, self.owner_field)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        obj = self.get_object()

        if not request.user.groups.filter(name='Managers').exists():
            if self.get_owner(obj) != request.user:
                raise PermissionDenied(
                    "You do not have permission to access this page.")

        return super().dispatch(request, *args, **kwargs)


"""
    Apps:
    Faculties - 
    Departments - 
    Managers -
    Teachers -
    Students -
    Certificates - CertificateUpdateView,CertificateDeleteView
"""


class ManagerOrOwnerForCertificateRequiredMixin(AccessMixin):
    """
    Mixin that requires the user to be in the 'Managers' group or 
    be the owner of the certificate (either student_owner or teacher_owner).
    """

    def is_owner(self, certificate, user):
        """
        Check if the user is the owner (either student_owner or teacher_owner).
        """
        if certificate is None:
            raise Http404("Certificate not found")

        # Safely check if owners are defined
        student_owner = certificate.student_owner
        teacher_owner = certificate.teacher_owner

        if (student_owner and student_owner.user == user) or (teacher_owner and teacher_owner.user == user):
            return True

        return False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission() 

        certificate = self.get_view_object() 

        if certificate is None:
            raise Http404("Certificate not found")

        if not request.user.groups.filter(name='Managers').exists():
            if not self.is_owner(certificate, request.user):
                raise PermissionDenied(
                    "You do not have permission to access this page.")

        return super().dispatch(request, *args, **kwargs)

    def get_view_object(self):
        raise NotImplementedError(
            "Subclasses must implement `get_view_object()`")
