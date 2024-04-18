from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductsViewSet, basename='products')


urlpatterns = [
    
    path('', include(router.urls)),
    
    path('cart_items/', views.cart_list, name='cart_items')
    
 
]
