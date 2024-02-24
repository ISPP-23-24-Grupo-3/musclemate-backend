from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('equipment/<int:id>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/new/', views.equipment_create, name='equipment_create'),
    path('equipment/<int:id>/edit/', views.equipment_update, name='equipment_update'),
    path('equipment/<int:id>/delete/', views.equipment_delete, name='equipment_delete'),
]