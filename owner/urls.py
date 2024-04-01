"""
URL configuration for musclematebackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

urlpatterns = [
    path('owners/', views.OwnerListView.as_view(), name='owner_list'),
    path('owners/detail/<str:pk>/', views.OwnerDetailView.as_view(), name='owner_detail'),
    path('owners/create/', views.OwnerCreateView.as_view(), name='owner_create'),
    path('owners/update/<str:pk>/', views.OwnerUpdateView.as_view(), name='owner_update'),
    path('owners/delete/<int:pk>/', views.OwnerDeleteView.as_view(), name='owner_delete'),
]
