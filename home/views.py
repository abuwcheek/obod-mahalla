from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from .forms import UserProfileEditForm
from .models import Home, UserRegistration, Elon, Sorovnoma, Ovoz, ContactMessage, ContactUs



def home(request):
    # 1. E'lonlar
    elonlar_list = Elon.objects.filter(is_active=True).order_by('-created_at')
    
    # 2. So'rovnomalar
    active_polls = Sorovnoma.objects.filter(is_active=True).order_by('-created_at')[:2]

    # Sessiyadan joriy foydalanuvchini aniqlash
    user_email = request.session.get('registered_email')
    current_user = UserRegistration.objects.filter(email=user_email).first() if user_email else None

    # Har bir so'rovnomaga ovoz berish ma'lumotlarini qo'shish
    for poll in active_polls:
        # Umumiy ovozlar sonini hisoblash
        total_votes = Ovoz.objects.filter(sorovnoma=poll).count()
        a_votes = Ovoz.objects.filter(sorovnoma=poll, tanlov='A').count()
        b_votes = Ovoz.objects.filter(sorovnoma=poll, tanlov='B').count()
        
        # Foizni hisoblash
        if total_votes > 0:
            poll.a_percent = round((a_votes / total_votes) * 100)
            poll.b_percent = round((b_votes / total_votes) * 100)
        else:
            poll.a_percent = 0
            poll.b_percent = 0
        
        poll.a_count = a_votes
        poll.b_count = b_votes
        poll.total_votes = total_votes
        
        # Foydalanuvchi ovoz berganligi va tanlovi
        if current_user:
            user_vote = Ovoz.objects.filter(sorovnoma=poll, user=current_user).first()
            if user_vote:
                poll.user_voted = True
                poll.user_choice = user_vote.tanlov
            else:
                poll.user_voted = False
                poll.user_choice = None
        else:
            poll.user_voted = False
            poll.user_choice = None

    old_news = Home.objects.filter(is_active=True).order_by('-created_at').first()
    all_news = Home.objects.filter(is_active=True).order_by('-created_at')
    solo_news = Home.objects.filter(is_active=True, is_published=True).order_by('-created_at').first()
    featured_news = Home.objects.filter(is_active=True, is_featured=True).order_by('-created_at').first()
    contact_us = ContactUs.objects.first()
    context = {
        'elonlar': elonlar_list,
        'active_polls': active_polls,

        'old_news': old_news,
        'all_news': all_news,
        'solo_news': solo_news,
        'featured_news': featured_news,
        'contact_us': contact_us,
    }
    return render(request, 'index.html', context)



def vote(request, poll_id):
    """ Ovoz berish jarayoni """
    user_email = request.session.get('registered_email')
    user = UserRegistration.objects.filter(email=user_email).first()

    if request.method == 'POST' and user:
        poll = get_object_or_404(Sorovnoma, id=poll_id)
        choice = request.POST.get('choice')

        # Faqat bir marta ovoz berishni bazada tekshirish
        if not Ovoz.objects.filter(sorovnoma=poll, user=user).exists():
            if choice in ['A', 'B']:
                Ovoz.objects.create(sorovnoma=poll, user=user, tanlov=choice)
    
    return redirect('home')


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

        if not all([ism, familya, email, nomer, jinsi, password1, password2]):
            messages.error(request, "Barcha majburiy maydonlarni to'ldiring.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Parollar mos kelmadi.")
            return redirect('register')

        if len(password1) < 6:
            messages.error(request, "Parol kamida 6 belgidan iborat bo'lsin.")
            return redirect('register')

        if UserRegistration.objects.filter(email=email).exists():
            messages.error(request, "Bu email bilan allaqachon ro'yxatdan o'tilgan.")
            return redirect('register')

        hashed_password = make_password(password1)
        created = UserRegistration.objects.create(
            ism=ism, familya=familya, email=email,
            nomer=nomer, jinsi=jinsi, rasm=rasm,
            password=hashed_password
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
        return redirect('login')

    user = get_object_or_404(UserRegistration, email=email)
    return render(request, 'profile.html', {"profile": user})



def edit_profile(request):
    email = request.session.get('registered_email')
    if not email:
        return redirect('login')

    user = get_object_or_404(UserRegistration, email=email)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            request.session['registered_email'] = user.email
            messages.success(request, "Ma'lumotlaringiz muvaffaqiyatli yangilandi.")
            return redirect('profile')
    else:
        form = UserProfileEditForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})



