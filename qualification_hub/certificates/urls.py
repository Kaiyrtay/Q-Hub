from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('', views.CertificateListView.as_view(), name='list'),
    path('<int:pk>/', views.CertificateDetailView.as_view(), name='detail'),
    path('create/', views.CertificateCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.CertificateUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.CertificateDeleteView.as_view(), name='delete'),
]
