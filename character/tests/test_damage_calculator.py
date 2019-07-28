from django.test import TestCase

from character.utils import DamageCalculator
from character.constants import *


class TestDamageCalculator(TestCase):

    def setUp(self):
        pass

    def test_new_health_state_healthy(self):
        # Test that with no damage done, the returned health state is healthy
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=0,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=True)

        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=0,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)

        self.assertEqual(result_human, HEALTH_STATE_HEALTHY)
        self.assertEqual(result_vamp, HEALTH_STATE_HEALTHY)

    def test_new_health_state_human(self):
        # Test the various ways that a human character takes damage

        # Human hit for HP of Agg
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=5,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_DEAD)

        # Human overkill
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=9999,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_DEAD)

        # Human injured, agg damage
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=1,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

        # Human injured, superficial damage
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=0,
                                                                   new_superficial_damage=1,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

        # Human injured, mixed damage types
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=1,
                                                                   new_superficial_damage=2,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

        # Test that the max health doesn't alter the result here.
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=7,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=2,
                                                                   new_superficial_damage=3,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

        # Human Injured, then injured again superficially
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                   max_health=7,
                                                                   old_aggravated_damage=2,
                                                                   new_aggravated_damage=2,
                                                                   new_superficial_damage=3,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

        # Human Injured, then injured again aggravated
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                   max_health=7,
                                                                   old_aggravated_damage=2,
                                                                   new_aggravated_damage=3,
                                                                   new_superficial_damage=3,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

        # Human injured, then splatted
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                   max_health=5,
                                                                   old_aggravated_damage=2,
                                                                   new_aggravated_damage=5,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_DEAD)

        # Humans that are dead, stay dead (... in combat anyway)
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_DEAD,
                                                                   max_health=5,
                                                                   old_aggravated_damage=5,
                                                                   new_aggravated_damage=6,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_DEAD)

    def test_new_health_state_vamp(self):
        # Test the various ways that a vampire character takes damage

        # vampire hit for HP of Agg goes into torpor
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=5,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_TORPOR)

        # vampire overkill technically still sends them to torpor except under special circumstances not handled
        # by the calculator (Storyteller's discretion)
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=9999,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_TORPOR)

        # vampire injured, agg damage
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=1,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

        # vampire injured, superficial damage
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=0,
                                                                  new_superficial_damage=1,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

        # vampire injured, mixed damage types
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=1,
                                                                  new_superficial_damage=2,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

        # Test that the max health doesn't alter the result here.
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=7,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=2,
                                                                  new_superficial_damage=3,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

        # vampire Injured, then injured again superficially
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                  max_health=7,
                                                                  old_aggravated_damage=2,
                                                                  new_aggravated_damage=2,
                                                                  new_superficial_damage=3,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

        # vampire Injured, then injured again aggravated
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                  max_health=7,
                                                                  old_aggravated_damage=2,
                                                                  new_aggravated_damage=3,
                                                                  new_superficial_damage=3,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

        # vampire injured, then put into torpor
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                  max_health=5,
                                                                  old_aggravated_damage=2,
                                                                  new_aggravated_damage=5,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_TORPOR)


        # vamps heal slowly in torpor but don't get better until they hit full HP
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_TORPOR,
                                                                  max_health=5,
                                                                  old_aggravated_damage=5,
                                                                  new_aggravated_damage=4,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_TORPOR)

        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_TORPOR,
                                                                  max_health=5,
                                                                  old_aggravated_damage=1,
                                                                  new_aggravated_damage=0,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_HEALTHY)

        # Vamps that have met the final death, stay dead
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_DEAD,
                                                                  max_health=5,
                                                                  old_aggravated_damage=5,
                                                                  new_aggravated_damage=6,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_DEAD)
