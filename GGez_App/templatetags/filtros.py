from django import template

register = template.Library()

@register.filter(name='divisa')
def divisa(number):
    return str(number) + "€"



@register.filter(name='multiplicar')
def multiplicar(number , number1):
    return number * number1

