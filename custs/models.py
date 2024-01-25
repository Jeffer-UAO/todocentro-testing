from django.db import models

class Tercero(models.Model):    
    name = models.CharField(max_length=20, verbose_name=(u'Nombre'))

    class Meta:
        verbose_name = "Tercero"
        verbose_name_plural = "Terceros"

    def __str__(self):
        return str(self.name)