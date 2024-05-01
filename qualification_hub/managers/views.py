"""
Manager Views for Managing Managers in Django

This file contains views for listing, creating, updating, and deleting 
`Manager` instances, as well as displaying detailed information about 
individual managers. It uses Django's generic class-based views for common 
operations like `ListView`, `DetailView`, `CreateView`, `UpdateView`, and 
`DeleteView`.

Key Classes:
- `ManagerListView`: Lists managers, grouped by department, with pagination.
- `ManagerDetailView`: Displays detailed information about a specific manager.
- `ManagerCreateView`: Allows creation of new manager instances, with associated 
  user information.
- `ManagerUpdateView`: Updates existing manager records, supporting user-related 
  updates like username and email.
- `ManagerDeleteView`: Handles the deletion of manager records and the associated 
  `User` object.

Important Features:
- The `ManagerListView` uses a `defaultdict` to group managers by department and 
  provides pagination.
- The `ManagerCreateView` creates a new `User` when adding a manager.
- The `ManagerDeleteView` deletes the associated `User` when removing a manager.

Dependencies:
- Uses the `Manager` model from the current module.
- Relies on `User` from `django.contrib.auth.models` to handle user information.
- Interacts with the `Department` model to group managers by department.
- Utilizes mixins like `StaffRequiredMixin` and `OwnerOrStaffRequiredMixin` for 
  permission control and access checks.

Author: Kaiyrtay
"""

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Manager
from .forms import UserManagerForm
from departments.models import Department
from collections import defaultdict
from core.mixins import StaffRequiredMixin, OwnerOrStaffRequiredMixin
from django.core.paginator import Paginator


class ManagerListView(ListView):
    model = Manager
    template_name = 'managers/manager_list.html'
    context_object_name = 'managers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments = Department.objects.all()

        grouped_managers = defaultdict(list)
        for manager in Manager.objects.all():
            if manager.department:
                grouped_managers[manager.department.id].append(manager)

        managers_grouped = []
        for dept_id, managers in grouped_managers.items():
            paginator = Paginator(managers, 5)  # Paginate by 5
            page_number = self.request.GET.get(f'page_dept_{dept_id}')
            managers_paginated = paginator.get_page(page_number)
            department = Department.objects.get(id=dept_id)
            managers_grouped.append((department, managers_paginated))

        context['managers_grouped'] = managers_grouped
        context['departments'] = departments

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
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name']
        )
        form.instance.user = user
        return super().form_valid(form)


class ManagerUpdateView(OwnerOrStaffRequiredMixin, UpdateView):
    model = Manager
    form_class = UserManagerForm
    template_name = 'managers/manager_form.html'
    success_url = reverse_lazy('managers:list')

    def get_object(self):
        obj = super().get_object()
        return obj

    def form_valid(self, form):
        manager = self.get_object()
        user = manager.user
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        return super().form_valid(form)


class ManagerDeleteView(OwnerOrStaffRequiredMixin, DeleteView):
    model = Manager
    template_name = 'managers/manager_confirm_delete.html'
    success_url = reverse_lazy('managers:list')

    def get_object(self):
        obj = super().get_object()
        return obj

    def post(self, request, *args, **kwargs):
        manager = self.get_object()
        response = super().post(request, *args, **kwargs)
        manager.user.delete()
        return response
