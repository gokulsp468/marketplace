# Generated by Django 4.2.11 on 2024-04-08 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_customuser_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mobile_number',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
