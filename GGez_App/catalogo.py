'''
Created on 18 nov 2022

@author: andres
'''

from django.shortcuts import render , redirect , HttpResponseRedirect
from GGez_App.models import *
from django.views import View

class Index(View):

    def post(self , request):
        juego = request.POST.get('juego')
        remove = request.POST.get('remove')
        carrito = request.session.get('carrito')
        if carrito:
            cantidad = carrito.get(juego)
            if cantidad:
                if remove:
                    if cantidad<=1:
                        carrito.pop(juego)
                    else:
                        carrito[juego]  = cantidad-1
                else:
                    carrito[juego]  = cantidad+1

            else:
                carrito[juego] = 1
        else:
            carrito = {}
            carrito[juego] = 1

        request.session['carrito'] = carrito
        return redirect('inicio')

    def get(self , request):
        return HttpResponseRedirect(f'/catalogo{request.get_full_path()[1:]}')

