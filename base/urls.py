from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
   path('', views.Home.as_view(), name='home'),
   path('commissioner/', views.Commissioner.as_view(), name='commissioner'),
   path('trade/', views.Trade.as_view(), name='trade'),
   path('team/<int:team_pk>/', views.Team.as_view(), name='team'),
   path('draftboard/', views.Draftboard.as_view(), name='draftboard'),
   
   path('login/', views.Login.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('register/', views.Register.as_view(), name='register'),
]