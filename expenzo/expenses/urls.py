from django.urls import path
from . import views
from .views import create_admin

urlpatterns = [
    path('', views.home, name='home'),
    path('create-admin/', create_admin),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_expense, name='add_expense'),
    path('list/', views.expense_list, name='expense_list'),
    path('edit/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),

]