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



class UserRegistration(BaseModel):
    # Jins uchun tanlovlar
    GENDER_CHOICES = [
        ('erkak', 'Erkak'),
        ('ayol', 'Ayol'),
    ]

    # Daraja uchun tanlovlar
    LEVEL_CHOICES = [
        ('fuqaro', 'Oddiy fuqaro'),
        ('rais', 'Rais'),
        ('muovin', 'Muovin'),
    ]

    ism = models.CharField(max_length=50)
    familya = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    nomer = models.CharField(max_length=20)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_sent_at = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    
    # Rasm uchun (media papkasiga yuklanadi)
    rasm = models.ImageField(upload_to='user_images/', null=True, blank=True)
    
    # Tanlov maydonlari (Choices)
    jinsi = models.CharField(
        max_length=10, 
        choices=GENDER_CHOICES, 
        default='jinsi'  # Placeholder tanlovni default qilib qo'yamiz
    )
    
    daraja = models.CharField(
        max_length=20, 
        choices=LEVEL_CHOICES, 
        default='fuqaro'
    )

    def __str__(self):
        return f"{self.ism} {self.familya} - {self.daraja}"

    class Meta:
        verbose_name = "Ro'yxatdan o'tgan foydalanuvchi"
        verbose_name_plural = "Ro'yxatdan o'tgan foydalanuvchilar"


class UserOTP(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=5)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "SMS kod"
        verbose_name_plural = "SMS kodlar"

    def __str__(self):
        return f"{self.user.email} - {self.code}"


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



class Elon(BaseModel):
    muallif = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    sarlavha = models.CharField(max_length=255)
    matn = RichTextUploadingField()
    rasm = models.ImageField(upload_to='elonlar/', null=True, blank=True)

    def __str__(self):
        return self.sarlavha

class Sorovnoma(BaseModel):
    muallif = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    savol = models.CharField(max_length=255)
    variant_a = models.CharField(max_length=100)
    variant_b = models.CharField(max_length=100)
    # Qo'shimcha variantlar qo'shish mumkin

    def __str__(self):
        return self.savol
    


class Ovoz(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    sorovnoma = models.ForeignKey(Sorovnoma, on_delete=models.CASCADE, related_name='ovozlar')
    tanlov = models.CharField(max_length=10) # 'A' yoki 'B' variant

    class Meta:
        unique_together = ('user', 'sorovnoma') # Bir kishi bir marta ovoz berishi uchun

    def __str__(self):
        return f"{self.user.ism} - {self.sorovnoma.savol} ({self.tanlov})"



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

     def __str__(self):
          return f"{self.viloyat} - {self.tuman}"

     class Meta:
          verbose_name = "Manzil va Aloqa"
          verbose_name_plural = "Manzil va Aloqa"


class ContactMessage(models.Model):
     full_name = models.CharField(max_length=255)
     email = models.EmailField()
     message = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default=False)

     def __str__(self):
          return f"{self.full_name} - {self.email}"

     class Meta:
          verbose_name = "Aloqa Xabari"
          verbose_name_plural = "Aloqa Xabarlari"
          ordering = ['-created_at']

