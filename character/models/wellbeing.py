from django.db import models

import math

class Wellbeing(models.Model):
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
    DEAD = -1
    TORPOR = 0
    IMPARED = 1
    INJURED = 2
    HEALTHY = 3

    HEALTH_STATES = (
        (DEAD, "Dead"),
        (TORPOR, "Torpor"),
        (IMPARED, "Physically Impared"),
        (INJURED, "Injured"),
        (HEALTHY, "Healthy"),
    )

    IMPARED = 0
    OK = 1

    WILLPOWER_STATES = (
        (IMPARED, "Impared"),
        (OK, "Unimpared")
    )

    max_health = models.PositiveSmallIntegerField()
    max_willpower = models.PositiveSmallIntegerField()

    aggrevated_health_damage = models.PositiveSmallIntegerField()
    aggrevated_willpower_damage = models.PositiveSmallIntegerField()

    superficial_health_damage = models.PositiveSmallIntegerField()
    superficial_willpower_damage = models.PositiveSmallIntegerField()

    health_state = models.SmallIntegerField(choices=HEALTH_STATES)
    willpower_state = models.SmallIntegerField(choices=WILLPOWER_STATES)

    class Meta:
        verbose_name = "Character Wellbeing"
        verbose_name_plural = "Character Wellbeings"

    def update_health_state_and_save(self):
        # Work out the current health state
        #TODO: logic for this
        self.save()

    def add_health_superficial_damage(self, damage, halved=False):
        """
            Add superficial damage to the tracker. Optionally halving it (e.g. if the
            character is a vampire), and convert to aggrevated if the tracker overflows.
        """
        if halved:
            damage = math.floor(damage / 2)

        free_boxes = self.max_health - self.aggrevated_health_damage - self.superficial_health_damage

        if free_boxes > damage:
            # there are free HP boxes, so we can just add the superficial damage
            self.superficial_health_damage += damage

        elif free_boxes < damage:
            # We have to convert the remainder to aggrevated and fill the tracker with superficial
            new_aggrevated_damage = self.aggrevated_health_damage + (damage - free_boxes)

            if new_aggrevated_damage >= self.max_health:
                # bad things happen!
                self.aggrevated_health_damage = self.max_health
                self.superficial_health_damage = 0

            else:
                self.aggrevated_health_damage = new_aggrevated_damage
                self.superficial_health_damage = self.max_health - self.aggrevated_health_damage

   
        self.update_health_state_and_save()
        


    