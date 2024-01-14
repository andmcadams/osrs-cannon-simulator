from unittest import TestCase, main
from unittest.mock import Mock
from cannon_sim import *

def is_north_tile_walkable(strategy, coord, npc):
  return strategy.is_walkable_tile(coord, (coord[0], coord[1] + 1), npc)
def is_northeast_tile_walkable(strategy, coord, npc):
  return strategy.is_walkable_tile(coord, (coord[0] + 1, coord[1] + 1), npc)
def is_east_tile_walkable(strategy, coord, npc):
  return strategy.is_walkable_tile(coord, (coord[0] + 1, coord[1]), npc)
def is_southeast_tile_walkable(strategy, coord, npc):
  return strategy.is_walkable_tile(coord, (coord[0] + 1, coord[1] - 1), npc)
def is_south_tile_walkable(strategy, coord, npc):
  return strategy.is_walkable_tile(coord, (coord[0], coord[1] - 1), npc)
def is_southwest_tile_walkable(strategy, coord, npc):
  return strategy.is_walkable_tile(coord, (coord[0] - 1, coord[1] - 1), npc)
def is_west_tile_walkable(strategy, coord, npc):
  return strategy.is_walkable_tile(coord, (coord[0] - 1, coord[1]), npc)
def is_northwest_tile_walkable(strategy, coord, npc):
  return strategy.is_walkable_tile(coord, (coord[0] - 1, coord[1] + 1), npc)

class StubWalkabilityStrategy(WalkabilityStrategy):
  def __init__(self):
    self.map_registry = None

class StubHuntStrategy(HuntStrategy):
  def __init__(self):
    self.map_registry = None

