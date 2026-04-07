from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify


class BaseModel(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     is_active = models.BooleanField(default=True)
     is_deleted = models.BooleanField(default=False)
     is_featured = models.BooleanField(default=False)
     is_published = models.BooleanField(default=False)
     

     class Meta:
          abstract = True



class Home(BaseModel):
     sarlavha = models.CharField(max_length=255)
     slug = models.SlugField(max_length=255, unique=True, blank=True)
     text = RichTextUploadingField()  # now rich-text editor with uploads in admin and forms
     image = models.ImageField(upload_to='images/', null=True, blank=True)



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
     xonadon = models.IntegerField(default=0)
     odamlar = models.IntegerField(default=0)
     telefon = models.CharField(max_length=255)
     email = models.EmailField(max_length=255, null=True, blank=True)
     facebook = models.CharField(max_length=255, null=True, blank=True)
     instagram = models.CharField(max_length=255, null=True, blank=True)
     telegram = models.CharField(max_length=255, null=True, blank=True)
     twitter = models.CharField(max_length=255, null=True, blank=True)
     image = models.ImageField(upload_to='images/', null=True, blank=True)
     name = models.CharField(max_length=255)

