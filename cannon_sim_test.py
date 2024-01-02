from unittest import TestCase, main, skip
from cannon_sim import *

@skip
class SimpleWalkabilityStrategyTest(TestCase):

  def setUp(self):
    npc_registry = NpcRegistry()
    player_registry = PlayerRegistry()
    map_config = {
      1: {
        0: [{'name': 'Wall', 'movement_flags': Mask.RIGHT, 'blocks_projectiles': True }]
      },
      3: {
        0: [{'name': 'Wall', 'movement_flags': Mask.LEFT, 'blocks_projectiles': True }]
      },
      5: {
        0: [{'name': 'Wall', 'movement_flags': Mask.BOTTOM, 'blocks_projectiles': True }]
      },
      7: {
        0: [{'name': 'Wall', 'movement_flags': Mask.TOP, 'blocks_projectiles': True }]
      },
    }
    map_registry = MapRegistry(map_config)
    self.strategy = SimpleWalkabilityStrategy(map_registry, npc_registry, player_registry)

  def test_is_walkable_tile_should_block_east_movement(self):
    self.assertFalse(self.strategy.is_walkable_tile((0, 0), (1, 0)))

  def test_is_walkable_tile_should_block_west_movement(self):
    self.assertFalse(self.strategy.is_walkable_tile((4, 0), (3, 0)))

class NpcRegistryTest(TestCase):

  def test_registry_should_be_empty_initially(self):
    self.assertTrue(len(NpcRegistry().registered_npcs) == 0)

  def test_create_npc_should_add_to_registry(self):
    registry = NpcRegistry()
    registry.create_npc(0, 0, None)
    self.assertTrue(len(registry.registered_npcs) == 1)

  def test_create_npc_should_return_npc(self):
    registry = NpcRegistry()
    npc = registry.create_npc(0, 0, None)
    self.assertEqual(npc.__class__, Npc)

  def test_create_npc_should_increment_slot_indices(self):
    registry = NpcRegistry()
    npc = registry.create_npc(0, 0, None)
    npc_2 = registry.create_npc(0, 0, None)
    self.assertEqual(npc.slot_index, 0)
    self.assertEqual(npc_2.slot_index, 1)

  def test_create_npc_should_add_them_to_chunk(self):
    registry = NpcRegistry()
    npc = registry.create_npc(0, 0, None)
    self.assertListEqual(list(registry.get_npcs_in_chunk(0, 0)), [npc])

  def test_create_npc_should_make_them_alive(self):
    registry = NpcRegistry()
    npc = registry.create_npc(0, 0, None)
    self.assertListEqual(list(registry.get_living_npcs_in_chunk(0, 0)), [npc])

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
        npc = npc_registry.create_npc(coord[0], coord[1], None)
        self.assertEqual(strat.get_target(cannon).slot_index, npc.slot_index)
      cannon.turn()

  def test_get_target_should_not_go_through_walls(self):
    pass

if __name__ == '__main__':
  main()