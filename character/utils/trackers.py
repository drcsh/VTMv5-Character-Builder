from character.constants import *

"""
    WIP: Not sure if I'll use these. The idea is to use them in conjunction with thr WellbeingMixin to store data
    for passing about the place, but I don't like that it's adding a layer of abstraction between the Model and the
    business logic, and the logic required to handle this will be prone to mess. 
"""

class HealthTracker:
    """
    Data class for passing around health state information for a character.
    """

    def __init__(self, health_state, max_health, aggravated_damage, superficial_damage):

        if health_state not in HEALTH_STATES:
            raise ValueError(f"Invalid health state {health_state}")

        assert isinstance(max_health, int)
        assert isinstance(aggravated_damage, int)
        assert isinstance(superficial_damage, int)

        self.health_state = health_state
        self.max_health = max_health
        self.aggravated_damage = aggravated_damage
        self.superficial_damage = superficial_damage


class WillpowerTracker:
    """
    Data class for passing around willpower state information for a character.
    """

    def __init__(self, willpower_state, max_willpower, aggravated_damage, superficial_damage):

        if willpower_state not in WILLPOWER_STATES:
            raise ValueError(f"Invalid willpower state {willpower_state}")

        assert isinstance(max_willpower, int)
        assert isinstance(aggravated_damage, int)
        assert isinstance(superficial_damage, int)

        self.willpower_state = willpower_state
        self.max_health = max_willpower
        self.aggravated_damage = aggravated_damage
        self.superficial_damage = superficial_damage
