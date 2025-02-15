from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.user_login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('change_password/',views.change_password,name='change_password'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('profile/',views.profile,name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
