from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.views import View
from .models import  Home, ContactUs




def home(request):
     first_news = Home.objects.filter(is_active=True).order_by('?')[1]
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

