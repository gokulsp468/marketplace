# Generated by Django 4.2.11 on 2024-04-02 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_image',
            field=models.ImageField(upload_to='product_images/'),
        ),
    ]