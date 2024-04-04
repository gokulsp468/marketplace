from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   
    
    path('', views.SignUp, name='signUp'),
    path('dashboard', views.DashBoard, name='dashboard'),
    path('login', views.LoginUsr, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('add_product', views.add_products, name='add_product'),
    path('edit_product/<int:id>', views.edit_product, name='edit_product'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    
]
