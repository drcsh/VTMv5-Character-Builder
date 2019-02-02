from django.db import models

from .character import Character

class CharacterAttribute(models.Model):
    """
        Attributes exist in a many to one relationship with a character. Each character should have the same
        9 attributes by default. 

        It could also allow custom attributes like we have custom skills.
    """

    DEFAULT_ATTRIBUTES = (
        ('Strength', 0),
        ('Dexterity', 0),
        ('Stamina', 0),
        ('Charisma', 1),
        ('Manipulation', 1),
        ('Composure', 1),
        ('Intelligence', 2),
        ('Wits', 2),
        ('Resolve', 2),
    )

    CATEGORIES = (
        (0, 'Physical'),
        (1, 'Social'),
        (2, 'Mental')
    )

    # Each attribute has a "dot" value from 0-5
    DOTS = (
        (0, 'Debilitated'),
        (1, 'Poor'),
        (2, 'Average'),
        (3, 'Good'),
        (4, 'Excellent'),
        (5, 'Peak Ability'),
    )

    character = models.ForeignKey(
        Character, 
        related_name="attributes", 
        on_delete=models.CASCADE
    )
    name = models.CharField()
    category = models.PositiveSmallIntegerField(choices=CATEGORIES)
    display_order = models.PositiveSmallIntegerField()
    value = models.PositiveSmallIntegerField(choices=DOTS)
    

    class Meta:
        ordering = ["character", "category", "description"]
        verbose_name = "Character Skill"
        verbose_name_plural = "Character Skills"