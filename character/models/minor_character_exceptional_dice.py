from django.db import models

from .minor_character import MinorCharacter


class MinorCharacterExceptionalDice(models.Model):
    """
        Exceptional dice pools represent particular specialisms for minor characters
        beyond the basic (physical/mental/social). For example an SI operative may have
        exceptional dice pools for Firearms, Investigation, etc.

        Minor characters can have multiple exceptional dice pools. 
    """

    minor_character = models.ForeignKey(
        MinorCharacter,
        on_delete=models.CASCADE,
        related_name="exceptional_dice",
    )
    description = models.CharField(max_length=30, blank=False)
    value = models.PositiveSmallIntegerField()