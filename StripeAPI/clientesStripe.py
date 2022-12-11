import stripe

def create_customer(cliente):
    clienteStripe = stripe.Customer.create(
        address={"city": cliente.datosEnvio.ciudad,
                 "postal_code": cliente.datosEnvio.codigoPostal,
                 "line1": cliente.datosEnvio.direccion,
                 "state": cliente.datosEnvio.pais + ", " + cliente.datosEnvio.provincia},
        email=cliente.correo,
        payment_method = "pm_card_visa",
        name=cliente.nombre,
        phone = cliente.telefono,
        invoice_settings={"default_payment_method": "pm_card_visa"},
    )
    cliente.clienteStripeId = clienteStripe.id
    cliente.save()
    return clienteStripe