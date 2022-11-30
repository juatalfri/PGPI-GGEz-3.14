from django.db import models
from unittest.util import _MAX_LENGTH
from django.template.defaultfilters import default
from django.utils import timezone
from django.db.models import Q


class Categoria(models.Model):
    categoria = models.CharField(max_length=50, unique = True, verbose_name='categoría')
    def __str__(self):
        return self.categoria
    
    @staticmethod
    def getTodasCategorias():
        return Categoria.objects.all()
    
class Juego(models.Model):
    
    PEGI3 = 3
    PEGI7 = 7
    PEGI12 = 12
    PEGI16 = 16
    PEGI18 = 18
    
    CHOICES = ((PEGI3, PEGI3),
               (PEGI7, PEGI7),
               (PEGI12, PEGI12),
               (PEGI16, PEGI16),
               (PEGI18, PEGI18))
    
    titulo = models.CharField(max_length=50, unique = True, verbose_name='título')
    descripcion = models.TextField(help_text='Añade una descripción del juego', verbose_name='descripción')
    desarrollador = models.CharField(max_length=50)
    precio = models.FloatField()
    caratula = models.ImageField(upload_to= 'caratulas', verbose_name='carátula')
    cantidad = models.IntegerField()
    categoria = models.ManyToManyField(Categoria)
    pegi = models.IntegerField(choices=CHOICES)
    
    def __str__(self):
        return self.titulo
    
    @staticmethod
    def getJuegoPorId(idJuego):
        return Juego.objects.filter(id=idJuego)
    @staticmethod
    def getJuegosPorId(ids):
        return Juego.objects.filter(id__in=ids)
    
    @staticmethod
    def getTodosJuegos():
        return Juego.objects.all()
    
    @staticmethod
    def getTodosJuegosPorCategoria(categoriaId):
        if categoriaId:
            return Juego.objects.filter(categoria=categoriaId)
        else:
            return Juego.getTodosJuegos();
        
    @staticmethod        
    def getJuegoBusqueda(categoriaId, texto):
        if categoriaId:
            return Juego.objects.filter(Q(categoria=categoriaId) & Q(titulo__contains=texto) | Q(desarrollador__contains=texto))
        else:
            return Juego.objects.filter(Q(titulo__contains=texto) | Q(desarrollador__contains=texto));

    @staticmethod
    def getJuegosPrecio(minimo,maximo):
        print(minimo)
        if minimo == '':
            minimo = 0.01
            print(minimo)
        print(maximo)
        if maximo == '':
            maximo = 999999.99
            print(maximo)
        return Juego.objects.filter(precio__range=(minimo,maximo))

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    nombreUsuario = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField()
    contrasena = models.CharField(max_length=20)
    
    def registro(self):
        self.save()
        
    def __str__(self):
        return self.nombreUsuario
    
    def existe(self):
        if Cliente.objects.filter(nombreUsuario=self.nombreUsuario):
            return True
  
        return False
    
    @staticmethod
    def getClientePorNombreUsuario(nombreUsuario):
        try:
            return Cliente.objects.get(nombreUsuario=nombreUsuario)
        except:
            return False
    
class Pedido(models.Model):
    
    PENDIENTE = 'Pendiente'
    EN_REPARTO = 'En reparto'
    ENTREGADO = 'Entregado'
    CANCELADO = 'Pedido cancelado'
    
    CHOICES = ((PENDIENTE, PENDIENTE),
               (EN_REPARTO, EN_REPARTO),
               (ENTREGADO, ENTREGADO),
               (CANCELADO, CANCELADO))
    
    estado = models.CharField(choices=CHOICES, max_length=50, default=PENDIENTE)
    juegos = models.ManyToManyField(Juego)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    precio = models.FloatField()
    fecha = models.DateField(default=timezone.now)
    direccion = models.CharField(max_length=50, default='', blank=True)
    telefono = models.CharField(max_length=50, default='', blank=True)
    localizador = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.localizador
    
    def hacerPedido(self):
        self.save()
        
    @staticmethod
    def getPedidoPorLocalizador(localizadorPedido):
        return Pedido.objects.filter(localizador=localizadorPedido)
        
    @staticmethod
    def getCantidadPedido(idPedido):
        return cantidadPedido.objects.filter(pedido=idPedido)
    
class cantidadPedido(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.juego.titulo + ": " + str(self.cantidad)
    
    def crearTablaCantidadPedido(self):
        self.save()