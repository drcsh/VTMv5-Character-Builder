from character.constants import *


class DamageCalculator:
    """
        Static class which provides methods for calculating the effect of damage.
    """

    @staticmethod
    def calculate_new_health_state(current_state,
                                   max_health,
                                   old_aggravated_damage,
                                   new_aggravated_damage,
                                   new_superficial_damage,
                                   is_vampire):
        """
            Work out the new health state of a character - assumes that the character's health state has just
            changed (i.e. they took damage or recovered some health)

            :param str current_state: corresponds to a Health state constant
            :param int max_health: the maximum number of 'boxes' on the health tracker
            :param int old_aggravated_damage: previous aggravated damage
            :param int new_aggravated_damage: aggravated damage now on their tracker
            :param int new_superficial_damage: superficial damage now on their tracker
            :param bool is_vampire: vampires have an additional health state (torpor)
            :return: The new health state of the character (post damage)
            :rtype str:
        """

        # Beating a dead vamp
        if current_state == HEALTH_STATE_DEAD:
            return HEALTH_STATE_DEAD

        # special rules for vamps in torpor
        if current_state == HEALTH_STATE_TORPOR:

            # If they took more aggravated damage, they suffer the final death
            if new_aggravated_damage > old_aggravated_damage:
                return HEALTH_STATE_DEAD

            # If they are in torpor and heal back to full HP, they recover
            if new_aggravated_damage == 0:
                return HEALTH_STATE_HEALTHY

            # Otherwise, they stay in Torpor
            return HEALTH_STATE_TORPOR

        # Tracker full, mortals die, vamps go into Torpor
        if new_aggravated_damage >= max_health:

            if is_vampire:
                return HEALTH_STATE_TORPOR

            return HEALTH_STATE_DEAD

        # impairment
        total_damage = new_aggravated_damage + new_superficial_damage
        if total_damage >= max_health:
            return HEALTH_STATE_IMPAIRED

        if total_damage > 0:
            return HEALTH_STATE_INJURED

        return HEALTH_STATE_HEALTHY

    @staticmethod
    def calculate_new_willpower_state(max_willpower, new_aggravated_damage, new_superficial_damage):
        """
            Works out the new Willpower state of the character. Much simpler than health - willpower is either
            impaired or unimpaired and there is no difference between vampires and mortals

            :param int max_willpower: the maximum number of 'boxes' on the willpower tracker
            :param int new_aggravated_damage: aggravated damage now on their tracker
            :param int new_superficial_damage: superficial damage now on their tracker
            :return: The new willpower state of the character (post damage)
            :rtype int:
        """

        if new_aggravated_damage + new_superficial_damage >= max_willpower:
            return WILLPOWER_STATE_IMPAIRED

        return WILLPOWER_STATE_HEALTHY

    @staticmethod
    def calculate_superficial_damage(max_value, aggravated_damage, superficial_damage, damage_taken):
        """
           Add Superficial damage to a tracker. Wraps calculate_damage.

           :param int max_value: the character's maximum health or willpower
           :param int aggravated_damage: current aggravated damage marked on the tracker
           :param int superficial_damage: current superficial damage
           :param int damage_taken: superficial damage to be added
           :return (aggravated_damage, superficial damage): new values for the tracker
           :rtype tuple:
        """
        return DamageCalculator.calculate_damage(max_value, aggravated_damage, superficial_damage, damage_taken, False)

    @staticmethod
    def calculate_aggravated_damage(max_value, aggravated_damage, superficial_damage, damage_taken):
        """
           Add Aggravated damage to a tracker. Wraps calculate_damage.

           :param int max_value: the character's maximum health or willpower
           :param int aggravated_damage: current aggravated damage marked on the tracker
           :param int superficial_damage: current superficial damage
           :param int damage_taken: superficial damage to be added
           :return (aggravated_damage, superficial damage): new values for the tracker
           :rtype tuple:
        """
        return DamageCalculator.calculate_damage(max_value, aggravated_damage, superficial_damage, damage_taken, True)

    @staticmethod
    def calculate_damage(max_value, aggravated_damage, superficial_damage, damage_taken, is_aggravated):
        """
        Calculates the effect of damage on the health or willpower tracker.

        Damage is added to the tracker as long as there is 'space' (on a physical
        character sheet, this means unmarked boxes), in other words, as long as the
        combined aggravated and superficial damage is less than the maximum value of the
        tracker. If space runs out, existing superficial damage is turned into aggravated
        for each point of additional superficial or aggravated damage taken over the maximum.

        :param int max_value: the character's maximum health or willpower
        :param int aggravated_damage: current aggravated damage marked on the tracker
        :param int superficial_damage: current superficial damage
        :param int damage_taken: damage to add to the tracker
        :param bool is_aggravated: True if the damage is Aggravated, otherwise it's Superficial
        :return (aggravated_damage, superficial damage): new values for the tracker
        :rtype tuple:
        """

        free_boxes = max_value - aggravated_damage - superficial_damage

        if free_boxes >= damage_taken:
            # there are free HP/WP boxes, so we can just add the damage
            if is_aggravated:
                aggravated_damage += damage_taken
            else:
                superficial_damage += damage_taken

        else:
            # Superficial damage gets converted to aggravated.
            aggravated_damage += (damage_taken - free_boxes)

            if aggravated_damage >= max_value:
                # bad things are going to happen!
                aggravated_damage = max_value
                superficial_damage = 0

            else:
                superficial_damage = max_value - aggravated_damage

        return aggravated_damage, superficial_damage