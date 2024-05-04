from . import views
from django.urls import path

urlpatterns = [
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/reservation/', views.EventWReservationListView.as_view(), name='event_with_reservation_list'),
    path('events/gym/<int:gymId>/', views.EventListByGymView.as_view(), name='event_list_by_gym'),
    path('events/client/<int:clientId>/', views.EventListByClientView.as_view(), name='event_list_by_client'),
    path('events/detail/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/update/<int:pk>/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/delete/<int:pk>/', views.EventDeleteView.as_view(), name='event_delete'),
]
