from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Certificate
from core.mixins import ManagerOrOwnerForCertificateRequiredMixin, TeacherOrStudentRequiredMixin


class CertificateListView(ListView):
    model = Certificate
    template_name = 'certificates/certificate_list.html'
    context_object_name = 'certificates'


class CertificateDetailView(DetailView):
    model = Certificate
    template_name = 'certificates/certificate_detail.html'
    context_object_name = 'certificate'


class CertificateCreateView(TeacherOrStudentRequiredMixin, CreateView):
    model = Certificate
    template_name = 'certificates/certificate_form.html'
    fields = ['certificate_name', 'organization', 'description', 'expiration_date',
              'issuing_authority', 'certificate_number', 'verification_url', 'date_earned']
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
    fields = ['certificate_name', 'organization', 'description', 'expiration_date',
              'issuing_authority', 'certificate_number', 'verification_url', 'date_earned']
    success_url = reverse_lazy('certificates:list')

    def get_view_object(self):
        certificate = self.get_object()
        if certificate is None:
            raise Http404("Certificate not found")
        return certificate


class CertificateDeleteView(ManagerOrOwnerForCertificateRequiredMixin, DeleteView):
    model = Certificate
    template_name = 'certificates/certificate_confirm_delete.html'
    success_url = reverse_lazy('certificates:list')

    def get_view_object(self):
        certificate = self.get_object()
        if certificate is None:
            raise Http404("Certificate not found")
        return certificate
