from django.contrib.auth.models import AbstractUser
from django.db import models
from . import manager
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver



class CustomUser(AbstractUser):
    
    USER_TYPE_CHOICES = (
        ('admin', 'admin'),
        ('seller', 'seller'),
        ('customer', 'customer'), 
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    mobile_number = models.CharField(blank=True, null=True, default=None, max_length=20)

    
    objects = manager.CustomUserManager()



    
class Products(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=20)
    product_description = models.CharField(max_length=50)  
    product_price = models.FloatField()
    product_image = models.ImageField(upload_to='product_images/')
    
    class Meta:
        ordering = ['id'] 
        


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products, through='CartProduct')

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def total_cash(self):
        total = sum(cart_product.product.product_price * cart_product.quantity for cart_product in self.cartproduct_set.all())
        return total

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in cart"
    
    
    
@receiver(post_save, sender=CartProduct)
def remove_product_from_cart(sender, instance, **kwargs):
    if instance.quantity == 0:
        instance.delete()