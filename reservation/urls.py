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
    path('reservations/all/', views.ReservationListView.as_view(), name='reservation_list'),
    path('reservations/client/<int:clientId>/', views.ReservationListByClientView.as_view(), name='reservationClient_list'),
    path('reservations/event/<int:eventId>/', views.ReservationListByEventView.as_view(), name='reservationEvent_list'),
    path('reservations/byClientEvent/<int:eventId>/', views.ReservationListByClientEvent.as_view(), name='reservationClientEvent'),
    path('reservations/detail/<int:pk>/', views.ReservationDetailView.as_view(), name='reservation_detail'),
    path('reservations/user/create/', views.ReservationUserCreateView.as_view(), name='reservation_usercreate'),
    path('reservations/create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/update/<int:pk>/', views.ReservationUpdateView.as_view(), name='reservation_update'),
    path('reservations/delete/<int:pk>/', views.ReservationDeleteView.as_view(), name='reservation_delete'),
]
