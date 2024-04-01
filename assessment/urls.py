from . import views
from django.urls import path

urlpatterns = [
    path('assessments/', views.AssessmentListView.as_view(), name='assessment_list'),
    path('assessments/client/<int:clientId>/', views.AssessmentListByClientView.as_view(),
        name='assessment_list_by_client'),
    path('assessments/equipment/<int:equipmentId>/', views.AssessmentListByEquipmentView.as_view(),
        name='assessment_list_by_equipment'),
    path('assessments/detail/<int:pk>/', views.AssessmentDetailView.as_view(), name='assessment_detail'),
    path('assessments/create/', views.AssessmentCreateView.as_view(), name='assessment_create'),
    path('assessments/update/<int:pk>/', views.AssessmentUpdateView.as_view(), name='assessment_update'),
    path('assessments/delete/<int:pk>/', views.AssessmentDeleteView.as_view(), name='assessment_delete'),
]