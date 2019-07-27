import math

from character.utils import DamageCalculator


class WellbeingMixin(object):
    """
        This Mixin handles the actual logic for character wellbeing so that it can be reused for 
        Minor characters and main characters. 

        The wellbeing of a character encompasses their health (HP) and willpower (WP).

        Both HP and WP can be damaged superficially or in an aggravated way. On the
        charactersheet these are represented by single / or an X respectively on
        the HP or WP tracker. When all boxes are marked with a / the character starts
        taking aggravated damage. When all boxes are marked with aggravated damage,
        they are physically or mentally broken.

        While simple to represent on a piece of paper, this is actually a bit 
        complicated to model. 
    """

    # These will all be overwritten by the Wellbeing classes. 
    character = None

    max_health = None
    max_willpower = None

    aggravated_health_damage = None
    aggravated_willpower_damage = None

    superficial_health_damage = None
    superficial_willpower_damage = None

    health_state = None
    willpower_state = None

    def update_health_state(self):
        """
            Updates the health state of this character. 

            Note: only call after that character's health *changes*
        """
        self.health_state = DamageCalculator.calculate_new_health_state(
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
        self.willpower_state = DamageCalculator.calculate_new_willpower_state(
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

        self.aggravated_health_damage, self.superficial_health_damage = DamageCalculator.calculate_superficial_damage(
            self.max_health,
            self.aggravated_health_damage, 
            self.superficial_health_damage, 
            damage
        )

        self.update_health_state()
        
    def add_health_aggravated_damage(self, damage):
        """
            Add aggravated damage to the tracker.

            Updates the health state when done.
        """
        self.aggravated_health_damage, self.superficial_health_damage = DamageCalculator.calculate_aggravated_damage(
            self.max_health,
            self.aggravated_health_damage, 
            self.superficial_health_damage, 
            damage
        )

        self.update_health_state()

    def add_willpower_superficial_damage(self, damage):
        """
            Add superficial damage to the willpower tracker
        """
        self.aggravated_willpower_damage, self.superficial_willpower_damage = DamageCalculator.calculate_superficial_damage(
            self.max_willpower,
            self.aggravated_willpower_damage, 
            self.superficial_willpower_damage, 
            damage
        )

        self.update_willpower_state()

    def add_willpower_aggravated_damage(self, damage):
        """
            Add aggravated damage to the willpower tracker
        """
        self.aggravated_willpower_damage, self.superficial_willpower_damage = DamageCalculator.calculate_aggravated_damage(
            self.max_willpower,
            self.aggravated_willpower_damage, 
            self.superficial_willpower_damage, 
            damage
        )

        self.update_willpower_state()
