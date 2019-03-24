from django.db import models

import math

from character.constants import HEALTH_STATES, WILLPOWER_STATES
from .mixins.wellbeing_mixin import WellbeingMixin
from .character import Character

class CharacterWellbeing(models.Model, WellbeingMixin):
    """
        The wellbeing of a character encompanses their health (HP) and willpower (WP). 

        Both HP and WP can be damaged superficially or in an aggrevated way. On the 
        charactersheet these are represented by single / or an X respectively on
        the HP or WP tracker. When all boxes are marked with a / the character starts
        taking aggrevated damage. When all boxes are marked with aggrevated damage,
        they are physically or mentally broken.

        While simple to represent on a piece of paper, this is actually a bit 
        complicated to model. 
    """
    

    character = models.ForeignKey(
        Character, 
        related_name="wellbeing", 
        on_delete=models.CASCADE
    )

    max_health = models.PositiveSmallIntegerField()
    max_willpower = models.PositiveSmallIntegerField()

    aggravated_health_damage = models.PositiveSmallIntegerField()
    aggravated_willpower_damage = models.PositiveSmallIntegerField()

    superficial_health_damage = models.PositiveSmallIntegerField()
    superficial_willpower_damage = models.PositiveSmallIntegerField()

    health_state = models.SmallIntegerField(choices=HEALTH_STATES)
    willpower_state = models.SmallIntegerField(choices=WILLPOWER_STATES)


    class Meta:
        verbose_name = "Character Wellbeing"
        verbose_name_plural = "Character Wellbeings"

    def update_health_state(self):
        """
            Updates the health state of this character. 

            Note: only call after that character's health *changes*
        """
        self.health_state = self.calculate_new_health_state(
            self.health_state,
            self.max_health,
            self.aggravated_health_damage,
            self.superficial_health_damage,
            self.character.is_vampire
        )

    def update_willpower_state(self):
        """
            Updates the current willpower state state of this character. 
        """
        self.willpower_state = self.calculate_new_willpower_state(
            self.max_willpower,
            self.aggravated_willpower_damage,
            self.superficial_willpower_damage
            )

    def add_health_superficial_damage(self, damage, raw=False):
        """
            Add superficial damage to the tracker, halfing it if the character is a vampire.

            If raw is set, the damage will not be halved for vampires. 

            Updates the health state when done.
        """
        if self.character.is_vampire and not raw:
            damage = math.floor(damage / 2)

        self.aggravated_health_damage, self.superficial_health_damage = self.calculate_superficial_damage(
            self.max_health,
            self.aggravated_health_damage, 
            self.superficial_health_damage, 
            damage
        )

        self.update_health_state()
        self.save()
        
    def add_health_aggravated_damage(self, damage):
        """
            Add aggravated damage to the tracker.

            Updates the health state when done.
        """
        self.aggravated_health_damage, self.superficial_health_damage = self.calculate_aggravated_damage(
            self.max_health,
            self.aggravated_health_damage, 
            self.superficial_health_damage, 
            damage
        )

        self.update_health_state()
        self.save()

    def add_willpower_superficial_damage(self, damage):
        """
            Add superficial damage to the willpower tracker
        """
        self.aggravated_willpower_damage, self.superficial_willpower_damage = self.calculate_superficial_damage(
            self.max_willpower,
            self.aggravated_willpower_damage, 
            self.superficial_willpower_damage, 
            damage
        )

        self.update_willpower_state()
        self.save()

    def add_willpower_aggravated_damage(self, damage):
        """
            Add aggravated damage to the willpower tracker
        """
        self.aggravated_willpower_damage, self.superficial_willpower_damage = self.calculate_aggravated_damage(
            self.max_willpower,
            self.aggravated_willpower_damage, 
            self.superficial_willpower_damage, 
            damage
        )

        self.update_willpower_state()
        self.save()
    