from django.urls import path
from .views import (
    ManagerListView,
    ManagerDetailView,
    ManagerCreateView,
    ManagerUpdateView,
    ManagerDeleteView,
)

app_name = 'managers'

urlpatterns = [
    path('', ManagerListView.as_view(), name='list'),  # List of all managers
    path('create/', ManagerCreateView.as_view(),
         name='create'),  # Create a new manager
    # Detail view of a specific manager
    path('<int:pk>/', ManagerDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', ManagerUpdateView.as_view(),
         name='update'),  # Update a specific manager
    path('<int:pk>/delete/', ManagerDeleteView.as_view(),
         name='delete'),  # Delete a specific manager
]
