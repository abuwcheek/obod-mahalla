from django.urls import path
from .views import home, register, profile, logout_profile, login_request


urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', login_request, name='login'),
    path('logout/', logout_profile, name='logout'),
]
