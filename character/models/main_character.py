from django.db import models

from chronicle.models import Chronicle

from choices import ATTRIBUTE_DOTS, SKILL_DOTS

class MainCharacter(models.Model):
    """
        Full character sheet for players and important characters. Gives a full rundown of skills, attributes etc.
    """

    name = models.CharField()

    chronicle = models.ForeignKey(
        Chronicle,
        on_delete=models.CASCADE,
        related_name="minor_characters",
    )

    