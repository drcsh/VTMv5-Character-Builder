import math

from character.constants import *


class WellbeingMixin(object):
    """
        This Mixin handles the actual logic for character wellbeing so that it can be reused for 
        Minor characters and main characters. 

        The wellbeing of a character encompanses their health (HP) and willpower (WP). 

        Both HP and WP can be damaged superficially or in an aggrevated way. On the 
        charactersheet these are represented by single / or an X respectively on
        the HP or WP tracker. When all boxes are marked with a / the character starts
        taking aggrevated damage. When all boxes are marked with aggrevated damage,
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

    @staticmethod
    def calculate_new_health_state(current_state, max_health, new_aggravated_damage, new_superficial_damage, is_vampire):
        """
            Work out the new health state of a character - assumes that the character's health state has just 
            changed (i.e. they took damage or recovered some health)
           
            :param int current_state: corresponds to a Health state constant
            :param int max_health: the maximum number of 'boxes' on the health tracker
            :param int new_aggravated_damage: aggravated damage now on their tracker
            :param int new_superficial_damage: superficial damage now on their tracker
            :param bool is_vampire: vampires have an additional health state (torpor)
            :return: The new health state of the character (post damage)
            :rtype int:
        """

        # Sanity check:
        if current_state == HEALTH_STATE_DEAD:
            return HEALTH_STATE_DEAD
        
        # Tracker full (death/torpor)
        if new_aggravated_damage >= max_health:

            if not is_vampire:
                return HEALTH_STATE_DEAD

            # Additional damage received by a vamp in Torpor causes death
            if current_state != HEALTH_STATE_TORPOR:
                return HEALTH_STATE_TORPOR
                
            else:
                return HEALTH_STATE_DEAD

        # impairment 
        if new_aggravated_damage + new_superficial_damage >= max_health:
            return HEALTH_STATE_IMPARED

        if new_aggravated_damage + new_superficial_damage > 0:
            return HEALTH_STATE_INJURED

        return HEALTH_STATE_HEALTHY

    @staticmethod
    def calculate_new_willpower_state(max_willpower, new_aggravated_damage, new_superficial_damage):
        """
            Works out the new Willpower state of the character. Much simpler than health - willpower is either 
            umpaired or unimpaired and there is no difference between vampires and mortals

            :param int max_willpower: the maximum number of 'boxes' on the willpower tracker
            :param int new_aggravated_damage: aggravated damage now on their tracker
            :param int new_superficial_damage: superficial damage now on their tracker
            :return: The new willpower state of the character (post damage)
            :rtype int:
        """

        if new_aggravated_damage + new_superficial_damage >= max_willpower:
            return WILLPOWER_STATE_IMPARED

        return WILLPOWER_STATE_OK
     
    @staticmethod
    def calculate_superficial_damage(max_value, aggravated_damage, superficial_damage, damage_taken):
        """
           Calculates the effect of superficial damage on the health or willpower tracker.

           Superficial damage is added to the tracker as long as there is 'space' (on a physical
           character sheet, this means unmarked boxes), in other words, as long as the
           combined aggravated and superficial damage is less than the maximum value of the
           tracker. If space runs out, existing superficial damage is turned into aggravated
           for each point of additional superficial damage taken over the maximum.

           :param int max_value: the character's maximum health or willpower
           :param int aggravated_damage: current aggravated damage marked on the tracker
           :param int superficial_damage: current superficial damage
           :param int damage_taken: superficial damage to be added
           :return (aggravated_damage, superficial damage): new values for the tracker
           :rtype tuple:
        """
        free_boxes = max_value - aggravated_damage - superficial_damage

        if free_boxes >= damage_taken:
            # there are free HP/WP boxes, so we can just add the damage
            superficial_damage += damage_taken

        else:
            # We have to convert the remainder to aggrevated and fill the tracker with superficial
            aggravated_damage += (damage_taken - free_boxes)

            if aggravated_damage >= max_value:
                # bad things are going to happen!
                aggravated_damage = max_value
                superficial_damage = 0

            else:
                superficial_damage = max_value - aggravated_damage

        return (aggravated_damage, superficial_damage)
    
    @staticmethod
    def calculate_aggravated_damage(max_value, aggravated_damage, superficial_damage, damage_taken):
        """
           work out the effect of aggravated damage on the tracker
        """
        
        free_boxes = max_value - aggravated_damage - superficial_damage

        # whatever happens, aggravated damage is going up
        aggravated_damage += damage_taken

        if aggravated_damage > max_value:
            # oh dear
            aggravated_damage = max_value
            superficial_damage = 0

        elif free_boxes < damage_taken:
            # We ran out of space on the tracker, so superficial damage goes down as it
            # is overwritten by aggravated damage
            remainder = free_boxes - damage_taken
            superficial_damage -= remainder

        return (aggravated_damage, superficial_damage)

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
