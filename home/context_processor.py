from .models import Home, ContactUs


def index_processor(request):
     contact_us = ContactUs.objects.all().first()

     context={

          'contact_us': contact_us,
     }
     return context