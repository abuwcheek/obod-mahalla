from django.urls import path
from .views import home, register, profile, logout_profile, login_request, edit_profile, create_elon, create_sorovnoma, vote, contact_submit


urlpatterns = [
    path('', home, name='home'),
    
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', login_request, name='login'),
    path('logout/', logout_profile, name='logout'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    path('elon/create/', create_elon, name='create_elon'),
    path('sorovnoma/create/', create_sorovnoma, name='create_sorovnoma'),
    path('vote/<int:poll_id>/', vote, name='vote'),
    path('contact/submit/', contact_submit, name='contact_submit'),
]
