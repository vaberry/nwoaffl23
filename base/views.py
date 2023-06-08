from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.
class Home(View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            return render(request, 'home.html')
        
class Commissioner(View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            return render(request, 'commissioner.html')
        
class Trade(View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            return render(request, 'trade.html')