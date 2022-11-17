from django.shortcuts import render
from GGez_App.models import *
# Create your views here.
def inicio(request):
    return render(request,'base.html')
    
def catalogo(request):
    juegos = Juego.objects.all()
    categorias = Categoria.objects.all()
    dic = {}
    for cat in categorias:
        dic[cat] = Juego.objects.filter(categoria = cat)
    return render(request,'catalogo.html',{'catalogo':juegos,'dic_categorias':dic})