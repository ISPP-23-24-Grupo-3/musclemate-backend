from django.urls import path
from gym import views

urlpatterns = [
    path('gyms/', views.gym_list),
    path('gyms/detail/<int:id>/', views.gym_detail),
    path('gyms/detail/<str:username>/', views.gym_detail_username),
    path('gyms/delete/<int:id>/', views.gym_delete),
    path('gyms/create/', views.gym_create),
    path('gyms/update/<int:id>/', views.gym_update),
    path('gyms/standard/<int:id>/', views.subscription_standar_uptade),
    path('gyms/premium/<int:id>/', views.subscription_premium_uptade),
    path('gyms/usage/<int:gym_id>/', views.monthly_usage),
    path('gyms/usage/<int:gym_id>/year/<int:year>/', views.monthly_usage),
    path('gyms/usage/<int:gym_id>/year/<int:year>/month/<int:month>/', views.monthly_usage),
    path('gyms/usage/<int:gym_id>/month/<int:month>/', views.monthly_usage),
    path('gyms/usage/<int:gym_id>/year/<int:year>/month/<int:month>/daily/', views.daily_usage),
]