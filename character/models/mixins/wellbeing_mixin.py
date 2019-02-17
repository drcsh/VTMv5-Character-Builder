
from character.constants import *

class WellbeingMixin(object):

    @staticmethod
    def calculate_new_health_state(current_state, max_health, new_aggravated_damage, new_superficial_damage, is_vampire):
        """
           Work out the new health state of a character
           TODO
        """
        pass
    
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