from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Manager
from .forms import UserManagerForm
from departments.models import Department
from collections import defaultdict
from core.mixins import StaffRequiredMixin, OwnerOrStaffRequiredMixin


# List View for displaying all managers
class ManagerListView(ListView):
    model = Manager
    template_name = 'managers/manager_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all departments
        departments = Department.objects.all()
        context['departments'] = departments

        # Group managers by their department ID
        grouped_managers = defaultdict(list)
        for manager in Manager.objects.all():
            if manager.department:  # Ensure department is not None
                grouped_managers[manager.department.id].append(manager)

        # Ensure every department has a key in the dictionary (even if it's an empty list)
        for department in departments:
            if department.id not in grouped_managers:
                grouped_managers[department.id] = []

        # Convert the defaultdict to a list of tuples for template iteration
        context['managers_grouped'] = [
            (Department.objects.get(id=dept_id), managers)
            for dept_id, managers in grouped_managers.items()
        ]

        return context


class ManagerDetailView(DetailView):
    model = Manager
    template_name = 'managers/manager_detail.html'
    context_object_name = 'manager'


class ManagerCreateView(StaffRequiredMixin, CreateView):
    model = Manager
    form_class = UserManagerForm
    template_name = 'managers/manager_form.html'
    success_url = reverse_lazy('managers:list')

    def form_valid(self, form):
        # Create a new User and link it to the new Manager
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name']
        )
        form.instance.user = user
        return super().form_valid(form)


# Form View for updating an existing manager
class ManagerUpdateView(OwnerOrStaffRequiredMixin, UpdateView):
    model = Manager
    form_class = UserManagerForm
    template_name = 'managers/manager_form.html'
    success_url = reverse_lazy('managers:list')

    def get_object(self):
        # Retrieve the Certificate object to check ownership
        obj = super().get_object()
        return obj

    def form_valid(self, form):
        manager = self.get_object()
        user = manager.user
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()  # Save changes to the user

        return super().form_valid(form)


# Delete View for deleting a manager
class ManagerDeleteView(OwnerOrStaffRequiredMixin, DeleteView):
    model = Manager
    template_name = 'managers/manager_confirm_delete.html'
    success_url = reverse_lazy('managers:list')

    def get_object(self):
        # Retrieve the Certificate object to check ownership
        obj = super().get_object()
        return obj

    def post(self, request, *args, **kwargs):
        manager = self.get_object()
        response = super().post(request, *args, **kwargs)
        manager.user.delete()
        return response
