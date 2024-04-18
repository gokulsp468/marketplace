from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('signUpRest/', views.SignUpView, name='signUprest'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('otp/generate_otp/', views.generate_otp_view ,name='generate_otp'),
    path('otp/verify_otp/', views.verify_otp_view, name= 'verify_otp'),
    path('messages/',views.message_list_view, name='message_list'),
    path('messages/create/', views.message_create_view, name='message_create'),
    
]
