from django.shortcuts import render , redirect , HttpResponseRedirect
from GGez_App.models import *
from django.views import View
from django.contrib import messages
from GGez_App import views

class CheckOut(View):
    
    def post(self , request):
        return views.Checkout(request);
    
    def get(self, request):
        if request.session.get('carrito') == None:
            return HttpResponseRedirect(f'/carrito/')
        else:
            return render(request, 'carrito.html')