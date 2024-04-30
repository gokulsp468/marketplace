from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.CustomUser)
admin.site.register(models.Products)
admin.site.register(models.Cart)
admin.site.register(models.CartProduct)
admin.site.register(models.Chat)
admin.site.register(models.ChatMessage)

