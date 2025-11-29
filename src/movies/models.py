from django.db import models

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    height = models.FloatField(verbose_name='Altura')
    base_experience = models.IntegerField(verbose_name='experiencia base')