from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View
from django.utils import timezone
import random
from datetime import timedelta
from django.conf import settings
from .models import Home, ContactUs, UserRegistration, UserOTP
from django.core.mail import send_mail




def home(request):
     first_news = Home.objects.filter(is_active=True).first()
     new_news = Home.objects.filter(is_active=True).order_by('-created_at')[:3]
     featured_news = Home.objects.filter(is_active=True, is_featured=True)[:2]
     all_news = Home.objects.filter(is_active=True).all()
     solo_news = Home.objects.filter(is_active=True).order_by('-created_at').distinct()[:1]
     context = {
          'first_news': first_news,
          'new_news': new_news,
          'featured_news': featured_news,
          'all_news': all_news,
          'solo_news': solo_news,
     }
     return render(request, 'index.html', context)


def register(request):
     if request.method == 'POST':
          ism = request.POST.get('ism', '').strip()
          familya = request.POST.get('familya', '').strip()
          email = request.POST.get('email', '').strip().lower()
          nomer = request.POST.get('nomer', '').strip()
          jinsi = request.POST.get('jinsi', '').strip()
          rasm = request.FILES.get('rasm')

          if not ism or not familya or not email or not nomer or not jinsi:
               messages.error(request, "Barcha majburiy maydonlarni to'ldiring.")
               return redirect('register')

          if jinsi not in dict(UserRegistration.GENDER_CHOICES):
               messages.error(request, "Jinsi tanlang.")
               return redirect('register')

          if UserRegistration.objects.filter(email=email).exists():
               messages.error(request, "Bu email bilan allaqachon ro'yxatdan o'tilgan.")
               return redirect('register')

          created = UserRegistration.objects.create(
               ism=ism,
               familya=familya,
               email=email,
               nomer=nomer,
               jinsi=jinsi,
               rasm=rasm,
          )
          request.session['is_registered'] = True
          request.session['registered_email'] = email
          request.session['registered_name'] = f"{created.ism} {created.familya}"
          messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz.")
          return redirect('home')

     return render(request, 'register.html')


def profile(request):
     email = request.session.get('registered_email')
     if not email:
          messages.info(request, "Profilni ko'rish uchun avval ro'yxatdan o'ting.")
          return redirect('register')

     user = UserRegistration.objects.filter(email=email).first()
     if not user:
          messages.warning(request, "Profil ma'lumoti topilmadi. Iltimos, qayta ro'yxatdan o'ting.")
          request.session.pop('is_registered', None)
          request.session.pop('registered_email', None)
          request.session.pop('registered_name', None)
          return redirect('register')

     context = {"profile": user}
     return render(request, 'profile.html', context)


def logout_profile(request):
     request.session.pop('is_registered', None)
     request.session.pop('registered_email', None)
     request.session.pop('registered_name', None)
     messages.success(request, "Tizimdan chiqdingiz.")
     return redirect('home')


def login_request(request):
     show_code_form = False
     pending_email = request.session.get('otp_pending_email')
     expiry_seconds = 60

     # clear pending if last OTP expired
     if pending_email:
          latest = UserOTP.objects.filter(user__email=pending_email, is_verified=False).order_by('-created_at').first()
          if not latest or (latest.created_at and timezone.now() > latest.created_at + timedelta(seconds=expiry_seconds)):
               request.session.pop('otp_pending_email', None)
               pending_email = None

     if request.method == 'POST' and 'email' in request.POST:
          email = request.POST.get('email', '').strip().lower()
          user = UserRegistration.objects.filter(email=email).first()
          if not user:
               messages.error(request, "Bu email bo'yicha foydalanuvchi topilmadi.")
               return redirect('login')

          code = str(random.randint(10000, 99999))
          UserOTP.objects.create(user=user, code=code, is_verified=False)

          request.session['otp_pending_email'] = email
          show_code_form = True
          messages.success(request, f"Kod emailingizga yuborildi: {user.email}")
          _send_email_code(user.email, code)

     if request.method == 'POST' and 'code' in request.POST:
          code = request.POST.get('code', '').strip()
          email = pending_email
          if not email:
               messages.error(request, "Avval emailni kiriting.")
               return redirect('login')

          user = UserRegistration.objects.filter(email=email).first()
          if not user:
               messages.error(request, "Bu email bo'yicha foydalanuvchi topilmadi.")
               return redirect('login')

          otp = UserOTP.objects.filter(user=user, is_verified=False).order_by('-created_at').first()
          if not otp:
               messages.error(request, "Avval kod so'rang.")
               return redirect('login')

          if otp.created_at and timezone.now() > otp.created_at + timedelta(seconds=expiry_seconds):
               messages.error(request, "Kodning amal qilish muddati tugadi. Qaytadan kod oling.")
               request.session.pop('otp_pending_email', None)
               return redirect('login')

          if len(code) != 5 or not code.isdigit():
               messages.error(request, "Kod 5 xonali son bo'lishi kerak.")
               show_code_form = True
          elif code != otp.code:
               messages.error(request, "Kod noto'g'ri.")
               show_code_form = True
          else:
               # muvaffaqiyatli login
               request.session['is_registered'] = True
               request.session['registered_email'] = user.email
               request.session['registered_name'] = f"{user.ism} {user.familya}"
               otp.is_verified = True
               otp.save(update_fields=['is_verified'])
               request.session.pop('otp_pending_email', None)
               messages.success(request, "Tizimga kirdingiz.")
               return redirect('home')

     if pending_email:
          show_code_form = True

     context = {
          "show_code_form": show_code_form,
     }
     return render(request, 'login.html', context)


def _send_email_code(email, code):
     subject = "Obod Mahalla tasdiq kodi"
     body = f"Sizning tasdiq kodingiz: {code}\n\nKod 1 daqiqa davomida amal qiladi."
     from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
     if not from_email or not email:
          print("Email not sent: DEFAULT_FROM_EMAIL yoki qabul qiluvchi yo'q.")
          return
     try:
          send_mail(subject, body, from_email, [email], fail_silently=False)
     except Exception as exc:
          print(f"Email send failed: {exc}")
