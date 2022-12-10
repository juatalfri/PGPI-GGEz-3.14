import stripe

def create_card(cliente, numeroTarjeta, anyoExp, mesExp):
        return stripe.Customer.create_source(cliente.clienteStripeId, source="tok_mastercard")