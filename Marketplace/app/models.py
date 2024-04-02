from django.contrib.auth.models import AbstractUser
from django.db import models
from . import manager

class CustomUser(AbstractUser):
    
    USER_TYPE_CHOICES = (
        ('admin', 'admin'),
        ('seller', 'seller'),
        ('customer', 'customer'), 
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    
    objects = manager.CustomUserManager()

    

    
class Products(models.Model):
    product_title = models.CharField(max_length = 20)
    Product_description = models.CharField(max_length = 50)
    product_price = models.FloatField()
    product_image = models.ImageField(upload_to='product_images/')
    