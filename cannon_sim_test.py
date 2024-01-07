from unittest import TestCase, main
from unittest.mock import Mock
from cannon_sim import *

def is_north_tile_walkable(strategy, coord):
  return strategy.is_walkable_tile(coord, (coord[0], coord[1] + 1))
def is_northeast_tile_walkable(strategy, coord):
  return strategy.is_walkable_tile(coord, (coord[0] + 1, coord[1] + 1))
def is_east_tile_walkable(strategy, coord):
  return strategy.is_walkable_tile(coord, (coord[0] + 1, coord[1]))
def is_southeast_tile_walkable(strategy, coord):
  return strategy.is_walkable_tile(coord, (coord[0] + 1, coord[1] - 1))
def is_south_tile_walkable(strategy, coord):
  return strategy.is_walkable_tile(coord, (coord[0], coord[1] - 1))
def is_southwest_tile_walkable(strategy, coord):
  return strategy.is_walkable_tile(coord, (coord[0] - 1, coord[1] - 1))
def is_west_tile_walkable(strategy, coord):
  return strategy.is_walkable_tile(coord, (coord[0] - 1, coord[1]))
def is_northwest_tile_walkable(strategy, coord):
  return strategy.is_walkable_tile(coord, (coord[0] - 1, coord[1] + 1))

class SimpleWalkabilityStrategyTest(TestCase):

  def test_is_walkable_tile_should_block_left_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.LEFT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord))
    self.assertTrue(is_northeast_tile_walkable(strategy, coord))
    self.assertTrue(is_east_tile_walkable(strategy, coord))
    self.assertTrue(is_southeast_tile_walkable(strategy, coord))
    self.assertTrue(is_south_tile_walkable(strategy, coord))
    self.assertFalse(is_southwest_tile_walkable(strategy, coord))
    self.assertFalse(is_west_tile_walkable(strategy, coord))
    self.assertFalse(is_northwest_tile_walkable(strategy, coord))

  def test_is_walkable_tile_should_block_top_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.TOP, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertFalse(is_north_tile_walkable(strategy, coord))
    self.assertFalse(is_northeast_tile_walkable(strategy, coord))
    self.assertTrue(is_east_tile_walkable(strategy, coord))
    self.assertTrue(is_southeast_tile_walkable(strategy, coord))
    self.assertTrue(is_south_tile_walkable(strategy, coord))
    self.assertTrue(is_southwest_tile_walkable(strategy, coord))
    self.assertTrue(is_west_tile_walkable(strategy, coord))
    self.assertFalse(is_northwest_tile_walkable(strategy, coord))

  def test_is_walkable_tile_should_block_right_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.RIGHT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord))
    self.assertFalse(is_northeast_tile_walkable(strategy, coord))
    self.assertFalse(is_east_tile_walkable(strategy, coord))
    self.assertFalse(is_southeast_tile_walkable(strategy, coord))
    self.assertTrue(is_south_tile_walkable(strategy, coord))
    self.assertTrue(is_southwest_tile_walkable(strategy, coord))
    self.assertTrue(is_west_tile_walkable(strategy, coord))
    self.assertTrue(is_northwest_tile_walkable(strategy, coord))

  def test_is_walkable_tile_should_block_bottom_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.BOTTOM, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord))
    self.assertTrue(is_northeast_tile_walkable(strategy, coord))
    self.assertTrue(is_east_tile_walkable(strategy, coord))
    self.assertFalse(is_southeast_tile_walkable(strategy, coord))
    self.assertFalse(is_south_tile_walkable(strategy, coord))
    self.assertFalse(is_southwest_tile_walkable(strategy, coord))
    self.assertTrue(is_west_tile_walkable(strategy, coord))
    self.assertTrue(is_northwest_tile_walkable(strategy, coord))

  def test_is_walkable_tile_should_block_top_left_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.TOP_LEFT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord))
    self.assertTrue(is_northeast_tile_walkable(strategy, coord))
    self.assertTrue(is_east_tile_walkable(strategy, coord))
    self.assertTrue(is_southeast_tile_walkable(strategy, coord))
    self.assertTrue(is_south_tile_walkable(strategy, coord))
    self.assertTrue(is_southwest_tile_walkable(strategy, coord))
    self.assertTrue(is_west_tile_walkable(strategy, coord))
    self.assertFalse(is_northwest_tile_walkable(strategy, coord))

  def test_is_walkable_tile_should_block_top_right_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.TOP_RIGHT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord))
    self.assertFalse(is_northeast_tile_walkable(strategy, coord))
    self.assertTrue(is_east_tile_walkable(strategy, coord))
    self.assertTrue(is_southeast_tile_walkable(strategy, coord))
    self.assertTrue(is_south_tile_walkable(strategy, coord))
    self.assertTrue(is_southwest_tile_walkable(strategy, coord))
    self.assertTrue(is_west_tile_walkable(strategy, coord))
    self.assertTrue(is_northwest_tile_walkable(strategy, coord))

  def test_is_walkable_tile_should_block_bottom_right_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.BOTTOM_RIGHT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord))
    self.assertTrue(is_northeast_tile_walkable(strategy, coord))
    self.assertTrue(is_east_tile_walkable(strategy, coord))
    self.assertFalse(is_southeast_tile_walkable(strategy, coord))
    self.assertTrue(is_south_tile_walkable(strategy, coord))
    self.assertTrue(is_southwest_tile_walkable(strategy, coord))
    self.assertTrue(is_west_tile_walkable(strategy, coord))
    self.assertTrue(is_northwest_tile_walkable(strategy, coord))

  def test_is_walkable_tile_should_block_bottom_left_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.BOTTOM_LEFT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord))
    self.assertTrue(is_northeast_tile_walkable(strategy, coord))
    self.assertTrue(is_east_tile_walkable(strategy, coord))
    self.assertTrue(is_southeast_tile_walkable(strategy, coord))
    self.assertTrue(is_south_tile_walkable(strategy, coord))
    self.assertFalse(is_southwest_tile_walkable(strategy, coord))
    self.assertTrue(is_west_tile_walkable(strategy, coord))
    self.assertTrue(is_northwest_tile_walkable(strategy, coord))

