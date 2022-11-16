from django.shortcuts import render
from GGez_App.models import *
# Create your views here.
def catalogo(request):
    juegos = Juego.objects.all()
    return render(request,'catalogo.html',{'catalogo':juegos})