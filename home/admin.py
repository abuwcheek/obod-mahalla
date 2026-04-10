from django.contrib import admin
from .models import Home, ContactUs, UserRegistration, UserOTP
from django.utils.html import format_html


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


@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
     list_display = ('id', 'ism', 'familya', 'email', 'nomer', 'jinsi', 'daraja', 'is_active', 'is_deleted', 'created_at')
     search_fields = ('ism', 'familya', 'email', 'nomer')
     list_filter = ('jinsi', 'daraja', 'is_active', 'is_deleted')
     list_editable = ('is_active', 'is_deleted')
     list_per_page = 20


@admin.register(UserOTP)
class UserOTPAdmin(admin.ModelAdmin):
     list_display = ('user', 'user_role', 'code', 'created_at', 'status_badge', 'view_user')
     readonly_fields = ('code', 'created_at')
     search_fields = ('user__email', 'user__nomer')
     list_filter = ('is_verified', 'created_at')
     list_per_page = 20

     def status_badge(self, obj):
          color = '#16a34a' if obj.is_verified else '#dc2626'
          text = 'Tasdiqlangan' if obj.is_verified else 'Kutilmoqda'
          return format_html(
               '<span style="padding:4px 8px;border-radius:12px;background:{};color:white;font-weight:700;">{}</span>',
               color, text
          )
     status_badge.short_description = "Holat"

     def user_role(self, obj):
          return obj.user.daraja
     user_role.short_description = "Daraja"

     def view_user(self, obj):
          url = f"/admin/home/userregistration/{obj.user.id}/change/"
          return format_html('<a href="{}" target="_blank">Ko‘rish</a>', url)
     view_user.short_description = "Foydalanuvchi"


