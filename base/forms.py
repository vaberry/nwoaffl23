from django import forms
from django.contrib.auth.models import User
from . import models

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = models.Team
        fields = ['name', 'commissioner', 'profile_picture', 'draft_order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs['accept'] = 'image/*'

    def save(self, owner):
        team = super().save(commit=False)
        team.owner = owner
        team.save()
        return team
