from . import views
from django.urls import path

urlpatterns = [
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/<int:gymId>/', views.ClientListByGymView.as_view(), name='client_list_by_gym'),
    path('clients/detail/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/update/<int:pk>/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', views.ClientDeleteView.as_view(), name='client_delete'),
]