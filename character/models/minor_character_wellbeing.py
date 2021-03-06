from django.db import models

from character.constants import HEALTH_STATES, WILLPOWER_STATES
from .mixins.wellbeing_mixin import WellbeingMixin
from .minor_character import MinorCharacter


class MinorCharacterWellbeing(models.Model, WellbeingMixin):
    """
        MinorCharacterWellbeing is the physical and mental wellbeing of the
        minor character

        The logic for changing wellbeing states is in the Mixin, this is just
        the model definition for storing the actual values. 

        Note that the class variable names must be consistent with the mixin.
    """
    
    character = models.ForeignKey(
        MinorCharacter, 
        related_name="wellbeing", 
        on_delete=models.CASCADE
    )

    max_health = models.PositiveSmallIntegerField()
    max_willpower = models.PositiveSmallIntegerField()

    aggravated_health_damage = models.PositiveSmallIntegerField()
    aggravated_willpower_damage = models.PositiveSmallIntegerField()

    superficial_health_damage = models.PositiveSmallIntegerField()
    superficial_willpower_damage = models.PositiveSmallIntegerField()

    health_state = models.CharField(max_length=25, choices=HEALTH_STATES)
    willpower_state = models.CharField(max_length=25, choices=WILLPOWER_STATES)

    class Meta:
        verbose_name = "Minor Character Wellbeing"
        verbose_name_plural = "Minor Character Wellbeings"
