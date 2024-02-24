from django.urls import path
from gym import views

urlpatterns = [
    path('gyms/', views.gym_list),
    path('gyms/<int:id>/', views.gym_detail),
    path('gyms/delete/<int:id>/', views.gym_delete),
]