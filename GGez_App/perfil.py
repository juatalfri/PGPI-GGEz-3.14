'''
Created on 5 dic 2022

@author: andres
'''
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from GGez_App.models import *
from django.views import View

class Perfil(View):
    return_url = None

    def get(self, request, idUsuario):
        cliente = Cliente.getClientePorId(idUsuario)
        return render (request, 'perfil.html', {'cliente' : cliente})

    # def post(self, request):
    #     nombreUsuario = request.POST.get ('nombreUsuario')
    #     contrasena = request.POST.get ('contrasena')
    #     cliente = Cliente.getClientePorNombreUsuario(nombreUsuario)
    #     mensajeError = None
    #     if cliente:
    #         flag = contrasena == cliente.contrasena
    #         if flag:
    #             request.session['cliente'] = cliente.id
    #
    #             if Login.return_url:
    #                 return HttpResponseRedirect(Login.return_url)
    #             else:
    #                 Login.return_url = None
    #                 return redirect ('inicio')
    #         else:
    #             mensajeError = 'Contraseña incorrecta'
    #     else:
    #         mensajeError = 'Nombre de usuario no existe'
    #
    #     return render (request, 'login.html', {'error': mensajeError})
