from django.db import models

from chronicle.models import Chronicle


class MinorCharacter(models.Model):
    """
        Represents a side character, usually controlled by the Storyteller. 
        
        These are qualitively different from Main Characters in that they don't have a full set
        of skills and attributes, but instead have pre-set dice pools to role for different
        types of situations. 
    """

    name = models.CharField(max_length=50)

    chronicle = models.ForeignKey(
        Chronicle,
        on_delete=models.CASCADE,
        related_name="minor_characters",
    )

    # Can be used to organise secondary chars. E.g. "SI", "Thugs", "Camarilla" etc
    tag = models.CharField(blank=True, max_length=50)

    physical_dice = models.PositiveSmallIntegerField()
    mental_dice = models.PositiveSmallIntegerField()
    social_dice = models.PositiveSmallIntegerField()

    special = models.TextField(blank=True)
    notes = models.TextField(blank=True)