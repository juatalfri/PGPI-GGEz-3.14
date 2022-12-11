from django.shortcuts import render , redirect , HttpResponseRedirect
from GGez_App.models import *
from django.views import View
from django.contrib import messages
from GGez_App import views, carrito
from StripeAPI import cargos, clientesStripe, tarjetas
from GGez_App.signup import Signup
from pickle import NONE, FALSE, TRUE
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
        contrareembolsoAux = postData.get('cash')
        if contrareembolsoAux == "on":
            contrareembolsoAux = True
        else:
            contrareembolsoAux = False
        listaErrores = []
        if not contrareembolsoAux:
            if len(numeroTarjetaAux) != 16:
                mensajeError = "Debe introducir un número válido de tarjeta (sin separar por espacios)"
                listaErrores.append(mensajeError)
            if len(fechaCaducidadAux) != 6 or (0 > int(fechaCaducidadAux[0:2:1]) > 32) or (0 > int(fechaCaducidadAux[2:4:1]) > 13) or (int(fechaCaducidadAux[4:6:1]) < 10):
                mensajeError = "La fecha de caducidad debe seguir el siguiente formato 'ddmmyy' de una fecha válida (los dos dígitos del día y del mes y los dos últimos dígitos del año)"
                listaErrores.append(mensajeError)
            if len(codigoSeguridadAux) != 3:
                mensajeError = "Debe introducir un código de seguridad válido de una tarjeta"
                listaErrores.append(mensajeError)
            if self.datosVaciosEnvio(request):
                mensajeError = self.datosEnvioVaciosError(request)
                listaErrores.append(mensajeError)
        if len(listaErrores) != 0:
            return render(request, 'checkOut.html', {'errores':listaErrores, 'precioTotalCarrito':precioTotal, 'noCliente':True})
        localizadorAux = random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+random.choice(string.ascii_letters)+'-'+str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
        
        #Registro cliente
        # si el cliente no está registrado, cliente = anónimo    
        if cliente==None:
            cliente = clienteAnonimo()
            datosEnvioAux = DatosEnvio.objects.create(direccion = direccionAux,
                                ciudad = ciudadAux,
                                codigoPostal = codigoPostalAux,   
                                provincia = provinciaAux,
                                pais = paisAux)
            cliente.datosEnvio = datosEnvioAux
            if not contrareembolsoAux and self.datosVaciosPago(request):
                mensajeError = self.datosPagoVaciosError(request)
                listaErrores.append(mensajeError)
                return render(request, 'checkOut.html', {'errores': listaErrores, 'noCliente':True, 'precioTotalCarrito':precioTotal})
            elif not contrareembolsoAux and not self.datosVaciosPago(request):
                datosPagoAux = DatosPago.objects.create(numeroTarjeta = numeroTarjetaAux,
                                fechaCaducidad = fechaCaducidadAux,
                                codigoSeguridad = codigoSeguridadAux)
                cliente.datosPago = datosPagoAux
                
                clientesStripe.create_customer(cliente)
                tarjeta = tarjetas.create_card(cliente, numeroTarjetaAux, int("20"+fechaCaducidadAux[4:6:1]), int(fechaCaducidadAux[2:4:1]), codigoSeguridadAux)
                cargos.create_charge(precioTotal, cliente, tarjeta)
                
            pedido = Pedido.objects.create(cliente=cliente, precio=precioTotal, direccion="calle: " + direccionAux + ", ciudad: " + ciudadAux
                            + ", código postal: " + codigoPostalAux + ", provincia: " + provinciaAux + ", pais: " + paisAux, telefono=cliente.telefono, 
                            localizador=localizadorAux, contrareembolso=contrareembolsoAux)
            pedido.juegos.set(juegosAux)
            pedido.save()
        else:
            cliente = Cliente.getClientePorId(request.session.get("cliente"))
            datosEnvioAux = DatosEnvio.objects.create(direccion = direccionAux,
                                       ciudad = ciudadAux,
                                       codigoPostal = codigoPostalAux,   
                                       provincia = provinciaAux,
                                       pais = paisAux)
            cliente.datosEnvio = datosEnvioAux
            if not contrareembolsoAux and self.datosVaciosPago(request):
                    mensajeError = self.datosPagoVaciosError(request)
                    listaErrores.append(mensajeError)
                    return render(request, 'checkOut.html', {'errores': listaErrores, 'noCliente':True, 'precioTotalCarrito':precioTotal})
            elif not contrareembolsoAux and not self.datosVaciosPago(request):
                    datosPagoAux = DatosPago(numeroTarjeta = numeroTarjetaAux,
                                    fechaCaducidad = fechaCaducidadAux,
                                    codigoSeguridad = codigoSeguridadAux)
                    cliente.datosPago = datosPagoAux
                    
                    clientesStripe.create_customer(cliente)
                    tarjeta = tarjetas.create_card(cliente, numeroTarjetaAux, int("20"+fechaCaducidadAux[4:6:1]), int(fechaCaducidadAux[2:4:1]), codigoSeguridadAux)
                    cargos.create_charge(precioTotal, cliente, tarjeta)
                    
            pedido = Pedido.objects.create(cliente=cliente, precio=precioTotal, direccion="calle: " + direccionAux + ", ciudad: " + ciudadAux
               + ", código postal: " + codigoPostalAux + ", provincia: " + provinciaAux + ", pais: " + paisAux, telefono=cliente.telefono, 
                    localizador=localizadorAux, contrareembolso=contrareembolsoAux)
            pedido.juegos.set(juegosAux)
            pedido.save()
            if postData.get('updateDataBase'):
                cliente.save()
                
            if postData.get('notPersistDataBase'):
                cliente.datosEnvio = None
                cliente.datosPago  = None
                cliente.save()
                
        for j, c in carritoAux.items():
            cantidadPedidoAux = cantidadPedido.objects.create(juego=Juego.getJuegoPorId(j).get(), cantidad=c, pedido=pedido)
            cantidadPedidoAux.save()
                         
        for juego in juegosAux:
            cantidadComprada = cantidad_carrito(juego, carritoAux)
            juego.cantidad = juego.cantidad - cantidadComprada
            juego.save(update_fields=['cantidad'])
        
        request.session['carrito'] = {}
        message = "Su pedido se ha realizado correctamente copie el siguiente localizador para revisar su estado: " + localizadorAux
        return render(request, 'inicio.html', {'message': message})
        
    
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
            return render(request, 'checkOut.html', {'cliente' : cliente, 'noCliente': False, 'precioTotalCarrito':precioTotal})
        else:
            return render(request, 'checkOut.html', {'noCliente': True, 'precioTotalCarrito':precioTotal})
    def datosVaciosPago(self, request):
        postData = request.POST
        #Datos de pago
        numeroTarjetaAux = postData.get('numeroTarjeta')
        fechaCaducidadAux = postData.get('fechaCaducidad')
        codigoSeguridadAux = postData.get('codigoSeguridad')
        if  numeroTarjetaAux == '' or fechaCaducidadAux == '' or codigoSeguridadAux == '':
            return True
        else:
            return False
    def datosVaciosEnvio(self, request):
        postData = request.POST
        #Datos de envío
        direccionAux = postData.get('direccion')
        ciudadAux = postData.get('ciudad')
        codigoPostalAux = postData.get('codigoPostal')
        provinciaAux = postData.get('provincia')
        paisAux = postData.get('pais')
        if  direccionAux == '' or ciudadAux == '' or codigoPostalAux == '' or provinciaAux == '' or paisAux == '':
            return True
        else:
            return False
    def datosEnvioVaciosError(self, request):
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
        codigoSeguridadAux = postData.get('codigoSeguridad')
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
        mensajeError= "No puedes dejar el/los siguiente/s campo/s en blanco: " + mensajeError 
        return mensajeError
    def datosPagoVaciosError(self, request):
        mensajeError = ''
        postData = request.POST
        numeroTarjetaAux = postData.get('numeroTarjeta')
        fechaCaducidadAux = postData.get('fechaCaducidad')
        codigoSeguridadAux = postData.get('codigoSeguridad')
        if numeroTarjetaAux == '':
            mensajeError = mensajeError + "Número de tarjeta, "
        if fechaCaducidadAux == '':
            mensajeError = mensajeError + "Fecha de caducidad de la tarjeta, "
        if codigoSeguridadAux == '':
            mensajeError = mensajeError + "Código de seguridad de la tarjeta"
        mensajeError= "No puedes dejar el/los siguiente/s campo/s en blanco: " + mensajeError 
        return mensajeError