class NpcRegistryTest(TestCase):

  def setUp(self):
    self.npc_registry = NpcRegistry()
    self.walkability_strategy = WalkabilityStrategy(MapRegistry({}), self.npc_registry, PlayerRegistry())

  def test_registry_should_be_empty_initially(self):
    self.assertTrue(len(NpcRegistry().registered_npcs) == 0)

  def test_create_npc_should_add_to_registry(self):
    self.npc_registry.create_npc(0, 0, self.walkability_strategy)
    self.assertTrue(len(self.npc_registry.registered_npcs) == 1)

  def test_create_npc_should_return_npc(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy)
    self.assertEqual(npc.__class__, Npc)

  def test_create_npc_should_increment_slot_indices(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy)
    npc_2 = self.npc_registry.create_npc(0, 0, self.walkability_strategy)
    self.assertEqual(npc.slot_index, 0)
    self.assertEqual(npc_2.slot_index, 1)

  def test_create_npc_should_add_them_to_chunk(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy)
    self.assertListEqual(list(self.npc_registry.get_npcs_in_chunk(0, 0)), [npc])

  def test_create_npc_should_make_them_alive(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy)
    self.assertListEqual(list(self.npc_registry.get_living_npcs_in_chunk(0, 0)), [npc])

class CannonHuntStrategyTest(TestCase):
  # Construct a bunch of real life test cases to make sure they work as expected
  def get_possible_cannon_coords(self, direction: Tuple[int, int]):
    coords = []
    if (direction[0] + direction[1]) % 2 == 1:
      # 3x3 around (3, 0) +- 1 in each dir
      for i in range(-1, 1):
        for j in range(-1, 1):
          coords.append((3*direction[0]+i, 3*direction[1]+j))
      # 5x5 around (7, 0) +-2 in each dir
      for i in range(-2, 2):
        for j in range(-2, 2):
          coords.append((7*direction[0]+i, 7*direction[1]+j))
      # 11x11 around (14, 0) +-5 in each dir
      for i in range(-5, 5):
        for j in range(-5, 5):
          coords.append((14*direction[0]+i, 14*direction[1]+j))
    else:
      # 3x3 around (3, 0) +- 1 in each dir
      for i in range(-1, 1):
        for j in range(-1, 1):
          coords.append((2*direction[0]+i, 2*direction[1]+j))
      # 5x5 around (7, 0) +-2 in each dir
      for i in range(-2, 2):
        for j in range(-2, 2):
          coords.append((5*direction[0]+i, 5*direction[1]+j))
      # 11x11 around (14, 0) +-5 in each dir
      for i in range(-5, 5):
        for j in range(-5, 5):
          coords.append((12*direction[0]+i, 12*direction[1]+j))
    return coords

  # Best case scenario. Assume no objects are in the way
  def test_get_target_should_hit_all_basic_spots(self):
    map_registry = MapRegistry({})
    player_registry = PlayerRegistry()
    npc_registry = NpcRegistry()
    strat = CannonHuntStrategy(npc_registry, map_registry, player_registry)
    player = player_registry.create_player((0, 0), strat)
    cannon = player.place_cannon((0, 0))
    for i in range(8):
      for coord in self.get_possible_cannon_coords(cannon.direction):
        npc_registry.reset()
        npc = npc_registry.create_npc(coord[0], coord[1], WalkabilityStrategy(map_registry, npc_registry, player_registry))
        self.assertEqual(strat.get_target(cannon).slot_index, npc.slot_index)
      cannon.turn()

