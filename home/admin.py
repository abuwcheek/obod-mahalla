from django.contrib import admin
from .models import Home, ContactUs


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
     list_display = ('sarlavha','created_at', 'updated_at', 'is_active', 'is_featured', 'is_published', 'is_deleted')
     search_fields = ('sarlavha',)
     list_filter = ('is_active', 'is_featured')
     prepopulated_fields = {'slug': ('sarlavha',)}
     list_editable = ('is_active', 'is_featured', 'is_published' ,'is_deleted')
     list_per_page = 10



@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
     list_display = ('viloyat', 'tuman', 'manzil', 'xonadon', 'odamlar', 'telefon', 'email', 'created_at', 'updated_at', 'is_active', 'is_deleted', 'is_featured')
     search_fields = ('viloyat', 'tuman')
     list_filter = ('is_active',)
     list_editable = ('is_active', 'is_deleted')
     list_per_page = 10


