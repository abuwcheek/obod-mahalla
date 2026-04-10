from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Home, UserRegistration
from django.contrib.auth.hashers import make_password, check_password




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
          password1 = request.POST.get('password1', '')
          password2 = request.POST.get('password2', '')

          if not ism or not familya or not email or not nomer or not jinsi:
               messages.error(request, "Barcha majburiy maydonlarni to'ldiring.")
               return redirect('register')

          if not password1 or not password2:
               messages.error(request, "Parolni ikki marta kiriting.")
               return redirect('register')

          if password1 != password2:
               messages.error(request, "Parollar mos kelmadi.")
               return redirect('register')

          if len(password1) < 6:
               messages.error(request, "Parol kamida 6 belgidan iborat bo'lsin.")
               return redirect('register')

          if jinsi not in dict(UserRegistration.GENDER_CHOICES):
               messages.error(request, "Jinsi tanlang.")
               return redirect('register')

          if UserRegistration.objects.filter(email=email).exists():
               messages.error(request, "Bu email bilan allaqachon ro'yxatdan o'tilgan.")
               return redirect('register')

          hashed_password = make_password(password1)

          created = UserRegistration.objects.create(
               ism=ism,
               familya=familya,
               email=email,
               nomer=nomer,
               jinsi=jinsi,
               rasm=rasm,
               password=hashed_password,
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
     if request.method == 'POST':
          ism = request.POST.get('ism', '').strip()
          familya = request.POST.get('familya', '').strip()
          password = request.POST.get('password', '')

          if not ism or not familya or not password:
               messages.error(request, "Ism, familya va parolni to'liq kiriting.")
               return redirect('login')

          user = UserRegistration.objects.filter(
               ism__iexact=ism,
               familya__iexact=familya
          ).first()

          if not user:
               messages.error(request, "Ism yoki familya noto'g'ri.")
               return redirect('login')

          if not user.password or not check_password(password, user.password):
               messages.error(request, "Parol xato.")
               return redirect('login')

          request.session['is_registered'] = True
          request.session['registered_email'] = user.email
          request.session['registered_name'] = f"{user.ism} {user.familya}"
          messages.success(request, f"Xush kelibsiz, {user.ism}!")
          return redirect('home')

     return render(request, 'login.html')
