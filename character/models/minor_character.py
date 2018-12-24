from django.db import models

from chronicle.models import Chronicle

from choices import ATTRIBUTE_DOTS, SKILL_DOTS

class MinorCharacter(models.Model):
    """
        Represents a side character, usually controlled by the Storyteller. 
        
        These are qualitively different from Main Characters in that they don't have a full set
        of skills and attributes, but instead have pre-set dice pools to role for different
        types of situations. 
    """

    name = models.CharField()

    chronicle = models.ForeignKey(
        Chronicle,
        on_delete=models.CASCADE,
        related_name="minor_characters",
    )

    physical_dice = models.IntegerField()

    mental_dice = models.IntegerField()

    social_dice = models.IntegerField()

    #TODO: Exceptional Dice Pools (these are mostly Skill + Attribute dice, but it's a customfield style deal)

    special = models.CharField(blank=True)

    notes = models.CharField(blank=True)