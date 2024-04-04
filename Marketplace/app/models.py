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

    
    objects = manager.CustomUserManager()

    

    
class Products(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=20)
    product_description = models.CharField(max_length=50)  
    product_price = models.FloatField()
    product_image = models.ImageField(upload_to='product_images/',blank=True)
    
    class Meta:
        ordering = ['id'] 
        

class APILog(models.Model):
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    query_params = models.JSONField(null=True, blank=True)
    response_data = models.TextField(null=True, blank=True)
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.path}"