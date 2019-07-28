from django.db import models


class Generation(models.Model):
    """
        Each vampire has a generation representing how many steps they are from the mythical Caine.

        Min generation is generally 3 and max is 16

        These have some flavour text and define the minimum and maximum blood potency of the vampire. 
    """

    value = models.PositiveSmallIntegerField()
    minimum_blood_potency = models.PositiveSmallIntegerField()
    maximum_blood_potency = models.PositiveSmallIntegerField()
    
    class Meta:
        ordering = ["value"]
        verbose_name = "Generation"
        verbose_name_plural = "Generations"