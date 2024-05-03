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
    path('', ManagerListView.as_view(), name='list'), 
    path('create/', ManagerCreateView.as_view(),
         name='create'),  
    path('<int:pk>/', ManagerDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', ManagerUpdateView.as_view(),
         name='update'),  
    path('<int:pk>/delete/', ManagerDeleteView.as_view(),
         name='delete'),  
]
