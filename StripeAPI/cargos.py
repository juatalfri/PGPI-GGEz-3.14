import stripe

def create_charge(cantidad, cliente, tarjeta):
    return stripe.Charge.create(
            amount=int(cantidad) * 100,
            currency='EUR',
            customer=cliente.clienteStripeId,
            source=tarjeta.id,
        )