class SimpleWalkabilityStrategyTest(TestCase):

  def setUp(self):
    self.npc = NpcRegistry().create_npc(0, 0, StubWalkabilityStrategy(), StubHuntStrategy())

  def test_is_walkable_tile_should_block_left_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.LEFT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_northeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_east_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_southeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_south_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_southwest_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_west_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_northwest_tile_walkable(strategy, coord, self.npc))

  def test_is_walkable_tile_should_block_top_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.TOP, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertFalse(is_north_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_northeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_east_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_southeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_south_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_southwest_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_west_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_northwest_tile_walkable(strategy, coord, self.npc))

  def test_is_walkable_tile_should_block_right_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.RIGHT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_northeast_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_east_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_southeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_south_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_southwest_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_west_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_northwest_tile_walkable(strategy, coord, self.npc))

  def test_is_walkable_tile_should_block_bottom_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.BOTTOM, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_northeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_east_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_southeast_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_south_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_southwest_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_west_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_northwest_tile_walkable(strategy, coord, self.npc))

  def test_is_walkable_tile_should_block_top_left_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.TOP_LEFT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_northeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_east_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_southeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_south_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_southwest_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_west_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_northwest_tile_walkable(strategy, coord, self.npc))

  def test_is_walkable_tile_should_block_top_right_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.TOP_RIGHT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_northeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_east_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_southeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_south_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_southwest_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_west_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_northwest_tile_walkable(strategy, coord, self.npc))

  def test_is_walkable_tile_should_block_bottom_right_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.BOTTOM_RIGHT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_northeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_east_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_southeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_south_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_southwest_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_west_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_northwest_tile_walkable(strategy, coord, self.npc))

  def test_is_walkable_tile_should_block_bottom_left_mask(self):
    map_registry = MapRegistry({ 0: { 0: {'movement_flags': Mask.BOTTOM_LEFT, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, NpcRegistry(), PlayerRegistry())
    coord = (0, 0)
    self.assertTrue(is_north_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_northeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_east_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_southeast_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_south_tile_walkable(strategy, coord, self.npc))
    self.assertFalse(is_southwest_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_west_tile_walkable(strategy, coord, self.npc))
    self.assertTrue(is_northwest_tile_walkable(strategy, coord, self.npc))

class LargeMonsterTest(TestCase):

  def test_is_walkable_blocks_large_monsters_with_object(self):
    npc_registry = NpcRegistry()
    npc = npc_registry.create_npc(0, 0, StubWalkabilityStrategy(), StubHuntStrategy(), opts={'size': 2})

    map_registry = MapRegistry({ 1: { 0: {'movement_flags': Mask.BOTTOM, 'projectile_flags': 0 } } })
    strategy = SimpleWalkabilityStrategy(map_registry, npc_registry, PlayerRegistry())
    coord = (0, 0)
    self.assertFalse(is_south_tile_walkable(strategy, coord, npc))
    self.assertFalse(is_southwest_tile_walkable(strategy, coord, npc))
    self.assertFalse(is_southeast_tile_walkable(strategy, coord, npc))

  def test_is_walkable_blocks_large_monsters_diagonally_with_npc(self):
    map_registry = MapRegistry({})
    blocking_tiles = [(-1, 0), (-1, 1), (0, -1), (1, -1), (-1, -1)]

    for i in range(len(blocking_tiles)):
      x, y = blocking_tiles[i]
      npc_registry = NpcRegistry()
      npc = npc_registry.create_npc(0, 0, StubWalkabilityStrategy(), StubHuntStrategy(), opts={'size': 2})
      npc_registry.create_npc(x, y, StubWalkabilityStrategy(),  StubHuntStrategy()) # Create the blocking npc

      strategy = SimpleWalkabilityStrategy(map_registry, npc_registry, PlayerRegistry())
      self.assertFalse(is_southwest_tile_walkable(strategy, npc.coordinate, npc))

  def test_is_walkable_blocks_large_monsters_diagonally_with_player(self):
    map_registry = MapRegistry({})
    blocking_tiles = [(-1, 0), (-1, 1), (0, -1), (1, -1), (-1, -1)]

    for i in range(len(blocking_tiles)):
      x, y = blocking_tiles[i]
      npc_registry = NpcRegistry()
      npc = npc_registry.create_npc(0, 0, StubWalkabilityStrategy(), StubHuntStrategy(), opts={'size': 2})
      player_registry = PlayerRegistry()
      player_registry.create_player((x, y), StubHuntStrategy()) # Create the blocking player

      strategy = SimpleWalkabilityStrategy(map_registry, npc_registry, player_registry)
      self.assertFalse(is_southwest_tile_walkable(strategy, npc.coordinate, npc))

  def test_can_attack_should_return_false_if_player_underneath(self):
    npc_registry = NpcRegistry()
    npc = npc_registry.create_npc(0, 0, StubWalkabilityStrategy(), StubHuntStrategy(), opts={'size': 2})
    tiles_under_npc = [(npc.coordinate[0] + i, npc.coordinate[1] + j) for i in range(npc.size) for j in range(npc.size)]

    for tile in tiles_under_npc:
      self.assertFalse(npc.can_attack(tile))

  def test_can_attack_should_return_true_if_player_around(self):
    npc_registry = NpcRegistry()
    npc = npc_registry.create_npc(0, 0, StubWalkabilityStrategy(), StubHuntStrategy(), opts={'size': 2})
    tiles_around_npc = [ (0, -1), (1, -1), (2, 0), (2, 1), (0, 2), (1, 2), (-1, 0), (-1, 1) ]

    for tile in tiles_around_npc:
      self.assertTrue(npc.can_attack(tile))

  def test_perform_move_should_not_move_if_able_to_attack_player(self):
    map_registry = MapRegistry({})
    blocking_tiles = [(-2, 0), (1, 0), (0, 1), (0, -2)]

    for i in range(len(blocking_tiles)):
      x, y = blocking_tiles[i]

      player_registry = PlayerRegistry()
      player = player_registry.create_player((0, 0), StubHuntStrategy())

      npc_registry = NpcRegistry()
      npc = npc_registry.create_npc(x, y, SimpleWalkabilityStrategy(map_registry, npc_registry, player_registry), SimpleHuntStrategy(map_registry, npc_registry, player_registry), opts={'size': 2})
      npc.set_interaction(player)
      npc.mode = NpcMode.PLAYERFOLLOW

      npc.perform_move()
      self.assertEqual(npc.coordinate, (x, y))
      self.assertEqual(npc.destination_tile, (x, y))

  def test_perform_move_should_path_if_able_to_attack_from_max_range(self):
    # This is an artifical test unless there is a 2x2 npc with maxrange 1 to test for accuracy
    npc_registry = NpcRegistry()
    npc = npc_registry.create_npc(0, 0, StubWalkabilityStrategy(), StubHuntStrategy(), opts={'size': 2, 'max_range': 1})
    attackable_area = [
      (-1, 3), (0, 3), (1, 3), (2, 3),
      (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2),
      (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1),
      (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0),
      (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1),
      (-1, -2), (0, -2), (1, -2), (2, -2)
    ]

    for tile in attackable_area:
      x, y = tile
      player_registry = PlayerRegistry()
      player = player_registry.create_player((x, y), StubHuntStrategy())
      if not npc.can_follow(player):
        import pdb; pdb.set_trace()
      self.assertTrue(npc.can_follow(player))
  
  def test_perform_move_should_not_path_if_not_able_to_attack_from_max_range(self):
    # This is an artifical test unless there is a 2x2 npc with maxrange 1 to test for accuracy
    npc_registry = NpcRegistry()
    npc = npc_registry.create_npc(0, 0, StubWalkabilityStrategy(), StubHuntStrategy(), opts={'size': 2, 'max_range': 1})
    attackable_area = [
      (-1, 3), (0, 3), (1, 3), (2, 3),
      (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2),
      (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1),
      (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0),
      (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1),
      (-1, -2), (0, -2), (1, -2), (2, -2)
    ]

    non_attackable_area = [(i, j) for i in range(-5, 5, 1) for j in range(-5, 5, 1) if (i, j) not in attackable_area]

    for tile in non_attackable_area:
      x, y = tile
      player_registry = PlayerRegistry()
      player = player_registry.create_player((x, y), StubHuntStrategy())
      self.assertFalse(npc.can_follow(player))

class NpcRegistryTest(TestCase):

  def setUp(self):
    self.npc_registry = NpcRegistry()
    self.walkability_strategy = WalkabilityStrategy(MapRegistry({}), self.npc_registry, PlayerRegistry())
    self.hunt_strategy = StubHuntStrategy()

  def test_registry_should_be_empty_initially(self):
    self.assertTrue(len(NpcRegistry().registered_npcs) == 0)

  def test_create_npc_should_add_to_registry(self):
    self.npc_registry.create_npc(0, 0, self.walkability_strategy, self.hunt_strategy)
    self.assertTrue(len(self.npc_registry.registered_npcs) == 1)

  def test_create_npc_should_return_npc(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy, self.hunt_strategy)
    self.assertEqual(npc.__class__, Npc)

  def test_create_npc_should_increment_slot_indices(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy, self.hunt_strategy)
    npc_2 = self.npc_registry.create_npc(0, 0, self.walkability_strategy, self.hunt_strategy)
    self.assertEqual(npc.slot_index, 0)
    self.assertEqual(npc_2.slot_index, 1)

  def test_create_npc_should_add_them_to_chunk(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy, self.hunt_strategy)
    self.assertListEqual(list(self.npc_registry.get_npcs_in_chunk(0, 0)), [npc])

  def test_create_npc_should_add_them_to_tiles(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy, self.hunt_strategy)
    self.assertListEqual(list(self.npc_registry.get_npcs_in_tile(0, 0)), [npc])

  def test_create_npc_should_add_larger_npcs_to_all_tiles(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy, self.hunt_strategy, opts={'size': 2})
    for (x, y) in [(0, 0), (1, 0), (0, 1), (1, 1)]:
      self.assertListEqual(list(self.npc_registry.get_npcs_in_tile(x, y)), [npc])

  def test_update_npc_should_update_tile_cache(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy, self.hunt_strategy)
    self.npc_registry.update_npc_location(npc, (0, 0), (0, 1))

    self.assertListEqual(list(self.npc_registry.get_npcs_in_tile(0, 1)), [npc])
    self.assertListEqual(list(self.npc_registry.get_npcs_in_tile(0, 0)), [])

  def test_update_npc_should_update_tile_cache_for_large_npcs(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy, self.hunt_strategy, opts={'size': 2})
    self.npc_registry.update_npc_location(npc, (0, 0), (0, 1))

    for (x, y) in [(0, 0), (1, 0)]:
      self.assertListEqual(list(self.npc_registry.get_npcs_in_tile(x, y)), [])
    for (x, y) in [(0, 1), (1, 1), (0, 2), (1, 2)]:
      self.assertListEqual(list(self.npc_registry.get_npcs_in_tile(x, y)), [npc])

  def test_create_npc_should_make_them_alive(self):
    npc = self.npc_registry.create_npc(0, 0, self.walkability_strategy, self.hunt_strategy)
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
    strat = CannonHuntStrategy(map_registry, npc_registry, player_registry)
    player = player_registry.create_player((0, 0), strat)
    cannon = player.place_cannon((0, 0))
    for i in range(8):
      for coord in self.get_possible_cannon_coords(cannon.direction):
        npc_registry.reset()
        npc = npc_registry.create_npc(coord[0], coord[1], WalkabilityStrategy(map_registry, npc_registry, player_registry), StubHuntStrategy())
        self.assertEqual(strat.get_target(cannon).slot_index, npc.slot_index)
      cannon.turn()

  def test_get_target_should_not_target_another_npc_in_single_combat(self):
    map_registry = MapRegistry({})
    player_registry = PlayerRegistry()
    npc_registry = NpcRegistry()
    strat = CannonHuntStrategy(map_registry, npc_registry, player_registry)

    player = player_registry.create_player((0, 0), strat)
    cannon = player.place_cannon((0, 0))
    npc = npc_registry.create_npc(-3, 0, StubWalkabilityStrategy(), StubHuntStrategy(), {'combat_level': 1})
    npc.is_in_multicombat = Mock(return_value=False) # Stub to avoid nil error

    # Player should be under attack
    player.in_combat_with = npc

    # Npc should be in singles in cannon range
    npc2 = npc_registry.create_npc(0, 3, StubWalkabilityStrategy(), StubHuntStrategy(), {'combat_level': 1})
    npc2.is_in_multicombat = Mock(return_value=False)

    self.assertIsNone(strat.get_target(cannon))

  def test_get_target_should_target_another_npc_in_multi_combat(self):
    map_registry = MapRegistry({})
    player_registry = PlayerRegistry()
    npc_registry = NpcRegistry()
    strat = CannonHuntStrategy(map_registry, npc_registry, player_registry)

    player = player_registry.create_player((0, 0), strat)
    cannon = player.place_cannon((0, 0))
    npc = npc_registry.create_npc(-3, 0, StubWalkabilityStrategy(), StubHuntStrategy(), {'combat_level': 1})
    npc.is_in_multicombat = Mock(return_value=True) # Stub to avoid nil error

    # Player should be under attack
    player.in_combat_with = npc

    # Npc should be in multi in cannon range
    npc2 = npc_registry.create_npc(0, 3, StubWalkabilityStrategy(), StubHuntStrategy(), opts={'combat_level': 1})
    npc2.is_in_multicombat = Mock(return_value=True)


    self.assertTrue(strat.get_target(cannon) == npc2)

class NpcInteractionTest(TestCase):

  def setUp(self):
    player_registry = PlayerRegistry()
    self.player = player_registry.create_player((0, 0), StubHuntStrategy())

    # Create an Npc focused on the player, standing next to the player
    self.npc_registry = NpcRegistry()
    self.npc = self.npc_registry.create_npc(0, 1, StubWalkabilityStrategy(), StubHuntStrategy())
    self.npc.set_interaction(self.player)
    self.npc.mode = NpcMode.PLAYERFOLLOW

  def test_interacting_with_player_in_combat_in_single_combat_should_deaggro(self):
    # The player is in a singles zone and in combat with another Npc
    self.player.is_in_multicombat = Mock(return_value=False)
    npc2 = self.npc_registry.create_npc(0, -1, StubWalkabilityStrategy(), StubHuntStrategy())
    self.player.in_combat_with = npc2

    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.WANDER)
    self.assertIsNone(self.npc.interacting_with)

  def test_interacting_with_player_in_combat_with_self_in_single_combat_should_stay_aggro(self):
    # The player is in a singles zone and in combat with this Npc
    self.player.is_in_multicombat = Mock(return_value=False)
    self.player.in_combat_with = self.npc

    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.PLAYERFOLLOW)
    self.assertEqual(self.npc.interacting_with, self.player)

  def test_interacting_with_player_not_in_combat_in_single_combat_should_stay_aggro(self):
    # The player is in a singles zone and in combat with nothing
    self.player.is_in_multicombat = Mock(return_value=False)
    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.PLAYERFOLLOW)
    self.assertEqual(self.npc.interacting_with, self.player)

  def test_interacting_with_player_in_combat_in_multi_combat_should_stay_aggro(self):
    # The player is in multi and in combat with another npc
    self.player.is_in_multicombat = Mock(return_value=True)
    npc2 = self.npc_registry.create_npc(0, -1, StubWalkabilityStrategy(), StubHuntStrategy())
    self.player.in_combat_with = npc2

    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.PLAYERFOLLOW)
    self.assertEqual(self.npc.interacting_with, self.player)

  def test_interacting_with_player_in_combat_with_self_in_multi_combat_should_stay_aggro(self):
    # The player is in multi and in combat with this Npc
    self.player.is_in_multicombat = Mock(return_value=True)
    self.player.in_combat_with = self.npc

    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.PLAYERFOLLOW)
    self.assertEqual(self.npc.interacting_with, self.player)

  def test_interacting_with_player_not_in_combat_in_multi_combat_should_stay_aggro(self):
    # The player is in multi and in combat with nothing
    self.player.is_in_multicombat = Mock(return_value=True)

    self.npc.perform_interact()

    self.assertEqual(self.npc.mode, NpcMode.PLAYERFOLLOW)
    self.assertEqual(self.npc.interacting_with, self.player)

class PlayerRetaliationTest(TestCase):

  def test_taking_damage_without_target_should_update_target(self):
    player = PlayerRegistry().create_player((0, 0), StubHuntStrategy())
    npc = NpcRegistry().create_npc(0, 0, StubWalkabilityStrategy(), StubHuntStrategy())
    player.add_to_queue(DamageAction(0, npc))

    player.perform_queue()

    self.assertTrue(player.is_in_combat_with(npc))
    self.assertEqual(player.time_to_next_attack, player.attack_speed//2)

  def test_taking_damage_with_target_should_keep_old_target(self):
    player = PlayerRegistry().create_player((0, 0), StubHuntStrategy())
    npc = NpcRegistry().create_npc(0, 0, StubWalkabilityStrategy(), StubHuntStrategy())
    player.in_combat_with = npc
    npc2 = NpcRegistry().create_npc(0, 0, StubWalkabilityStrategy(), StubHuntStrategy())
    player.add_to_queue(DamageAction(0, npc2))

    player.perform_queue()

    self.assertTrue(player.is_in_combat_with(npc))
    self.assertEqual(player.time_to_next_attack, 0)

if __name__ == '__main__':
  main()