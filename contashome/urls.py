from django.contrib import admin
from . import views
from expense import views as views_two
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('expenses/<int:expense_id>/spents/', views_two.list_spents, name='list_spents'),
    path('edit_expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('expenses/<int:expense_id>/history/', views.view_history, name='view_history'),
    path('accounts/', include('account.urls')),
    path('expenses/', include('expense.urls')),
    path('pending/', views.pending_spents, name='pending_spents'),
    path('approve/<int:spent_id>/', views.approve_spent, name='approve_spent'),
    path('reject/<int:spent_id>/', views.reject_spent, name='reject_spent'),
    path('resubmit/<int:spent_id>/', views.resubmit_spent, name='resubmit_spent'),
]