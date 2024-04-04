from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Products



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'user_type', 'password1', 'password2']



class AddProduct(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_title', 'product_description', 'product_price', 'product_image']