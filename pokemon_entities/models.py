from django.db import models  # noqa F401
import datetime


class Pokemon(models.Model):
    title_ru = models.CharField(verbose_name="Название на русском",
                                max_length=200)
    title_en = models.CharField(verbose_name="Название на английском",
                                max_length=200)
    title_jp = models.CharField(verbose_name="Название на японском",
                                max_length=200, blank=True)
    image = models.ImageField(verbose_name="Изображение",
                              null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    previous_evolution = models.ForeignKey("self",
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           related_name='next_evolutions',
                                           verbose_name="Предыдущая эволюция",)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                verbose_name="Покемон",
                                related_name="pokemon_set")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name="Появится в:",
                                       default=datetime.datetime.now)
    disappeared_at = models.DateTimeField(verbose_name="Исчезнет в:",
                                          default=datetime.datetime.now)
    level = models.IntegerField(verbose_name="Уровень", default=None, null=True, blank=True)
    health = models.IntegerField(verbose_name="Здоровье", default=None, null=True, blank=True)
    strength = models.IntegerField(verbose_name="Сила", default=None, null=True, blank=True)
    defence = models.IntegerField(verbose_name="Защита", default=None, null=True, blank=True)
    stamina = models.IntegerField(verbose_name="Выносливость", default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.pokemon.title_ru} {self.level}"
