from django.contrib.auth.models import AbstractUser
from django.db import models
from . import manager
from django.contrib.auth.models import User
from django.conf import settings

class CustomUser(AbstractUser):
    
    USER_TYPE_CHOICES = (
        ('admin', 'admin'),
        ('seller', 'seller'),
        ('customer', 'customer'), 
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    mobile_number = models.IntegerField(blank=True, null=True, default=None)

    
    objects = manager.CustomUserManager()

    

    
class Products(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=20)
    product_description = models.CharField(max_length=50)  
    product_price = models.FloatField()
    product_image = models.ImageField(upload_to='product_images/',blank=True)
    
    class Meta:
        ordering = ['id'] 
        

