from django.urls import path
from api import views

urlpatterns = [
    path('gyms/', views.py.gym_list),
    path('gyms/<int:id>/', views.gym_detail),
    path('gyms/delete/<int:id>/', views.gym_delete),
]