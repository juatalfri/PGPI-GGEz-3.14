from django.shortcuts import render, redirect, HttpResponseRedirect
from GGez_App.models import *
from django.views import View
from django.contrib.auth.hashers import check_password
# Create your views here.
def inicio(request):
    return render(request,'base.html')
    
def catologo(request):
    carrito = request.session.get('carrito')
    if not carrito:
        request.session['carrito'] = {}
    juegos = None
    categorias = Categoria.getTodasCategorias()
    categoriaId = request.GET.get('categoria')
    if categoriaId:
        juegos = Juego.getTodosJuegosPorCategoria(categoriaId)
    else:
        juegos = Juego.getTodosJuegos();

    data = {}
    data['juegos'] = juegos
    data['categorias'] = categorias

    print('Eres : ', request.session.get('nombreUsuario'))
    return render(request, 'catalogo.html', data)

def Carrito(request):
    ids = list(request.session.get('carrito').keys())
    juegos = Juego.getJuegosPorId(ids)
    return render(request, 'carrito.html', {'juegos' : juegos})

def Checkout(request):
    carrito = request.session.get('carrito')
    juegos = Juego.getJuegosPorId(list(carrito.keys()))
    direccion = request.POST.get('direccion')
    telefono = request.POST.get('telefono')
    cliente = request.session.get('cliente')
    for juego in juegos:
        pedido = Pedido(cliente=Cliente(id=cliente), juego=juego, precio=juego.precio, direccion=direccion, telefono=telefono, cantidad=carrito.get(str(juego.id)))
        pedido.save()
    request.session['carrito'] = {}
    
    return redirect('carrito')

def Pedido(request):
    cliente = request.session.get('cliente')
    pedidos = Pedido.getPedidosPorCliente(cliente)
    return render(request, 'pedido.html', {'pedidos' : pedidos})
    

