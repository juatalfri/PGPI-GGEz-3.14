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
        contrasena2 = postData.get('contrasena2')
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
  
        cliente = Cliente(
            nombre=nombre,
            apellidos=apellidos,
            telefono=telefono,
            correo=correo,
            contrasena=contrasena,
            nombreUsuario=nombreUsuario)
        mensajeError = self.validarCliente(cliente, contrasena, contrasena2)
  
        if not mensajeError:
            cliente.registro()
            return redirect('inicio')
        else:
            data = {
                'error': mensajeError,
                'values': value
            }
            return render(request, 'signup.html', data)
  
    def validarCliente(self, cliente, contrasena, contrasena2):
        mensajeError = ''
        if not cliente.nombre:
            mensajeError = mensajeError +  " |ERROR: Introduce tu nombre.|"
        if len(cliente.nombre) < 3:
            mensajeError = mensajeError + ' |ERROR: El nombre debe tener al menos 3 caracteres.|'
        if not cliente.apellidos:
            mensajeError = mensajeError + ' |ERROR: Introduce tus apellidos.'
        if len(cliente.apellidos) < 3:
            mensajeError = mensajeError + ' |ERROR: Los apellidos deben tener al menos 3 caracteres.|'
        if not cliente.telefono:
            mensajeError = mensajeError + ' |ERROR: Introduce tu teléfono.|'
        if len(cliente.telefono) < 9:
            mensajeError = mensajeError + ' |ERROR: El telefono debe tener al menos 9 digitos.|'
        if len(cliente.contrasena) < 5:
            mensajeError = mensajeError + ' |ERROR: La contraseña debe tener al menos 5 caracteres.|'
        if contrasena != contrasena2:
            mensajeError = mensajeError + ' |ERROR: Las contraseñas deben ser iguales.|'
        if len(cliente.correo) < 5:
            mensajeError = mensajeError + ' |ERROR: El correo debe tener más de 5 caracteres.|'
        if not cliente.nombreUsuario:
            mensajeError = mensajeError + ' |ERROR: Introduce tu nombre de usuario.|'
        if cliente.existe():
            mensajeError = mensajeError + ' |ERROR:  Nombre de usuario ya registrado.|'
  
        print(mensajeError)
        return mensajeError