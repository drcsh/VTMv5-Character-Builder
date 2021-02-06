from django.dispatch import receiver
from django.db.models.signals import post_save

from character.models import Character, CharacterAttribute, CharacterSkill, CharacterWellbeing


@receiver(post_save, sender=Character, created=True)
def initialise_character(sender, instance, *args, **kwargs):
    """
    Initialize fields on the Character when it's created

    TODO: Maybe want to do this via a creation form instead of implicitly here...
    """

    # Attributes
    for name, category in CharacterAttribute.DEFAULT_ATTRIBUTES:
        CharacterAttribute(character=instance, name=name, category=category, value=0)

    # Skills
    for name, category in CharacterSkill.DEFAULT_SKILLS:
        CharacterSkill(character=instance, name=name, category=category, value=0)

    CharacterWellbeing(character=instance)
