from . import views
from django.urls import path

urlpatterns = [
    
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('workouts/detail/<int:pk>', views.WorkoutDetailView.as_view(), name='workout_detail'),
    path('workouts/create/', views.WorkoutCreateView.as_view(), name='workout_create'),
    path('workouts/update/<int:pk>/', views.WorkoutUpdateView.as_view(), name='workout_update'),
    path('workouts/delete/<int:pk>/', views.WorkoutDeleteView.as_view(), name='workout_delete'),
]
