from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   
    
    path('', views.SignUp, name='signUp'),
    path('dashboard', views.DashBoard, name='dashboard'),
    path('login', views.LoginUsr, name='login'),
    path('logout', views.logout_view, name='logout')
]
