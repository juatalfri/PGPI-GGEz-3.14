from django import template
register = template.Library ()

@register.filter (name='hay_en_stock')
def hay_en_stock(juego):
    if juego.cantidad == 0:
        return False
    else:
        return True
