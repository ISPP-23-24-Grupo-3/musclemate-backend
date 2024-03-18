from . import views
from django.urls import path

urlpatterns = [
    path('tickets/', views.TicketListView.as_view(), name='ticket_list'),
    path('tickets/detail/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('tickets/byClient/<int:clientId>/', views.TicketListByClientView.as_view(), name='ticket_listByClient'),
    path('tickets/byEquipment/<int:equipmentId>/', views.TicketListByEquipmentView.as_view(), name='ticket_listByEquipment'),
    path('tickets/create/', views.TicketCreateView.as_view(), name='ticket_create'),
    path('tickets/update/<int:pk>/', views.TicketUpdateView.as_view(), name='ticket_update'),
    path('tickets/delete/<int:pk>/', views.TicketDeleteView.as_view(), name='ticket_delete'),
]