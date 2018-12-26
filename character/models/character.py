from django.db import models

from chronicle.models import Chronicle

# Model Dependencies 
from character_attributes import CharacterAttributes
from clan import Clan

class Character(models.Model):
    """
        Full character sheet for players and important characters. Gives a full rundown of skills, attributes etc.
    """

    # Identification
    name = models.CharField()
    chronicle = models.ForeignKey(
        Chronicle,
        on_delete=models.CASCADE,
        related_name="characters",
    )

    # General 
    concept = models.TextField()
    predator_type = models.CharField()
    ambition = models.TextField()
    desire = models.TextField()
    clan = models.ForeignKey(
        Clan,
        on_delete=models.PROTECT,
        null=True  # Technically you could create (or start as) a mortal rather than a vampire
    )

    # Attributes
    attribues = models.OneToOneField(CharacterAttributes)
    

    class Meta:
        ordering = ["name"]
        verbose_name = "Main Character"
        verbose_name_plural = "Main Characters"

    