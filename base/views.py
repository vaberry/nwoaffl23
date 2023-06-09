from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.base import View
from dotenv import load_dotenv
from . import forms
from . import models
import os

load_dotenv()

class Login(LoginView):
    template_name = 'registration/login.html' 

class Register(View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            if request.user.is_authenticated:
                return redirect('home')
            else:
                context = {
                    'form': forms.RegistrationForm()
                }
                return render(request, 'registration/register.html', context=context)
        
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = forms.RegistrationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                if User.objects.filter(email=email).exists():
                    form.add_error('email', 'This email is already registered.')
                else:
                    user = form.save()
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(request=request, username=user.username, password=raw_password)
                    login(request, user)
            return redirect('home')

class Home(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            return render(request, 'home.html')
        
class Commissioner(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            create_team_form = forms.TeamCreationForm()
            teams = models.Team.objects.all()
            context = {
                'create_team_form': create_team_form,
                'teams': teams,
            }
            return render(request, 'commissioner.html', context=context)
        
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if "create-team" in request.POST:
                create_team_form = forms.TeamCreationForm(request.POST, request.FILES)
                if create_team_form.is_valid():
                    create_team_form.save()
                else:
                    create_team_form = forms.TeamCreationForm()
            elif "update-draft-order" in request.POST:
                pass
        return redirect('commissioner')

class Team(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            context = {
                'team_pk' : kwargs.get('team_pk'),
            }
            return render(request, 'team.html', context=context)
        
class Trade(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            return render(request, 'trade.html')