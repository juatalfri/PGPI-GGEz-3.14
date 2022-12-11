import stripe

def create_card(cliente, numeroTarjeta, anyoExp, mesExp, codigoSeguridad):
        return stripe.Customer.create_source(cliente.clienteStripeId, source={'object':"card", 
                                                                              'number':numeroTarjeta,
                                                                              'exp_month':mesExp,
                                                                              'exp_year':anyoExp,
                                                                              'cvc':codigoSeguridad})