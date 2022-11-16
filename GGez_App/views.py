from django.shortcuts import render
from GGez_App.models import *
# Create your views here.
def catalogo(request):
    juegos = Juego.objects.all()
    categorias = []
    for j in juegos:
        cat = j.categoria
        if cat not in categorias:
            categorias.append(cat)
    return render(request,'catalogo.html',{'catalogo':juegos,'categorias':categorias})