from django.db import models  # noqa F401
import datetime


class Pokemon(models.Model):
    title_ru = models.CharField(verbose_name="Название на русском",
                                max_length=200, null=True, blank=True)
    title_en = models.CharField(verbose_name="Название на английском",
                                max_length=200)
    title_jp = models.CharField(verbose_name="Название на японском",
                                max_length=200, null=True, blank=True)
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
