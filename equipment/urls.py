from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('equipments/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('equipments/detail/<int:pk>/', views.EquipmentDetailView.as_view(), name='equipment_detail'),
    path('equipments/create/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('equipments/update/<int:pk>/', views.EquipmentUpdateView.as_view(), name='equipment_update'),
    path('equipments/delete/<int:pk>/', views.EquipmentDeleteView.as_view(), name='equipment_delete'),
    path('equipments/time/<int:pk>/', views.EquipmentObtainTime.as_view(), name="equipment_timer"),
    path('equipments/global/', views.EquipmentGlobalList.as_view(), name='equipment_global'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)