# Generated by Django 4.2.11 on 2024-04-05 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_endpoint', models.TextField(max_length=500)),
                ('response_data', models.TextField(max_length=500)),
                ('request_data', models.TextField(max_length=500)),
                ('status', models.IntegerField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=20)),
                ('age', models.IntegerField()),
            ],
        ),
    ]
