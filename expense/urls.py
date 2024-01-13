from django.urls import path
from . import views

urlpatterns = [
    path('create_expense/', views.create_expense, name='create_expense'),
    path('create_spent/', views.create_spent, name='create_spent'),
    path('<int:expense_id>/spents/<int:spent_id>/', views.view_spent, name='view_spent'),
    path('dashboard_spents/', views.dashboard_spents, name='dashboard_spents'),
    path('edit_spent/<int:spent_id>/', views.edit_spent, name='edit_spent'),
]