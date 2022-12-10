import stripe

def create_charge(cantidad, cliente, tarjeta):
    return stripe.Charge.create(
            amount=cantidad,
            currency='EUR',
            customer=cliente.clienteStripeId,
            source=tarjeta.card_id,
        )