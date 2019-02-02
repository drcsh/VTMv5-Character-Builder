from django.db import models

from .discipline import Discipline
from .character import Character

class DisciplinePower(models.Model):
    """
        This represents a power which a character has gained from one of their Disciplines.

        Note that this is left very generic for the players to fill out themselves. Ideally
        I'd make this much tighter and use the actual discipline list but Paradox/White Wolf
        would probably have a problem with me putting half the rulebook online :)
    """

    character = models.ForeignKey(
        Character, 
        related_name="powers",
        related_query_name="power", 
        on_delete=models.CASCADE
    )
    discipline = models.ForeignKey(
        Discipline, 
        on_delete=models.PROTECT
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    dice_pools = models.CharField(max_length=50)
    cost = models.TextField()
    system = models.TextField()
    duration = models.TextField()

    class Meta:
        ordering = ["character", "discipline", "name"]
        verbose_name = "Power"
        verbose_name_plural = "Powers"