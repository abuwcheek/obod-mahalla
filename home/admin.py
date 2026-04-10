from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Home, ContactUs, UserRegistration, UserOTP, Elon, Sorovnoma, Ovoz



# --- 1. HOME ADMIN ---
@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('sarlavha', 'created_at', 'is_active', 'is_featured', 'is_published')
    search_fields = ('sarlavha',)
    list_filter = ('is_active', 'is_featured')
    prepopulated_fields = {'slug': ('sarlavha',)}
    list_editable = ('is_active', 'is_featured', 'is_published')
    list_per_page = 15



# --- 2. CONTACT US ADMIN ---
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('viloyat', 'tuman', 'manzil', 'telefon', 'odamlar', 'is_active')
    search_fields = ('viloyat', 'tuman', 'telefon')
    list_filter = ('is_active', 'viloyat')
    list_editable = ('is_active',)
    list_per_page = 15



# --- 3. FOYDALANUVCHILAR ADMIN ---
@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'ism', 'familya', 'email', 'nomer', 'daraja', 'is_active')
    list_display_links = ('id', 'ism', 'familya')
    search_fields = ('ism', 'familya', 'email', 'nomer')
    list_filter = ('daraja', 'jinsi', 'is_active')
    list_editable = ('is_active',)
    list_per_page = 20



# --- 4. OTP TASDIQLASH ADMIN ---
@admin.register(UserOTP)
class UserOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_role', 'code', 'status_badge', 'created_at')
    readonly_fields = ('code', 'created_at')
    search_fields = ('user__email', 'user__nomer')
    list_filter = ('is_verified',)

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



# --- 5. E'LONLAR ADMIN ---
@admin.register(Elon)
class ElonAdmin(admin.ModelAdmin):
    list_display = ('sarlavha', 'muallif', 'display_rasm', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('sarlavha', 'matn')
    list_editable = ('is_active',)

    def display_rasm(self, obj):
        if obj.rasm:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px; object-fit: cover;" />', obj.rasm.url)
        return "Rasm yo'q"
    display_rasm.short_description = 'Rasm'



# --- 6. SO'ROVNOMALAR ADMIN (STATISTIKA SHU YERDA) ---
@admin.register(Sorovnoma)
class SorovnomaAdmin(admin.ModelAdmin):
    # 'muallif' o'rniga biz yaratgan 'muallif_with_title' funksiyasini chiqaramiz
    list_display = ('savol', 'muallif_with_title', 'get_stats_a', 'get_stats_b', 'total_votes', 'is_active')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('show_votes_list',)
    list_editable = ('is_active',)

    # 1. Muallif qismini to'g'irlash: Ism (link) + Unvon (text)
    def muallif_with_title(self, obj):
        if obj.muallif:
            # Foydalanuvchini tahrirlash sahifasiga link
            url = reverse('admin:home_userregistration_change', args=[obj.muallif.id])
            
            # Ism-familiya link bo'ladi, darajasi esa oddiy chiziqcha bilan yonida turadi
            return format_html(
                '<a href="{}" style="font-weight:bold; color:#00d2ff;">{} {}</a> - <span style="color:#888;">{}</span>', 
                url, obj.muallif.ism, obj.muallif.familya, obj.muallif.daraja
            )
        return "Noma'lum"
    
    muallif_with_title.short_description = 'Muallif va Unvon'

    # --- Qolgan statistika funksiyalari o'zgarmaydi ---
    def get_stats_a(self, obj):
        count = obj.ovozlar.filter(tanlov='A').count()
        return format_html('<b style="color: #2ecc71;">A: {} ta</b>', count)
    get_stats_a.short_description = "A varianti"

    def get_stats_b(self, obj):
        count = obj.ovozlar.filter(tanlov='B').count()
        return format_html('<b style="color: #e74c3c;">B: {} ta</b>', count)
    get_stats_b.short_description = "B varianti"

    def total_votes(self, obj):
        return obj.ovozlar.count()
    total_votes.short_description = "Jami ovozlar"

    def show_votes_list(self, obj):
        ovozlar = obj.ovozlar.all()
        if not ovozlar: return "Hali ovozlar yo'q"
        html = '<table style="width:100%; border:1px solid #ddd; border-collapse: collapse;">'
        html += '<tr style="background:#f4f4f4;"><th>Foydalanuvchi</th><th>Tanlov</th></tr>'
        for ovoz in ovozlar:
            user_url = reverse('admin:home_userregistration_change', args=[ovoz.user.id])
            color = "green" if ovoz.tanlov == 'A' else "red"
            html += f'<tr><td style="border:1px solid #ddd; padding:8px;">'
            html += f'<a href="{user_url}">{ovoz.user.ism} {ovoz.user.familya}</a></td>'
            html += f'<td style="border:1px solid #ddd; padding:8px; color:{color};"><b>{ovoz.tanlov}</b></td></tr>'
        html += '</table>'
        return format_html(html)
    
    show_votes_list.short_description = "Ovoz berganlar ro'yxati"



# --- 7. OVOZLAR ADMIN (KIM NIMA DEGANINI ODDIY KO'RISH) ---
@admin.register(Ovoz)
class OvozAdmin(admin.ModelAdmin):
    list_display = ('user', 'sorovnoma', 'tanlov')
    list_filter = ('tanlov', 'sorovnoma')

# Admin panel sozlamalari
admin.site.site_header = "Obod Mahalla | Admin Panel"
admin.site.site_title = "Admin Boshqaruvi"
admin.site.index_title = "Mahalla boshqaruv tizimiga xush kelibsiz"


