from django.shortcuts import render, redirect, HttpResponseRedirect
from GGez_App.models import *
from django.views import View
from django.contrib.auth.hashers import check_password
from GGez_App.templatetags import carrito
from GGez_App.templatetags.carrito import cantidad_carrito
import random
import string
from numpy.random.mtrand import randint
from django.core.mail import send_mail

# Create your views here.
def inicio(request):
    return render(request,'inicio.html')
    
def catalogo(request):
    carrito = request.session.get('carrito')
    if not carrito:
        request.session['carrito'] = {}
    juegos = None
    categorias = Categoria.getTodasCategorias()
    categoriaId = request.GET.get('categoria')
    busqueda = request.GET.get('searchbar')
    minimo = request.GET.get('min')
    maximo = request.GET.get('max')
    if busqueda:    
        juegos = Juego.getJuegoBusqueda(categoriaId,busqueda)
    elif ((minimo != None) | (maximo != None)):
        juegos = Juego.getJuegosPrecio(minimo,maximo)
    else:
        juegos = Juego.getTodosJuegosPorCategoria(categoriaId)
            
    data = {}
    data['juegos'] = juegos
    data['categorias'] = categorias
    data['busqueda'] = busqueda

    return render(request, 'catalogo.html', data)

def Carrito(request):
    carrito = request.session.get('carrito')
    if carrito:
        ids = list(request.session.get('carrito').keys())
        juegos = Juego.getJuegosPorId(ids)
    else:
        juegos= []
    carritoVacio = len(juegos)==0
    return render(request, 'carrito.html', {'juegos' : juegos, 'carritoVacio' : carritoVacio})

def Checkout(request):
    ids = list(request.session.get('carrito').keys())
    juegos = Juego.getJuegosPorId(ids)
    carritoAux = request.session.get('carrito')
    juegosAux = Juego.getJuegosPorId(list(carritoAux.keys()))
    direccionAux = request.POST.get('direccion')
    telefonoAux = request.POST.get('telefono')
    localizadorAux = random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+'-'+str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))

    if request.session.get('cliente') == None:
        clienteAux = clienteAnonimo()
    else:
        clienteAux = request.session.get('cliente')
  
    precioAux = carrito.precio_total_carrito(juegosAux, carritoAux)
    pedidoAux = Pedido.objects.create(cliente=clienteAux, precio=precioAux, direccion=direccionAux, telefono=telefonoAux, localizador = localizadorAux)
    pedidoAux.juegos.set(juegosAux)
    pedidoAux.save()
    
    for j, c in carritoAux.items():
        cantidadPedidoAux = cantidadPedido.objects.create(juego=Juego.getJuegoPorId(j).get(), cantidad=c, pedido=pedidoAux)
        cantidadPedidoAux.save()
    
    juegosConCantidadEmail = ''
    
    for juego in juegosAux:
        cantidadComprada = cantidad_carrito(juego, carritoAux)
        juego.cantidad = juego.cantidad - cantidadComprada
        juego.save(update_fields=['cantidad'])
        
        juegosConCantidadEmail += str(juego.titulo) + ' x' + str(cantidadComprada) + '\n'
    
    request.session['carrito'] = {}
    
    return render(request, 'checkOut.html', {'juegos' : juegos})

def pedido(request):
    localizador = request.GET.get('searchbarPedido')
    if localizador:
        if not Pedido.getPedidoPorLocalizador(localizador):
            mensajeError = "El localizador que ha introducido no corresponde a ning??n pedido registrado en nuestro sistema"
            return render(request, 'pedidos.html', {'error':mensajeError})
        else:
            pedido = Pedido.getPedidoPorLocalizador(localizador).get()
            relacion = list()
            cantidadPedido = Pedido.getCantidadPedido(pedido.id)
            for i in range(len(cantidadPedido)):
                relacion.append(cantidadPedido[i])
            return render(request, 'pedidos.html', {'relacion' : relacion, 'pedido': pedido})
    else:
        return render(request, 'pedidos.html')

def politicaEnvio(request):
    return render(request,'politicaEnvio.html')

def clienteAnonimo():
    if Cliente.getClientePorNombreUsuario('An??nimo') != False:
        return Cliente.getClientePorNombreUsuario('An??nimo')
    else:
        cliente = Cliente(nombre='An??nimo', apellidos='An??nimo', nombreUsuario='An??nimo', telefono='000000000', correo='an??nimo@gmail.com', contrasena='An??nimo')
        cliente.save()
        return cliente
    
def fichaJuego(request):
    juegoId = request.GET.get('juego')
    juego = Juego.getJuegoPorId(juegoId).get()
    return render(request, 'fichaJuego.html', {'juego' : juego})
        
def politicaPrivacidad(request):
    return render(request,'politicaPrivacidad.html')

def atencionCliente(request):
    return render(request,'atencionCliente.html')

def datosEmpresa(request):
    return render(request,'datosEmpresa.html')