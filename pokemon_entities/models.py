from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=50)
    id = models.BigAutoField(primary_key=True)
