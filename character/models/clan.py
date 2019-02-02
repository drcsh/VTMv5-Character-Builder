from django.db import models

from .discipline import Discipline

class Clan(models.Model):

    name = models.CharField()
    description = models.TextField()
    bane = models.TextField

    disciplines = models.ManyToManyField(
        Discipline,
        related_name="clans"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Vampire Clan"
        verbose_name_plural = "Vampire Clans"