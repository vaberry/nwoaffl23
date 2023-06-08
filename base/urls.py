from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
   path('', views.Home.as_view(), name='home'),
   path('commissioner/', views.Commissioner.as_view(), name='commissioner'),
    path('trade/', views.Trade.as_view(), name='trade'),
]