from django.shortcuts import render , redirect , HttpResponseRedirect
from GGez_App.models import *
from django.views import View
from django.contrib import messages
from GGez_App import views, carrito
from StripeAPI import *
from GGez_App.signup import Signup
from pickle import NONE, FALSE
from numpy.random.mtrand import randint
import random
import string
from GGez_App.templatetags import carrito
from GGez_App.templatetags.carrito import precio_total
from GGez_App.views import clienteAnonimo
from GGez_App.templatetags.carrito import cantidad_carrito



class CheckOut(View):
    
    def post(self , request):
        mensajeError = None
        cliente = request.session.get("cliente")
        carritoAux = request.session.get('carrito')
        ids = carritoAux.keys()
        juegosAux = Juego.getJuegosPorId(ids)
        precioTotal = carrito.precio_total_carrito(juegosAux, carritoAux)

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
        codigoSeguridadAux = postData.get('codigoSeguridad')
        
        localizadorAux = random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+'-'+str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
        
        #Registro cliente
        # si el cliente no está registrado, cliente = anónimo    
        if cliente==None:
            cliente = clienteAnonimo()
            if self.datosVacios(request):
                mensajeError = self.datosVaciosError(request)
                return render(request, 'checkOut.html', {'error': mensajeError, 'noCliente': True})                
            else:
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
                
            pedido = Pedido.objects.create(cliente=cliente, precio=precioTotal, direccion="calle: " + direccionAux + ", ciudad: " + ciudadAux
                                + ", código postal: " + codigoPostalAux + ", provincia: " + provinciaAux + ", pais: " + paisAux, telefono=cliente.telefono, 
                                localizador=localizadorAux)
            pedido.juegos.set(juegosAux)
            pedido.save()
                
        else:
            
            cliente = Cliente.getClientePorId(request.session.get("cliente"))
            datosEnvioAux = DatosEnvio.objects.create(direccion = direccionAux,
                                       ciudad = ciudadAux,
                                       codigoPostal = codigoPostalAux,   
                                       provincia = provinciaAux,
                                       pais = paisAux)
            
            datosPagoAux = DatosPago.objects.create(numeroTarjeta = numeroTarjetaAux,
                                     fechaCaducidad = fechaCaducidadAux,
                                     codigoSeguridad = codigoSeguridadAux)
            cliente.datosEnvio = datosEnvioAux
            cliente.datosPago = datosPagoAux
            pedido = Pedido.objects.create(cliente=cliente, precio=precioTotal, direccion="calle: " + direccionAux + ", ciudad: " + ciudadAux
               + ", código postal: " + codigoPostalAux + ", provincia: " + provinciaAux + ", pais: " + paisAux, telefono=cliente.telefono, 
                    localizador=localizadorAux)
            pedido.juegos.set(juegosAux)
            pedido.save()

            if postData.get('persist'):
                cliente.save()
                
            if postData.get('notPersistDataBase'):
                cliente.datosEnvio = None
                cliente.datosPago  = None
                cliente.save()
                
                
        for juego in juegosAux:
            cantidadComprada = cantidad_carrito(juego, carritoAux)
            juego.cantidad = juego.cantidad - cantidadComprada
            juego.save(update_fields=['cantidad'])
        
        request.session['carrito'] = {}
        return render(request, 'inicio.html')
        
    
    def get(self, request):
        idCliente = request.session.get('cliente')
        cliente = Cliente.getClientePorId(idCliente)
        carritoAux = request.session.get('carrito')
        ids = carritoAux.keys()
        juegosAux = Juego.getJuegosPorId(ids)
        precioTotal = carrito.precio_total_carrito(juegosAux, carritoAux)
        if request.session.get('carrito') == None:
            return HttpResponseRedirect(f'/carrito/')
        elif cliente or cliente==clienteAnonimo() and request.session.get('carrito'):
            return render(request, 'checkOut.html', {'cliente' : cliente, 'noCliente': False, 'precioTotal':precioTotal})
        else:
            return render(request, 'checkOut.html', {'noCliente': True, 'precioTotal':precioTotal})
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
        if  direccionAux == '' or ciudadAux == '' or codigoPostalAux == '' or provinciaAux == '' or paisAux == '' or numeroTarjetaAux == '' or fechaCaducidadAux == '':
            return True
        else:
            return False
    def datosVaciosError(self, request):
        mensajeError = ''
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
        if direccionAux == '':
            mensajeError = mensajeError + "Dirección, "
        if ciudadAux == '':
            mensajeError = mensajeError + "Ciudad, "
        if codigoPostalAux == '':
            mensajeError = mensajeError + "Código postal, "
        if provinciaAux == '':
            mensajeError = mensajeError + "Provincia, "
        if paisAux == '':
            mensajeError = mensajeError + "País, "
        if numeroTarjetaAux == '':
            mensajeError = mensajeError + "Número de tarjeta, "
        if fechaCaducidadAux == '':
            mensajeError = mensajeError + "Fecha de caducidad de la tarjeta"
        mensajeError= "No puedes dejar este campo/s en blanco: " + mensajeError 
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
        