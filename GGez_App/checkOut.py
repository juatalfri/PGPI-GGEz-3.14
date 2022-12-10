from django.shortcuts import render , redirect , HttpResponseRedirect
from GGez_App.models import *
from django.views import View
from django.contrib import messages
from GGez_App import views
from StripeAPI import *
from GGez_App.signup import Signup
from pickle import NONE, FALSE
import random

class CheckOut(View):
    
    def post(self , request):
        mensajeError = None
        cliente = None
        ids = list(request.session.get('carrito').keys())
        juegosAux = Juego.getJuegosPorId(ids)
        postData = request.POST
        precioTotal = postData.get('precioTotal')
        #Datos de usuario
        nombreUsuarioAux = postData.get('nombreUsuario')
        nombreAux = postData.get('nombre')
        apellidosAux = postData.get('apellidos')
        telefonoAux = postData.get('telefono')
        correoAux = postData.get('correo')
        contrasenaAux = postData.get('contrasena')
        contrasenaAux2 = postData.get('contrasena2')
        #Datos de envío
        direccionAux = postData.get('direccion')
        ciudadAux = postData.get('ciudad')
        codigoPostalAux = postData.get('codigoPostal')
        provinciaAux = postData.get('provincia')
        paisAux = postData.get('pais')
        #Datos de pago
        numeroTarjetaAux = postData.get('numeroTarjeta')
        fechaCaducidadAux = postData.get('fechaCaducidad')
        codigoSeguridadAux = postData.get('codigoSeguridad')
        #Registro cliente
        if not self.datosRegistroVacios(request):
            cliente = Cliente(
                nombre=nombreAux,
                apellidos=apellidosAux,
                telefono=telefonoAux,
                correo=correoAux,
                contrasena=contrasenaAux,
                nombreUsuario=nombreUsuarioAux)
            mensajeError = Signup.validarCliente(cliente, contrasenaAux, contrasenaAux2)
            if not postData.get('notPersistDataBase') and mensajeError != None:
                return render(request, 'checkOut.html', {'error': mensajeError})
            else:
                cliente.registro()
        localizadorAux = None
        if self.datosVacios(request) and not postData.get('notPersistDataBase'):
            mensajeError = self.datosVaciosError(request)
            if mensajeError != None:
                mensajeError = "Si quiere persistir los datos y no está registrado, debe añadir al menos lo siguientes campos obligatorios: " + mensajeError
                return render(request, 'checkOut.html', {'error': mensajeError})
        if postData.get('notPersistDataBase') and cliente == None and not self.datosVacios(request):
            clienteAux = None
            if Cliente.getClientePorNombreUsuario("Anónimo") == None:
                clienteAux = views.clienteAnonimo()
            localizadorAux = "4n0n1m0" + random.randint(0, 99999999999) + random.randint(0, 99999999999) + random.randint(0, 99999999999) + random.randint(0, 99999999999)
            pedido = Pedido(juegos=juegosAux, cliene=clienteAux, precio=precioTotal, direccion="calle: " + direccionAux + ", ciudad: " + ciudadAux
                                + ", código postal: " + codigoPostalAux + ", provincia: " + provinciaAux + ", pais: " + paisAux, telefono=telefonoAux, 
                                localizador=localizadorAux)
            pedido.save()
            return render(request, 'inicio.html')
        elif postData.get('notPersistDataBase') and self.datosVacios(request):
            mensajeError = "Aunque no quiera persistir sus datos, los siguientes campos son obligatorios: " + self.datosVaciosError(request)
            return render(request, 'checkOut.html', {'error': mensajeError})
        if not postData.get('notPersistDataBase') and not self.datosVacios(request) and cliente != None:
            datosEnvioAux = DatosEnvio(direccion = direccionAux,
                                       ciudad = ciudadAux,
                                       codigoPostal = codigoPostalAux,   
                                       provincia = provinciaAux,
                                       pais = paisAux)
            datosPagoAux = DatosPago(numeroTarjeta = numeroTarjetaAux,
                                     fechaCaducidad = fechaCaducidadAux,
                                     codigoSeguridad = codigoSeguridadAux)
            cliente.datosEnvio = datosEnvioAux
            cliente.datosPago = datosPagoAux
            cliente.save(force_update=True)
            localizadorAux = nombreUsuarioAux[0:-1:3] + nombreAux[0:-1:3] + correoAux[0:-1:3] + codigoPostalAux[0:-1:2] + paisAux[0:2:1] + telefonoAux[0:-1:2] + telefonoAux[1:-1:2]
            pedido = Pedido(juegos=juegosAux, cliene=cliente, precio=precioTotal, direccion="calle: " + direccionAux + ", ciudad: " + ciudadAux
                                + ", código postal: " + codigoPostalAux + ", provincia: " + provinciaAux + ", pais: " + paisAux, telefono=telefonoAux, 
                                localizador=localizadorAux)
            clientesStripe.create_customer(cliente)
            tarjeta = tarjetas.create_card(cliente, numeroTarjetaAux, fechaCaducidadAux[3:-1:1], fechaCaducidadAux[0:2:1])
            cargos.create_charge(precioTotal, cliente, tarjeta)
            return render(request, 'inicio.html')
    
    def get(self, request, idUsuario):
        cliente = Cliente.getClientePorId(idUsuario)
        if request.session.get('carrito') == None:
            return HttpResponseRedirect(f'/carrito/')
        elif cliente and request.session.get('carrito'):
            return render(request, 'checkOut.html', {'cliente' : cliente, 'noCliente': False})
        else:
            return render(request, 'checkOut.html', {'noCliente': True})
    def datosVacios(self, request):
        postData = request.POST
        #Datos de envío
        direccionAux = postData.get('direccion')
        ciudadAux = postData.get('ciudad')
        codigoPostalAux = postData.get('codigoPostal')
        provinciaAux = postData.get('provincia')
        paisAux = postData.get('pais')
        #Datos de pago
        numeroTarjetaAux = postData.get('numeroTarjeta')
        fechaCaducidadAux = postData.get('fechaCaducidad')
        if  direccionAux == None or ciudadAux == None or codigoPostalAux == None or provinciaAux == None or paisAux == None or numeroTarjetaAux == None or fechaCaducidadAux == None:
            return True
        else:
            return False
    def datosVaciosError(self, request):
        mensajeError = None
        postData = request.POST
        #Datos de envío
        direccionAux = postData.get('direccion')
        ciudadAux = postData.get('ciudad')
        codigoPostalAux = postData.get('codigoPostal')
        provinciaAux = postData.get('provincia')
        paisAux = postData.get('pais')
        #Datos de pago
        numeroTarjetaAux = postData.get('numeroTarjeta')
        fechaCaducidadAux = postData.get('fechaCaducidad')
        if direccionAux == None:
            mensajeError = mensajeError + "Dirección, "
        if ciudadAux == None:
            mensajeError = mensajeError + "Ciudad, "
        if codigoPostalAux == None:
            mensajeError = mensajeError + "Código postal, "
        if provinciaAux == None:
            mensajeError = mensajeError + "Provincia, "
        if paisAux == None:
            mensajeError = mensajeError + "País, "
        if numeroTarjetaAux == None:
            mensajeError = mensajeError + "Número de tarjeta, "
        if fechaCaducidadAux == None:
            mensajeError = mensajeError + "Fecha de caducidad de la tarjeta"
        return mensajeError
    def datosRegistroVacios(self, request):
        postData = request.POST
        #Datos de usuario
        nombreUsuarioAux = postData.get('nombreUsuario')
        nombreAux = postData.get('nombre')
        apellidosAux = postData.get('apellidos')
        telefonoAux = postData.get('telefono')
        correoAux = postData.get('correo')
        contrasenaAux = postData.get('contrasena')
        contrasenaAux2 = postData.get('contrasena2')
        if nombreUsuarioAux != None or nombreAux != None or apellidosAux != None or telefonoAux != None or correoAux != None or contrasenaAux != None or contrasenaAux2 != None:
            return True
        else:
            return False
        