from django.db import models

from .discipline import Discipline


class Clan(models.Model):
    """
        Vampire characters belong to one of the Vampire Clans. 
        This class keeps track of them.
        
        This is meta information which belongs to the VTM setting,
        rather than any particular Chronicle. 
    """

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