from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductsViewSet, basename='products')


urlpatterns = [
    
    path('', include(router.urls)),
    
    path('cart_items/', views.cart_list, name='cart_items'),
     path('chat/', views.chat, name='chat'),
     path('supportchat/<str:roomName>',views.supportChat,name='supportchat'),
     
     
     
     
     
     path('signup', views.SignUp, name='signUp'),
    path('dashboard', views.DashBoard, name='dashboard'),
    path('login', views.LoginUsr, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('add_product', views.add_products, name='add_product'),
    path('edit_product/<int:id>', views.edit_product, name='edit_product'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    
 
]
