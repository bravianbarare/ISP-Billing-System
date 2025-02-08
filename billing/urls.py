from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('purchase/<int:plan_id>/', views.purchase_plan, name='purchase_plan'),
    path('history/', views.transaction_history, name='transaction_history'),
]