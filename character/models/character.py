from django.db import models

from chronicle.models import Chronicle

# Model Dependencies 
from .clan import Clan
from .discipline import Discipline
from .character_discipline import CharacterDiscipline
from .vampire_generation import Generation

class Character(models.Model):
    """
        Represents a player character or important NPC. The equivalent of a full character sheet instead of
        just a minor character.

        The character can be mortal or vampire
    """

    # Identification
    name = models.CharField()
    chronicle = models.ForeignKey(
        Chronicle,
        on_delete=models.CASCADE,
        related_name="characters",
    )

    # Personality
    concept = models.TextField()
    ambition = models.TextField()
    desire = models.TextField()

    # Background
    date_of_birth = models.DateField()
    date_of_death = models.DateField(blank=True)
    true_age = models.PositiveIntegerField()
    apparent_age = models.PositiveIntegerField()
    appearence = models.TextField()
    distinguishing_features = models.TextField()
    history = models.TextField()
    notes = models.TextField()

    # Blood
    is_vampire = models.BooleanField(null=False, default=True)
    clan = models.ForeignKey(
        Clan,
        on_delete=models.PROTECT,
        null=True  # Technically you could create (or start as) a mortal rather than a vampire
    )
    generation = models.ForeignKey(
        Generation,
        on_delete=models.PROTECT,
        null=True
    )
    disciplines = models.ManyToManyField(
        Discipline,
        related_name="characters",
        through=CharacterDiscipline  # Custom intermediary
    )
    blood_potency = models.PositiveSmallIntegerField()
    predator_type = models.CharField()
    hunger = models.PositiveSmallIntegerField()
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Main Character"
        verbose_name_plural = "Main Characters"

    