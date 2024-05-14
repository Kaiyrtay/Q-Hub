"""
Certificate Views for Managing Certificates in Django

This file contains views for listing, creating, updating, and deleting `Certificate` 
instances, as well as displaying detailed information about specific certificates. 
The views use Django's generic class-based views for common operations, including 
list, detail, create, update, and delete views. They also incorporate permission 
control through custom mixins.

Key Classes:
- `CertificateListView`: Lists all certificates with pagination, allowing users to 
  browse through a collection of certificates.
- `CertificateDetailView`: Displays detailed information about a specific certificate.
- `CertificateCreateView`: Allows creation of new certificates, requiring users to 
  belong to either the "Teachers" or "Students" group.
- `CertificateUpdateView`: Updates existing certificates. Requires users to be in 
  the "Managers" group or be the certificate's owner.
- `CertificateDeleteView`: Handles the deletion of certificates with permission 
  requirements similar to the update view.

Key Features:
- The `CertificateListView` includes pagination with a `paginate_by` value of 9, allowing 
  users to navigate through multiple pages of certificates.
- The `CertificateCreateView` assigns ownership based on the current user, setting 
  `teacher_owner` or `student_owner`.
- The `CertificateUpdateView` and `CertificateDeleteView` use custom mixins to enforce 
  permissions, allowing access to users in the "Managers" group or those who own the 
  certificate.

Dependencies:
- Uses the `Certificate` model from the current module.
- Relies on permission mixins from `core.mixins` to control access to certain views.
- Requires Django's `ListView`, `DetailView`, `CreateView`, `UpdateView`, and `DeleteView` 
  for class-based view functionality.

Author: Kaiyrtay
"""

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Certificate
from .forms import CertificateForm
# handle permission
from core.mixins import ManagerOrOwnerForCertificateRequiredMixin, TeacherOrStudentRequiredMixin


class CertificateListView(ListView):
    model = Certificate
    template_name = 'certificates/certificate_list.html'
    context_object_name = 'certificates'
    paginate_by = 6


class CertificateDetailView(DetailView):
    model = Certificate
    template_name = 'certificates/certificate_detail.html'
    context_object_name = 'certificate'


class CertificateCreateView(TeacherOrStudentRequiredMixin, CreateView):
    model = Certificate
    form_class = CertificateForm
    template_name = 'certificates/certificate_form.html'
    success_url = reverse_lazy('certificates:list')

    def form_valid(self, form):
        user = self.request.user

        if hasattr(user, 'teacher'):
            form.instance.teacher_owner = user.teacher
        elif hasattr(user, 'student'):
            form.instance.student_owner = user.student

        form.instance.owner = user
        return super().form_valid(form)


class CertificateUpdateView(ManagerOrOwnerForCertificateRequiredMixin, UpdateView):
    model = Certificate
    template_name = 'certificates/certificate_form.html'
    form_class = CertificateForm
    success_url = reverse_lazy('certificates:list')

    def get_view_object(self):
        certificate = self.get_object()
        if certificate is None:
            raise Http404("Certificate not found")
        return certificate
    
    def form_valid(self, form):
        return super().form_valid(form)


class CertificateDeleteView(ManagerOrOwnerForCertificateRequiredMixin, DeleteView):
    model = Certificate
    template_name = 'certificates/certificate_confirm_delete.html'
    success_url = reverse_lazy('certificates:list')

    def get_view_object(self):
        certificate = self.get_object()
        if certificate is None:
            raise Http404("Certificate not found")
        return certificate
