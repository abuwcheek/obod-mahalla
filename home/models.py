from django.db import models
from djrichtextfield.models import RichTextField
from django.utils.text import slugify


class BaseModel(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     is_active = models.BooleanField(default=True)
     is_deleted = models.BooleanField(default=False)
     is_featured = models.BooleanField(default=False)

     class Meta:
          abstract = True


class Home(BaseModel):
     sarlavha = models.CharField(max_length=255)
     slug = models.SlugField(max_length=255, unique=True, blank=True)
     text = RichTextField()
     image = models.ImageField(upload_to='images/', null=True, blank=True)
     xonadon = models.IntegerField(default=0)
     odamlar = models.IntegerField(default=0)


     def __str__(self):
          return self.sarlavha 
     

     def save(self, *args, **kwargs):
          if not self.slug:
               self.slug = slugify(self.sarlavha)
          super().save(*args, **kwargs)



class ContactUs(BaseModel):
     viloyat = models.CharField(max_length=255)
     tuman = models.CharField(max_length=255)
     manzil = models.CharField(max_length=255)
     telefon = models.CharField(max_length=255)
     email = models.EmailField(max_length=255)
     facebook = models.CharField(max_length=255)
     instagram = models.CharField(max_length=255)
     telegram = models.CharField(max_length=255)
     twitter = models.CharField(max_length=255)