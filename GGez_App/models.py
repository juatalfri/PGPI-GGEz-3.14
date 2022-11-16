from django.db import models

# Create your models here.
class Juego(models.Model):
    titulo = models.CharField(max_length=50, unique = True, verbose_name='título')
    descripcion = models.TextField(help_text='Añade una descripción del juego', verbose_name='descripción')
    precio = models.FloatField()
    caratula = models.ImageField(upload_to= 'caratulas', verbose_name='carátula')
    genero = models.TextField(verbose_name='género')
    def __unicode__(self):
        return self.titulo