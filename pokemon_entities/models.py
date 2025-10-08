from django.db import models  # noqa F401
import datetime

class Pokemon(models.Model):
    title = models.CharField(max_length=50)
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
            return self.title_ru
        
class PokemonEntity(models.Model):
    Pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                verbose_name="Покемон")
    Lat = models.FloatField(verbose_name="Широта")
    Lon = models.FloatField(verbose_name="Долгота")
    Appeared_at = models.DateTimeField(verbose_name="Появится в:",
                                       default=datetime.datetime.now)
    Disappeared_at = models.DateTimeField(verbose_name="Исчезнет в:",
                                          default=datetime.datetime.now)
    Level = models.IntegerField(verbose_name="Уровень", default=0, null=True, blank=True)
    Health = models.IntegerField(verbose_name="Здоровье", default=0, null=True, blank=True)
    Strength = models.IntegerField(verbose_name="Сила", default=0, null=True, blank=True)
    Defence = models.IntegerField(verbose_name="Защита", default=0, null=True, blank=True)
    Stamina = models.IntegerField(verbose_name="Выносливость", default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.Pokemon.title_ru} {self.Level}"
