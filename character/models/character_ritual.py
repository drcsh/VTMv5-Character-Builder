from django.db import models

from .character import Character
from .discipline import Discipline


class CharacterRitual(models.Model):
    """
        In addition to their disciplines, characters can learn magic
        rituals. 

        These are usually associated with the Blood Sorcery discipline, 
        but they can also be associated with Oblibion (and presumably
        eventually Koldunic Sorvery). As a result I've left it open 
        which discipline (if any) the ritual is bound to.
    """

    character = models.ForeignKey(
        Character, 
        related_name="rituals", 
        on_delete=models.CASCADE
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    description = models.TextField()
    ritual_level = models.PositiveSmallIntegerField()
    ingredients = models.TextField(null=True, blank=True)
    process = models.TextField(null=True, blank=True)
    system = models.TextField(null=True, blank=True)
    
