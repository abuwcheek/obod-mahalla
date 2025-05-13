from django.shortcuts import render
from .models import Home, ContactUs




def home(request):
     home_objects = Home.objects.all()
     contact_us = ContactUs.objects.all()
     context = {
          'home_objects': home_objects,
          'contact_us': contact_us,
     }
     return render(request, 'index.html', context)