class StubWalkabilityStrategy(WalkabilityStrategy):
  def __init__(self):
    self.map_registry = None

class SingleCombatTest(TestCase):

  def setUp(self):
    player_registry = PlayerRegistry()
    self.player = player_registry.create_player((0, 0), None)

    # Create an Npc focused on the player, standing next to the player
    self.npc_registry = NpcRegistry()
    self.npc = self.npc_registry.create_npc(0, 1, StubWalkabilityStrategy())
    self.npc.set_interaction(self.player)
    self.npc.mode = NpcMode.PLAYERFOLLOW

  def test_interacting_with_player_in_combat_in_single_combat_should_deaggro(self):
    # The player is in a singles zone and in combat with another Npc
    self.npc.is_in_multicombat = Mock(return_value=False)
    npc2 = self.npc_registry.create_npc(0, -1, StubWalkabilityStrategy())
    self.player.in_combat_with = npc2

    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.WANDER)
    self.assertIsNone(self.npc.interacting_with)

  def test_interacting_with_player_in_combat_with_self_in_single_combat_should_stay_aggro(self):
    # The player is in a singles zone and in combat with this Npc
    self.npc.is_in_multicombat = Mock(return_value=False)
    self.player.in_combat_with = self.npc

    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.PLAYERFOLLOW)
    self.assertEqual(self.npc.interacting_with, self.player)

  def test_interacting_with_player_not_in_combat_in_single_combat_should_stay_aggro(self):
    # The player is in a singles zone and in combat with nothing
    self.npc.is_in_multicombat = Mock(return_value=False)
    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.PLAYERFOLLOW)
    self.assertEqual(self.npc.interacting_with, self.player)

  def test_interacting_with_player_in_combat_in_multi_combat_should_stay_aggro(self):
    # The player is in multi and in combat with another npc
    self.npc.is_in_multicombat = Mock(return_value=True)
    npc2 = self.npc_registry.create_npc(0, -1, StubWalkabilityStrategy())
    self.player.in_combat_with = npc2

    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.PLAYERFOLLOW)
    self.assertEqual(self.npc.interacting_with, self.player)

  def test_interacting_with_player_in_combat_with_self_in_multi_combat_should_stay_aggro(self):
    # The player is in multi and in combat with this Npc
    self.npc.is_in_multicombat = Mock(return_value=True)
    self.player.in_combat_with = self.npc

    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.PLAYERFOLLOW)
    self.assertEqual(self.npc.interacting_with, self.player)

  def test_interacting_with_player_not_in_combat_in_multi_combat_should_stay_aggro(self):
    # The player is in multi and in combat with nothing
    self.npc.is_in_multicombat = Mock(return_value=True)

    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.PLAYERFOLLOW)
    self.assertEqual(self.npc.interacting_with, self.player)

if __name__ == '__main__':
  main()