def create_elon(request):
    email = request.session.get('registered_email')
    if not email:
        messages.error(request, "Avval tizimga kiring.")
        return redirect('login')

    user = get_object_or_404(UserRegistration, email=email)

    if user.daraja == 'fuqaro':
        messages.error(request, "Sizda e'lon yaratish huquqi yo'q.")
        return redirect('home')

    if request.method == 'POST':
        sarlavha = request.POST.get('sarlavha')
        matn = request.POST.get('matn')
        rasm = request.FILES.get('rasm')

        if not sarlavha or not matn:
            messages.error(request, "Sarlavha va matn to'ldirilishi shart!")
            return redirect('create_elon')

        Elon.objects.create(
            muallif=user, sarlavha=sarlavha, matn=matn, rasm=rasm,
            is_active=True, is_published=True
        )
        messages.success(request, "E'lon muvaffaqiyatli qo'shildi!")
        return redirect('home')

    return render(request, 'create_elon.html')



def create_sorovnoma(request):
    email = request.session.get('registered_email')
    if not email:
        return redirect('login')

    user = get_object_or_404(UserRegistration, email=email)

    if user.daraja == 'fuqaro':
        messages.error(request, "Sizda so'rovnoma yaratish huquqi yo'q!")
        return redirect('home')

    if request.method == 'POST':
        savol = request.POST.get('savol')
        v_a = request.POST.get('variant_a')
        v_b = request.POST.get('variant_b')

        if not all([savol, v_a, v_b]):
            messages.error(request, "Barcha variantlarni to'ldiring.")
            return redirect('create_sorovnoma')

        Sorovnoma.objects.create(
            muallif=user, savol=savol, variant_a=v_a, variant_b=v_b, is_active=True
        )
        messages.success(request, "So'rovnoma muvaffaqiyatli qo'shildi!")
        return redirect('home')

    return render(request, 'create_sorovnoma.html')




def login_request(request):
    if request.method == 'POST':
        ism = request.POST.get('ism', '').strip()
        familya = request.POST.get('familya', '').strip()
        password = request.POST.get('password', '')

        user = UserRegistration.objects.filter(ism__iexact=ism, familya__iexact=familya).first()

        if user and check_password(password, user.password):
            request.session['is_registered'] = True
            request.session['registered_email'] = user.email
            request.session['registered_name'] = f"{user.ism} {user.familya}"
            messages.success(request, f"Xush kelibsiz, {user.ism}!")
            return redirect('home')
        else:
            messages.error(request, "Ism, familya yoki parol xato.")
            return redirect('login')

    return render(request, 'login.html')



def logout_profile(request):
    request.session.flush() # Barcha session ma'lumotlarini tozalash
    messages.success(request, "Tizimdan chiqdingiz.")
    return redirect('home')


def contact_submit(request):
    """ Contact formini database'ga saqlash """
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([full_name, email, message]):
            messages.error(request, "Barcha maydonlarni to'ldiring.")
            return redirect(reverse('home') + '#contact')

        try:
            ContactMessage.objects.create(
                full_name=full_name,
                email=email,
                message=message
            )
            messages.success(request, "✓ Xabaringiz yuborildi. Tez orada javob keladi!")
        except Exception as e:
            messages.error(request, "Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")

        return redirect(reverse('home') + '#contact')
    
    return redirect(reverse('home') + '#contact')