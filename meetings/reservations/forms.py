from django import forms
from .models import Rooms


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data['title']
        if Rooms.objects.filter(title=title).exists():
            raise forms.ValidationError("This title is already exists, please choose another one")
        return title