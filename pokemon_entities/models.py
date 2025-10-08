from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=50)
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
            return self.title_ru
        
class PokemonEntity(models.Model):
    Lat = models.FloatField(verbose_name="Широта")
    Lon = models.FloatField(verbose_name="Долгота")
