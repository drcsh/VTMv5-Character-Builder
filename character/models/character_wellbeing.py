from django.db import models

from character.constants import HEALTH_STATES, WILLPOWER_STATES, HEALTH_STATE_HEALTHY, WILLPOWER_STATE_HEALTHY
from .mixins.wellbeing_mixin import WellbeingMixin
from .character import Character


class CharacterWellbeing(models.Model, WellbeingMixin):
    """
        CharacterWellbeing is the physical and mental wellbeing of the character

        The logic for changing wellbeing states is in the Mixin, this is just
        the model definition for storing the actual values. 

        Note that the class variable names must be consistent with the mixin.
    """

    character = models.ForeignKey(
        Character, 
        related_name="wellbeing", 
        on_delete=models.CASCADE
    )

    max_health = models.PositiveSmallIntegerField(default=5)
    max_willpower = models.PositiveSmallIntegerField(default=5)

    aggravated_health_damage = models.PositiveSmallIntegerField(default=0)
    aggravated_willpower_damage = models.PositiveSmallIntegerField(default=0)

    superficial_health_damage = models.PositiveSmallIntegerField(default=0)
    superficial_willpower_damage = models.PositiveSmallIntegerField(default=0)

    health_state = models.CharField(max_length=25, choices=HEALTH_STATES, default=HEALTH_STATE_HEALTHY)
    willpower_state = models.CharField(max_length=25, choices=WILLPOWER_STATES, default=WILLPOWER_STATE_HEALTHY)

    class Meta:
        verbose_name = "Character Wellbeing"
        verbose_name_plural = "Character Wellbeings"
