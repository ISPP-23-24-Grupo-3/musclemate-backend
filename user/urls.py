from . import views
from django.urls import path

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
]