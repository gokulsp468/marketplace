# Generated by Django 4.2.11 on 2024-04-04 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_apilog_alter_products_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apilog',
            old_name='body',
            new_name='response_data',
        ),
    ]
