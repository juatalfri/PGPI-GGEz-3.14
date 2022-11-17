from django.db import models


class Categoria(models.Model):
    categoria = models.CharField(max_length=50, unique = True, verbose_name='categoría')
    def __str__(self):
        return self.categoria
    
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
    categoria = models.ManyToManyField(Categoria)
    pegi = models.IntegerField(choices=CHOICES)
    def __str__(self):
        return self.titulo
