from django import forms
from .models import Rooms, Profile
from django.contrib.auth.models import User


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data['title']
        if Rooms.objects.filter(title=title).exists():
            raise forms.ValidationError(
                "This title is already exists, please choose another one")
        return title


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nuotrauka']
