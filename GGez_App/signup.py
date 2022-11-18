'''
Created on 17 nov 2022

@author: andres
'''

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from GGez_App.models import *
from django.views import View

class Signup (View):
    def get(self, request):
        return render(request, 'signup.html')
  
    def post(self, request):
        postData = request.POST
        nombre = postData.get('nombre')
        apellidos = postData.get('apellidos')
        telefono = postData.get('telefono')
        correo = postData.get('correo')
        contrasena = postData.get('contrasena')
        nombreUsuario = postData.get('nombreUsuario')
        # validation
        value = {
            'nombre': nombre,
            'apellidos': apellidos,
            'telefono': telefono,
            'correo': correo,
            'nombreUsuario': nombreUsuario
        }
        
        mensajeError = None
  
        cliente = Cliente(nombre=nombre,
                            apellidos=apellidos,
                            telefono=telefono,
                            correo=correo,
                            contrasena=contrasena,
                            nombreUsuario=nombreUsuario)
        mensajeError = self.validarCliente(cliente)
  
        if not mensajeError:
            cliente.registro()
            return redirect('inicio')
        else:
            data = {
                'error': mensajeError,
                'values': value
            }
            return render(request, 'signup.html', data)
  
    def validarCliente(self, cliente):
        mensajeError = None
        if (not cliente.nombre):
            mensajeError = "Introduce tu nombre"
        elif len(cliente.apellidos) < 3:
            mensajeError = 'El nombre debe tener al menos 3 caracteres'
        elif not cliente.apellidos:
            mensajeError = 'Introduce tus apellidos'
        elif len(cliente.apellidos) < 3:
            mensajeError = 'Los apellidos deben tener al menos 3 caracteres'
        elif not cliente.telefono:
            mensajeError = 'Introduce tu teléfono'
        elif len(cliente.telefono) < 9:
            mensajeError = 'El telefono debe tener al menos 9 digitos'
        elif len(cliente.contrasena) < 5:
            mensajeError = 'La contraseña debe tener al menos 5 caracteres'
        elif len(cliente.correo) < 5:
            mensajeError = 'Correo debe tener más de 5 caracteres'
        elif not cliente.nombreUsuario:
            mensajeError = 'Introduce tu nombre de usuario'
        elif cliente.existe():
            mensajeError = 'Nombre de usuario ya registrado.'
  
        return mensajeError