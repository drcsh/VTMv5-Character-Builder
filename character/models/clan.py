from django.db import models


class Clan(models.Model):

    name = models.CharField()
    description = models.TextField()
    bane = models.TextField
    
    #Todo: discipline association
    #Todo: Add insignias?

    class Meta:
        ordering = ["name"]
        verbose_name = "Vampire Clan"
        verbose_name_plural = "Vampire Clans"