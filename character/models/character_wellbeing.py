from django.db import models

from character.constants import HEALTH_STATES, WILLPOWER_STATES
from .mixins.wellbeing_mixin import WellbeingMixin
from .character import Character


class CharacterWellbeing(models.Model, WellbeingMixin):
    """
        CharacterWellbeing is the physical and mental wellbeing of the character

        The logic for changing wellbeing states is in the Mixin, this is just
        the model definition for storing the actual values. 

        Note that the class names must be consistent with the mixin.
    """

    character = models.ForeignKey(
        Character, 
        related_name="wellbeing", 
        on_delete=models.CASCADE
    )

    max_health = models.PositiveSmallIntegerField()
    max_willpower = models.PositiveSmallIntegerField()

    aggravated_health_damage = models.PositiveSmallIntegerField()
    aggravated_willpower_damage = models.PositiveSmallIntegerField()

    superficial_health_damage = models.PositiveSmallIntegerField()
    superficial_willpower_damage = models.PositiveSmallIntegerField()

    health_state = models.SmallIntegerField(choices=HEALTH_STATES)
    willpower_state = models.SmallIntegerField(choices=WILLPOWER_STATES)

    class Meta:
        verbose_name = "Character Wellbeing"
        verbose_name_plural = "Character Wellbeings"
