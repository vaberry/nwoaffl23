from django import forms
from .models import Team
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TeamCreationForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Team
        fields = ['owner', 'name', 'commissioner', 'profile_picture', 'draft_order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs['accept'] = 'image/*'

    def save(self):
        team = super().save(commit=False)
        team.save()
        return team


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = '<span class="ms-4" style="color:lightgray;">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>'
        self.fields['password1'].help_text = '<span style="color:lightgray;"><ul><li>Your password cant be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password cant be a commonly used password.</li><li>Your password cant be entirely numeric.</li></ul></span>'
        self.fields['password2'].help_text = '<span class="ms-4" style="color:lightgray;">Enter the same password as before, for verification.</span>'

    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
