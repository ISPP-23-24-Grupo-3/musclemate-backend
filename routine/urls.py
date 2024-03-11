from django.urls import path
from . import views

urlpatterns = [
    path('routines/', views.RoutineListView.as_view(), name='routine_list'),
    path('routines/client/<int:clientId>/', views.RoutineListByClientView.as_view(), name='routine_list_By_Client'),
    path('routines/detail/<int:pk>/', views.RoutineDetailView.as_view(), name='routine_detail'),
    path('routines/create/', views.RoutineCreateView.as_view(), name='routine_create'),
    path('routines/update/<int:pk>/', views.RoutineUpdateView.as_view(), name='routine_update'),
    path('routines/delete/<int:pk>/', views.RoutineDeleteView.as_view(), name='routine_delete'),
]
