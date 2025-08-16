from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.logout, name='logout'),
] 