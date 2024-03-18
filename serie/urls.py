from . import views
from django.urls import path

urlpatterns = [
    path('series/', views.SerieListView.as_view(), name='serie_list'),
    path('series/detail/<int:pk>/', views.SerieDetailView.as_view(), name='serie_detail'),
    path('series/create/', views.SerieCreateView.as_view(), name='serie_create'),
    path('series/update/<int:pk>/', views.SerieUpdateView.as_view(), name='serie_update'),
    path('series/delete/<int:pk>/', views.SerieDeleteView.as_view(), name='serie_delete'),
    path('series/workout/<int:pk>/', views.SerieListByWorkoutView.as_view(), name='serie_list_workout'),
]
