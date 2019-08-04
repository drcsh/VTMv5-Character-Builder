from django.test import TestCase

from character.utils import DamageCalculator
from character.constants import *


class TestDamageCalculator(TestCase):

    def setUp(self):
        pass

    def test_new_health_state_healthy_huaman(self):
        # Test that with no damage done, the returned health state is healthy
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=0,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=True)
        self.assertEqual(result_human, HEALTH_STATE_HEALTHY)

    def test_new_health_state_healthy_vamp(self):
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=0,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)

        self.assertEqual(result_vamp, HEALTH_STATE_HEALTHY)

    def test_new_health_state_human_dead(self):
        # Test the various ways that a human character takes damage

        # Human hit for HP of Agg
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=5,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_DEAD)

    def test_new_health_state_human_overkill(self):
        # Human overkill
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=9999,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_DEAD)

    def test_new_health_state_human_injured(self):
        # Human injured, agg damage
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=1,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

    def test_new_health_state_human_injured_superficial(self):
        # Human injured, superficial damage
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=0,
                                                                   new_superficial_damage=1,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

    def test_new_health_state_human_injured_mixed(self):
        # Human injured, mixed damage types
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=5,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=1,
                                                                   new_superficial_damage=2,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

    def test_new_health_state_human_injured_diff_health(self):
        # Test that the max health doesn't alter the result here.
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                   max_health=7,
                                                                   old_aggravated_damage=0,
                                                                   new_aggravated_damage=2,
                                                                   new_superficial_damage=3,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

    def test_new_health_state_human_injured_twice_superficial(self):
        # Human Injured, then injured again superficially
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                   max_health=7,
                                                                   old_aggravated_damage=2,
                                                                   new_aggravated_damage=2,
                                                                   new_superficial_damage=3,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

    def test_new_health_state_human_injured_twice_agg(self):
        # Human Injured, then injured again aggravated
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                   max_health=7,
                                                                   old_aggravated_damage=2,
                                                                   new_aggravated_damage=3,
                                                                   new_superficial_damage=3,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_INJURED)

    def test_new_health_state_human_injured_then_impaired(self):
        # Human injured, then takes damage and becomes impaired
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                   max_health=5,
                                                                   old_aggravated_damage=2,
                                                                   new_aggravated_damage=2,
                                                                   new_superficial_damage=3,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_IMPAIRED)

    def test_new_health_state_human_impaired_still(self):
        # Human injured, then takes damage and becomes impaired
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_IMPAIRED,
                                                                   max_health=5,
                                                                   old_aggravated_damage=2,
                                                                   new_aggravated_damage=4,
                                                                   new_superficial_damage=1,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_IMPAIRED)

    def test_new_health_state_human_injured_then_dead(self):
        # Human injured, then splatted
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                   max_health=5,
                                                                   old_aggravated_damage=2,
                                                                   new_aggravated_damage=5,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_DEAD)

    def test_new_health_state_human_no_zombies(self):
        # Humans that are dead, stay dead (... in combat anyway)
        result_human = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_DEAD,
                                                                   max_health=5,
                                                                   old_aggravated_damage=5,
                                                                   new_aggravated_damage=6,
                                                                   new_superficial_damage=0,
                                                                   is_vampire=False)
        self.assertEqual(result_human, HEALTH_STATE_DEAD)

    def test_new_health_state_vamp_torpor(self):
        # Test the various ways that a vampire character takes damage

        # vampire hit for HP of Agg goes into torpor
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=5,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_TORPOR)

    def test_new_health_state_vamp_overkill(self):
        # vampire overkill technically still sends them to torpor except under special circumstances not handled
        # by the calculator (Storyteller's discretion)
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=9999,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_TORPOR)

    def test_new_health_state_vamp_injured(self):
        # vampire injured, agg damage
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=1,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

    def test_new_health_state_vamp_injured_superficial(self):
        # vampire injured, superficial damage
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=0,
                                                                  new_superficial_damage=1,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

    def test_new_health_state_vamp_injured_mixed(self):
        # vampire injured, mixed damage types
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=5,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=1,
                                                                  new_superficial_damage=2,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

    def test_new_health_state_vamp_injured_diff_health(self):
        # Test that the max health doesn't alter the result here.
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_HEALTHY,
                                                                  max_health=7,
                                                                  old_aggravated_damage=0,
                                                                  new_aggravated_damage=2,
                                                                  new_superficial_damage=3,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

    def test_new_health_state_vamp_injured_twice_superficial(self):
        # vampire Injured, then injured again superficially
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                  max_health=7,
                                                                  old_aggravated_damage=2,
                                                                  new_aggravated_damage=2,
                                                                  new_superficial_damage=3,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

    def test_new_health_state_vamp_injured_twice_agg(self):
        # vampire Injured, then injured again aggravated
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                  max_health=7,
                                                                  old_aggravated_damage=2,
                                                                  new_aggravated_damage=3,
                                                                  new_superficial_damage=3,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_INJURED)

    def test_new_health_state_vamp_injured_then_impaired(self):
        # Human injured, then takes damage and becomes impaired
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                  max_health=5,
                                                                  old_aggravated_damage=2,
                                                                  new_aggravated_damage=2,
                                                                  new_superficial_damage=3,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_IMPAIRED)

    def test_new_health_state_vamp_impaired_still(self):
        # Human injured, then takes damage and becomes impaired
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_IMPAIRED,
                                                                  max_health=5,
                                                                  old_aggravated_damage=2,
                                                                  new_aggravated_damage=4,
                                                                  new_superficial_damage=1,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_IMPAIRED)

    def test_new_health_state_vamp_injured_then_torpor(self):
        # vampire injured, then put into torpor
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_INJURED,
                                                                  max_health=5,
                                                                  old_aggravated_damage=2,
                                                                  new_aggravated_damage=5,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_TORPOR)

    def test_new_health_state_vamp_torpor_recovery(self):
        # vamps heal slowly in torpor but don't get better until they hit full HP
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_TORPOR,
                                                                  max_health=5,
                                                                  old_aggravated_damage=5,
                                                                  new_aggravated_damage=4,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_TORPOR)

    def test_new_health_state_vamp_return_from_torpor(self):
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_TORPOR,
                                                                  max_health=5,
                                                                  old_aggravated_damage=1,
                                                                  new_aggravated_damage=0,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_HEALTHY)

    def test_new_health_state_vamp_final_death_is_permanent(self):
        # Vamps that have met the final death, stay dead
        result_vamp = DamageCalculator.calculate_new_health_state(current_state=HEALTH_STATE_DEAD,
                                                                  max_health=5,
                                                                  old_aggravated_damage=5,
                                                                  new_aggravated_damage=6,
                                                                  new_superficial_damage=0,
                                                                  is_vampire=True)
        self.assertEqual(result_vamp, HEALTH_STATE_DEAD)

    def test_calculate_willpower_state_healthy(self):
        # full Willpower
        result = DamageCalculator.calculate_new_willpower_state(max_willpower=5,
                                                                new_aggravated_damage=0,
                                                                new_superficial_damage=0)

        self.assertEquals(result, WILLPOWER_STATE_HEALTHY)

    def test_calculate_willpower_state_healthy_superficial(self):
        # Willpower state is healthy until damage of both types added together exceeds the tracker
        result = DamageCalculator.calculate_new_willpower_state(max_willpower=5,
                                                                new_aggravated_damage=0,
                                                                new_superficial_damage=4)
        self.assertEquals(result, WILLPOWER_STATE_HEALTHY)

    def test_calculate_willpower_state_healthy_superficial_maxed(self):
        # When damage taken = willpower, we should get impaired
        result = DamageCalculator.calculate_new_willpower_state(max_willpower=5,
                                                                new_aggravated_damage=0,
                                                                new_superficial_damage=5)
        self.assertEquals(result, WILLPOWER_STATE_IMPAIRED)

    def test_calculate_willpower_state_impaired(self):
        # Aggravated damage shouldn't change this
        result = DamageCalculator.calculate_new_willpower_state(max_willpower=5,
                                                                new_aggravated_damage=1,
                                                                new_superficial_damage=4)
        self.assertEquals(result, WILLPOWER_STATE_IMPAIRED)

    def test_calculate_willpower_state_impaired_mixed(self):
        # Mixed damage should return impaired
        result = DamageCalculator.calculate_new_willpower_state(max_willpower=5,
                                                                new_aggravated_damage=3,
                                                                new_superficial_damage=2)
        self.assertEquals(result, WILLPOWER_STATE_IMPAIRED)

    def test_calculate_willpower_state_impaired_mixed_diff_max(self):
        # Max willpower shouldn't impact result
        result = DamageCalculator.calculate_new_willpower_state(max_willpower=7,
                                                                new_aggravated_damage=2,
                                                                new_superficial_damage=5)
        self.assertEquals(result, WILLPOWER_STATE_IMPAIRED)

    def test_calculate_superficial_damage_no_change(self):
        # Base case, no change
        aggravated, superficial = DamageCalculator.calculate_superficial_damage(max_value=5,
                                                                                aggravated_damage=0,
                                                                                superficial_damage=0,
                                                                                damage_taken=0)
        self.assertEquals(aggravated, 0)
        self.assertEquals(superficial, 0)

    def test_calculate_superficial_damage_superficial_taken(self):
        # Take 2 superficial from already having 2
        aggravated, superficial = DamageCalculator.calculate_superficial_damage(max_value=5,
                                                                                aggravated_damage=0,
                                                                                superficial_damage=0,
                                                                                damage_taken=2)
        self.assertEquals(aggravated, 0)
        self.assertEquals(superficial, 2)

    def test_calculate_superficial_damage_superficial_added(self):
        # Take 2 superficial from max hp
        aggravated, superficial = DamageCalculator.calculate_superficial_damage(max_value=5,
                                                                                aggravated_damage=0,
                                                                                superficial_damage=2,
                                                                                damage_taken=2)
        self.assertEquals(aggravated, 0)
        self.assertEquals(superficial, 4)

    def test_calculate_superficial_damage_overflows_to_aggravated(self):
        # Already taken superficial damage, further damage becomes aggravated
        aggravated, superficial = DamageCalculator.calculate_superficial_damage(max_value=5,
                                                                                aggravated_damage=0,
                                                                                superficial_damage=5,
                                                                                damage_taken=1)
        self.assertEquals(aggravated, 1)
        self.assertEquals(superficial, 4)

    def test_calculate_superficial_damage_overflow_from_full_hp(self):
        # Tests that from full HP/WP if a character takes a lot of superficial damage, it overflows
        aggravated, superficial = DamageCalculator.calculate_superficial_damage(max_value=5,
                                                                                aggravated_damage=0,
                                                                                superficial_damage=0,
                                                                                damage_taken=8)
        self.assertEquals(aggravated, 3)
        self.assertEquals(superficial, 2)

    def test_calculate_superficial_damage_overflow_diff_max(self):
        # Tests that max value doesn't impact the overflow
        aggravated, superficial = DamageCalculator.calculate_superficial_damage(max_value=7,
                                                                                aggravated_damage=0,
                                                                                superficial_damage=0,
                                                                                damage_taken=10)
        self.assertEquals(aggravated, 3)
        self.assertEquals(superficial, 4)

    def test_calculate_aggravated_damage_no_change(self):
        # Base case, no change
        aggravated, superficial = DamageCalculator.calculate_aggravated_damage(max_value=5,
                                                                               aggravated_damage=0,
                                                                               superficial_damage=0,
                                                                               damage_taken=0)
        self.assertEquals(aggravated, 0)
        self.assertEquals(superficial, 0)

    def test_calculate_aggravated_damage_agg_taken(self):
        # some points of damage taken
        aggravated, superficial = DamageCalculator.calculate_aggravated_damage(max_value=5,
                                                                               aggravated_damage=0,
                                                                               superficial_damage=0,
                                                                               damage_taken=3)
        self.assertEquals(aggravated, 3)
        self.assertEquals(superficial, 0)

    def test_calculate_aggravated_damage_agg_added(self):
        # Already taken a hit, take another
        aggravated, superficial = DamageCalculator.calculate_aggravated_damage(max_value=5,
                                                                               aggravated_damage=1,
                                                                               superficial_damage=0,
                                                                               damage_taken=1)
        self.assertEquals(aggravated, 2)
        self.assertEquals(superficial, 0)

    def test_calculate_aggravated_damage_with_superficial(self):
        # test that agg/superficial don't interfere
        aggravated, superficial = DamageCalculator.calculate_aggravated_damage(max_value=5,
                                                                               aggravated_damage=0,
                                                                               superficial_damage=2,
                                                                               damage_taken=1)
        self.assertEquals(aggravated, 1)
        self.assertEquals(superficial, 2)

    def test_calculate_aggravated_damage_with_superficial_and_agg(self):
        # test that agg/superficial don't interfere
        aggravated, superficial = DamageCalculator.calculate_aggravated_damage(max_value=5,
                                                                               aggravated_damage=1,
                                                                               superficial_damage=2,
                                                                               damage_taken=1)
        self.assertEquals(aggravated, 2)
        self.assertEquals(superficial, 2)

    def test_calculate_aggravated_damage_with_superficial_overflow(self):
        # When the character has superficial damage already, and the tracker is overfilled with agg, superficial
        # gets converted to agg.
        aggravated, superficial = DamageCalculator.calculate_aggravated_damage(max_value=5,
                                                                               aggravated_damage=0,
                                                                               superficial_damage=5,
                                                                               damage_taken=1)
        self.assertEquals(aggravated, 1)
        self.assertEquals(superficial, 4)

    def test_calculate_aggravated_damage_with_superficial_overflow_with_agg(self):
        # When the character has superficial damage already, and the tracker is overfilled with agg, superficial
        # gets converted to agg.
        aggravated, superficial = DamageCalculator.calculate_aggravated_damage(max_value=5,
                                                                               aggravated_damage=1,
                                                                               superficial_damage=4,
                                                                               damage_taken=1)
        self.assertEquals(aggravated, 2)
        self.assertEquals(superficial, 3)