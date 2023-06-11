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
            print('REGISTERING...')
            if form.is_valid():
                print('FORM IS VALID')
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
            team = models.Team.objects.get(pk=kwargs.get('team_pk'))
            context = {
                'team' : team,
            }
            return render(request, 'team.html', context=context)
        
class TradeLobby(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            trades = models.Trade.objects.all()
            context = {
                'trades': trades,
            }
            return render(request, 'trade_lobby.html', context=context)
        
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            if "create-trade" in request.POST:
                user_team = models.Team.objects.get(owner=request.user)
                trade_partner = models.Team.objects.get(name=request.POST.get('trade-partner'))
                new_trade = models.Trade.objects.create(
                    team_one=user_team,
                    team_two=trade_partner,
                )
                new_trade.save()
                return redirect('trade-room', trade_pk=new_trade.pk)
            return redirect('trade')

class TradeRoom(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            trade = models.Trade.objects.get(pk=kwargs.get('trade_pk'))
            team_one_picks = models.Pick.objects.filter(current_owner=trade.team_one)
            team_two_picks = models.Pick.objects.filter(current_owner=trade.team_two)
            context = {
                'trade': trade,
                'team_one_picks': team_one_picks,
                'team_two_picks': team_two_picks,
            }
            return render(request, 'trade_room.html', context=context)
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            trade = models.Trade.objects.get(pk=kwargs.get('trade_pk'))
            if "delete-trade" in request.POST:
                trade.delete()
                return redirect('trade-lobby')
            elif "add-pick" in request.POST:
                pick = request.POST.get('pick')
                pick = models.Pick.objects.get(pk=int(pick))
                if pick.current_owner == trade.team_one:
                    trade.team_one_sends.add(pick)
                elif pick.current_owner == trade.team_two:
                    trade.team_two_sends.add(pick)
                trade.save()
            elif "remove-pick" in request.POST:
                pick = request.POST.get('pick')
                pick = models.Pick.objects.get(pk=int(pick))
                if pick.current_owner == trade.team_one:
                    trade.team_one_sends.remove(pick)
                elif pick.current_owner == trade.team_two:
                    trade.team_two_sends.remove(pick)
                trade.save()

            elif "propose" in request.POST:
                trade.status = "PROPOSED"
                trade.team_one_accepted = True
                trade.save()

            elif "cancel" in request.POST:
                trade.status = "CANCELLED"
                trade.delete()
                return redirect('trade-lobby')
            
            return redirect('trade-room', trade_pk=trade.pk)

class Draftboard(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            picks_2023 = models.Pick.objects.filter(year=2023).order_by('round', 'number')
            context = {
                'picks': picks_2023,
            }
            return render(request, 'draftboard.html', context=context)