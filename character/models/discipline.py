from django.db import models


class Discipline(models.Model):
    """
        Vampire characters have a number of disciplines. They always start with 3 which depend on their clan, 
        but they can obtain more than that (by drinking the blood of a vampire with another discipline and then
        spending XP on it)

        Because the Discipline is related to both the clan and the character, the Discipline itself has to be
        represented separately from its relationship to the character (unlike Attributes and Skills)
    """

    name = models.CharField(max_length=25)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        verbose_name = "Discipline"
        verbose_name_plural = "Disciplines"