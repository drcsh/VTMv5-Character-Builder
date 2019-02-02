from django.db import models

from .discipline import Discipline
from .character import Character

class CharacterDiscipline(models.Model):
    """
        Represents a discipline which a character has access to. 
        
        This is a many-to-many relationship with an additional 'value' field which represents
        how developed their powers are in that discipline (i.e. how many dots)
    """

    DOTS = (
        (0, 'Latent'),
        (1, 'Nascent'),
        (2, 'Developing'),
        (3, 'Potent'),
        (4, 'Masterful'),
        (5, 'Apotheosis'),
    )

    discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(choices=DOTS)