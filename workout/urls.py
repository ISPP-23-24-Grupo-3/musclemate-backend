from . import views
from django.urls import path

urlpatterns = [
    
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('workouts/byEquipment/<int:equipmentId>/', views.WorkoutListByEquipmentListView.as_view(),
        name='workout_list_by_equipment'),
    path('workouts/byClient/<int:clientId>/', views.WorkoutListByClientListView.as_view(),
        name='workout_list_by_client'),
    path('workouts/byRoutine/<int:routineId>/', views.WorkoutListByRoutineListView.as_view(),
        name='workout_list_by_routine'),
    path('workouts/detail/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout_detail'),
    path('workouts/create/', views.WorkoutCreateView.as_view(), name='workout_create'),
    path('workouts/update/<int:pk>/', views.WorkoutUpdateView.as_view(), name='workout_update'),
    path('workouts/delete/<int:pk>/', views.WorkoutDeleteView.as_view(), name='workout_delete'),
]
