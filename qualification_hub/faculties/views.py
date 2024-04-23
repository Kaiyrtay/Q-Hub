from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Faculty


# List View for displaying all faculties
class FacultyListView(ListView):
    model = Faculty
    template_name = "faculties/faculty_list.html"
    context_object_name = "faculties"


# Detail View for displaying a specific faculty's details
class FacultyDetailView(DetailView):
    model = Faculty
    template_name = "faculties/faculty_detail.html"
    context_object_name = "faculty"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculty = self.get_object()

        # Add department information to the context
        # All related departments
        context['departments'] = faculty.departments.all()

        return context


# Create View for creating a new faculty
class FacultyCreateView(CreateView):
    model = Faculty
    fields = ["name", "description", "dean", "departments",
              "website", "contact_email", "location"]
    template_name = "faculties/faculty_form.html"
    success_url = reverse_lazy("faculties:list")


# Update View for updating an existing faculty
class FacultyUpdateView(UpdateView):
    model = Faculty
    fields = ["name", "description", "dean", "departments",
              "website", "contact_email", "location"]
    template_name = "faculties/faculty_form.html"
    success_url = reverse_lazy("faculties:list")


# Delete View for deleting a faculty
class FacultyDeleteView(DeleteView):
    model = Faculty
    template_name = "faculties/faculty_confirm_delete.html"
    success_url = reverse_lazy("faculties:list")
