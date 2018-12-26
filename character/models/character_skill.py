from django.db import models

from .character import Character 


class CharacterSkill(models.Model):
    """
        Skills exist in a many to one relationship with characters, each character has many skills (default 27) each with
        a value between 0 and 5, and an optional speciality which is a free text field. Additionally they have a
        'category', i.e. Physical/Social/Mental with corresponding attributes. 

        Each skill represented separately to allow adding custom fields. I.e. running a Chronicle in 1600, the Storyteller
        may want to use "Ride" rather than "Drive" and "Archery" rather than "Firearms", nd not provide "Technology" or
        "Science" skills at all. 
    """
    DEFAULT_SKILLS = (
        ("Athletics", 0),
        ("Brawl", 0),
        ("Craft", 0),
        ("Drive", 0),
        ("Firearms", 0),
        ("Larceny", 0),
        ("Melee", 0),
        ("Stealth", 0),
        ("Survival", 0),
        ("Animal Ken", 1),
        ("Etiquette", 1),
        ("Insight", 1),
        ("Intimidation", 1),
        ("Leadership", 1),
        ("Performance", 1),
        ("Persuasion", 1),
        ("Streetwise", 1),
        ("Subterfuge", 1),
        ("Academics", 2),
        ("Awareness", 2),
        ("Finance", 2),
        ("Investigation", 2),
        ("Medicine", 2),
        ("Occult", 2),
        ("Politics", 2),
        ("Science", 2),
        ("Technology", 2),
    )

    CATEGORIES = (
        (0, 'Physical'),
        (1, 'Social'),
        (2, 'Mental')
    )

    DOTS = (
        (0, 'Untrained'),
        (1, 'Novice'),
        (2, 'Trained'),
        (3, 'Experienced'),
        (4, 'Expert'),
        (5, 'Renowned Master'),
    )

    character = models.ForeignKey(
        Character, 
        related_name="skills", 
        on_delete=models.CASCADE
    )
    name = models.CharField()
    category = models.PositiveSmallIntegerField(choices=CATEGORIES)
    speciality = models.CharField(blank=True)
    value = models.PositiveSmallIntegerField(choices=DOTS)

    class Meta:
        ordering = ["character", "category", "description"]
        verbose_name = "Character Skill"
        verbose_name_plural = "Character Skills"