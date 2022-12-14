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
                'errores': mensajeError,
                'values': value
            }
            return render(request, 'signup.html', data)
  
    def validarCliente(self, cliente, contrasena, contrasena2):
        listaErrores=[]
        if not cliente.nombre:
            listaErrores.append("Introduce tu nombre.")
        if len(cliente.nombre) < 3:
            listaErrores.append("El nombre debe tener al menos 3 caracteres.")
        if not cliente.apellidos:
            listaErrores.append("Introduce tus apellidos.")
        if len(cliente.apellidos) < 3:
            listaErrores.append("Los apellidos deben tener al menos 3 caracteres.")
        if not cliente.telefono:
            listaErrores.append("Introduce tu tel??fono.")
        if len(cliente.telefono) < 9:
            listaErrores.append("El telefono debe tener al menos 9 digitos.")
        if len(cliente.contrasena) < 5:
            listaErrores.append("La contrase??a debe tener al menos 5 caracteres.")
        if contrasena != contrasena2:
            listaErrores.append("Las contrase??as deben ser iguales.")
        if len(cliente.correo) < 5:
            listaErrores.append("El correo debe tener m??s de 5 caracteres.")
        if not cliente.nombreUsuario:
            listaErrores.append("Introduce tu nombre de usuario.")
        if cliente.existe():
            listaErrores.append("Nombre de usuario ya registrado.")
  
        return listaErrores