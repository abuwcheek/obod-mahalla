from django import forms
from .models import UserRegistration

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = ['ism', 'familya', 'email', 'nomer', 'rasm', 'jinsi']
        
        help_texts = {
            'email': "Agar email manzilingiz o'zingizda bo'lmasa, hisobingizni qayta tiklashning iloji yo'q!",
            'nomer': "Hozirda ishlab turgan faol raqamingizni kiriting.",
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        # Barcha fieldlarga Bootstrap klassi qo'shish (chiroyli chiqishi uchun)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


