from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('set-budget/', views.set_budget, name='set_budget'),
    path('update-transaction/<int:id>/', views.update_transaction, name='update_transaction'),
    path('delete-transaction/<int:id>/', views.delete_transaction, name='delete_transaction'),
    path('transactions/', views.transactions, name='transactions'),
    path('budget-overview/', views.budget_overview, name='budget_overview'),
    path('logout/', views.custom_logout, name='logout'),
    path('pdf/', views.pdf, name='pdf'),
    path('admin/', admin.site.urls),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('expenses/', views.expenses, name='expenses'),
    path('update_expense/<id>', views.update_expense, name='update_expense'),
    path('delete_expense/<id>', views.delete_expense, name='delete_expense'),
]