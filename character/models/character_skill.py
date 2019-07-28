from django.db import models

from .character import Character 


class CharacterSkill(models.Model):
    """
        Skills exist in a many to one relationship with characters, each character has many skills (default 27) each
        with a value between 0 and 5, and an optional speciality which is a free text field. Additionally they have a
        'category', i.e. Physical/Social/Mental with corresponding attributes. 

        Each skill represented separately to allow adding custom fields. I.e. running a Chronicle in 1600, the
        Storyteller may want to use "Ride" rather than "Drive" and "Archery" rather than "Firearms", and not provide
        "Technology" or "Science" skills at all.
    """

    PHYSICAL = 0
    SOCIAL = 1
    MENTAL = 2

    CATEGORIES = (
        (PHYSICAL, 'Physical'),
        (SOCIAL, 'Social'),
        (MENTAL, 'Mental')
    )

    DEFAULT_SKILLS = (
        ("Athletics", PHYSICAL),
        ("Brawl", PHYSICAL),
        ("Craft", PHYSICAL),
        ("Drive", PHYSICAL),
        ("Firearms", PHYSICAL),
        ("Larceny", PHYSICAL),
        ("Melee", PHYSICAL),
        ("Stealth", PHYSICAL),
        ("Survival", PHYSICAL),
        ("Animal Ken", SOCIAL),
        ("Etiquette", SOCIAL),
        ("Insight", SOCIAL),
        ("Intimidation", SOCIAL),
        ("Leadership", SOCIAL),
        ("Performance", SOCIAL),
        ("Persuasion", SOCIAL),
        ("Streetwise", SOCIAL),
        ("Subterfuge", SOCIAL),
        ("Academics", MENTAL),
        ("Awareness", MENTAL),
        ("Finance", MENTAL),
        ("Investigation", MENTAL),
        ("Medicine", MENTAL),
        ("Occult", MENTAL),
        ("Politics", MENTAL),
        ("Science", MENTAL),
        ("Technology", MENTAL),
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
    name = models.CharField(max_length=25)
    category = models.PositiveSmallIntegerField(choices=CATEGORIES)
    speciality = models.CharField(max_length=50, blank=True)
    value = models.PositiveSmallIntegerField(choices=DOTS)

    class Meta:
        ordering = ["character", "category", "name"]
        verbose_name = "Character Skill"
        verbose_name_plural = "Character Skills"
        