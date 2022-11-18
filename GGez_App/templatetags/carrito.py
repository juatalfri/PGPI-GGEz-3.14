from django import template

register = template.Library ()


@register.filter (name='esta_en_el_carrito')
def esta_en_el_carrito(juego, carrito):
    keys = carrito.keys()
    for id in keys:
        if int(id) == juego.id:
            return True
    return False;


@register.filter (name='cantidad_carrito')
def cantidad_carrito(juego, carrito):
    keys = carrito.keys()
    for id in keys:
        if int(id) == juego.id:
            return carrito.get(id)
    return 0;


@register.filter (name='precio_total')
def precio_total(juego, carrito):
    return juego.precio * cantidad_carrito(juego, carrito)


@register.filter (name='precio_total_carrito')
def precio_total_carrito(juegos, carrito):
    sum = 0;
    for j in juegos:
        sum += precio_total(j, carrito)

    return sum
