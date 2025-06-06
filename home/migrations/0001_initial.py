# Generated by Django 5.2.1 on 2025-05-13 07:29

import djrichtextfield.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('viloyat', models.CharField(max_length=255)),
                ('tuman', models.CharField(max_length=255)),
                ('manzil', models.CharField(max_length=255)),
                ('telefon', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('facebook', models.CharField(max_length=255)),
                ('instagram', models.CharField(max_length=255)),
                ('telegram', models.CharField(max_length=255)),
                ('twitter', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('sarlavha', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('text', djrichtextfield.models.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('xonadon', models.IntegerField(default=0)),
                ('odamlar', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
