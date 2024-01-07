import math
import random
from create_map import Mask, create_map_config
from typing import Tuple
from create_map import relevant_npcs

DEBUG = False
# Keep track of Npc movements, can be very memory intensive over long sims
DEBUG_NPC_PATHING = False
def debug(msg):
  if DEBUG == True:
    print(msg)

def cheb(point1, point2):
  return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

def euclidean(point1, point2):
  return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


class Engine:
  def __init__(self, map_registry, npc_registry, player_registry) -> None:
    self.map_registry = map_registry
    self.npc_registry = npc_registry
    self.player_registry = player_registry
    pass

  def perform_ticks(self, ticks):
    for _ in range(ticks):
      self.perform_tick()

  def perform_tick(self):
    # Process client input
    for npc in self.npc_registry.registered_npcs:
      # Each npc do
      #   stalls end
      npc.perform_timers()
      #   * queue (take damage)
      npc.perform_queue()
      #   interaction with items/objects
      #   * movement
      npc.perform_move()
      #   * interaction with players/npcs (determine pathing the next tick?)
      npc.perform_interact()

    # Does this matter at all for a v0? prob not
    for player in self.player_registry.registered_players:
      # Each player do
      #   stalls end
      #   queue (take damage)
      #   timers (poison?)
      player.perform_timers() # This fires the cannon
      #   area queue
      #   interaction with items/objects
      #   * (not v0) movement
      #   * (not v0) interaction with players/npcs

class Action:
  def act_on(self, entity):
    raise NotImplementedError

class DamageAction(Action):
  def __init__(self, damage: int, attacker: 'Player'):
    self.damage = damage
    self.attacker = attacker

  def act_on(self, npc: 'Npc'):
    npc.take_damage(self.damage, self.attacker)

class WalkabilityStrategy:
  def __init__(self, map_registry, npc_registry, player_registry) -> None:
    self.map_registry = map_registry
    self.npc_registry = npc_registry
    self.player_registry = player_registry

  def is_walkable_tile(self, old_coord, new_coord):
    raise NotImplementedError

class SimpleWalkabilityStrategy(WalkabilityStrategy):
  def _blocks_direction(self, direction, blockers):

    moving = 0
    if direction[0] == 1:
      moving |= Mask.RIGHT
    if direction[0] == -1:
      moving |= Mask.LEFT
    if direction[1] == 1:
      moving |= Mask.TOP
    if direction[1] == -1:
      moving |= Mask.BOTTOM

    if direction[0] == 1 and direction [1] == 1:
      moving |= Mask.TOP_RIGHT
    if direction[0] == -1 and direction [1] == 1:
      moving |= Mask.TOP_LEFT
    if direction[0] == 1 and direction [1] == -1:
      moving |= Mask.BOTTOM_RIGHT
    if direction[0] == -1 and direction [1] == -1:
      moving |= Mask.BOTTOM_LEFT

    return bool(blockers & moving)


  def _are_objects_blocking(self, old_coord, new_coord):
    direction = (new_coord[0] - old_coord[0], new_coord[1] - old_coord[1])
    flags = self.map_registry.get_objs(old_coord).get('movement_flags', 0)
    if self._blocks_direction(direction, flags):
      return True
    if direction[0] != 0 and direction[1] != 0:
      # If trying to go diagonally, check both components
      # This is probably worth precomputing with flags
      if self.is_walkable_tile(old_coord, (old_coord[0] + direction[0], old_coord[1])) is False:
        return True
      if self.is_walkable_tile((old_coord[0] + direction[0], old_coord[1]), new_coord) is False:
        return True
      if self.is_walkable_tile(old_coord, (old_coord[0], old_coord[1] + direction[1])) is False:
        return True
      if self.is_walkable_tile((old_coord[0], old_coord[1] + direction[1]), new_coord) is False:
        return True
    return False

  def is_walkable_tile(self, old_coord, new_coord):
    # Not walkable if there is an npc there or object that restricts movement
    for npc in self.npc_registry.get_living_npcs_in_chunk_by_abs_coordinate(new_coord):
      # TODO: Allow if the transparent flag is set
      # TODO: Should this account for the Npc trying to walk on itself?
      if npc.coordinate == new_coord:
        return False

    # Is there something on the current tile blocking me?
    if self._are_objects_blocking(old_coord, new_coord):
      return False

    # Is there something on the new tile blocking me?
    if self._are_objects_blocking(new_coord, old_coord):
      return False

    return True

from collections import defaultdict
class NpcRegistry:
  def __init__(self) -> None:
    self._initialize_state()

  def _initialize_state(self):
    # Give us a clean slate to work from
    self._npcs = []
    self.current_slot = 0
    self.npc_chunk_lookup = defaultdict(lambda: defaultdict(dict))

  def reset(self):
    self._initialize_state()

  @property
  def registered_npcs(self):
    return self._npcs

  def create_npc(self, x, y, walkability_strategy, opts={}):
    npc = Npc(self._next_slot(), x, y, self, walkability_strategy, opts)

    # Add them to the chunk for tracking
    chunk = self._get_chunk(x, y)
    self._add_to_chunk(npc, chunk[0], chunk[1])

    # Add to registered npc list
    self._npcs.append(npc)

    return npc

  def get_npcs_in_chunk(self, chunk_x, chunk_y):
    return self.npc_chunk_lookup[chunk_x][chunk_y].values()

  def get_living_npcs_in_chunk(self, chunk_x, chunk_y):
    return [n for n in self.get_npcs_in_chunk(chunk_x, chunk_y) if n.is_dead() is False]

  def get_living_npcs_in_chunk_by_abs_coordinate(self, coordinate):
    chunk = self._get_chunk(coordinate[0], coordinate[1])
    return self.get_living_npcs_in_chunk(chunk[0], chunk[1])

  def update_npc_location(self, npc, old_coord, new_coord):
    old_chunk = self._get_chunk(old_coord[0], old_coord[1])
    new_chunk = self._get_chunk(new_coord[0], new_coord[1])
    if new_chunk != old_chunk:
      self._remove_from_chunk(npc, old_chunk[0], old_chunk[1])
      self._add_to_chunk(npc, new_chunk[0], new_chunk[1])

  def get_npc_stats(self, npc_struct):
    npc_id = npc_struct['id']
    if npc_id in [3269, 11942, 11943, 11944, 3270, 11945, 3271, 11946, 11947, 3273, 3274]:
      return {'id': npc_id, 'max_range': 4, 'wander_range': 2, 'hitpoints': 22, 'combat_level': 10, 'name': 'Guard'}
    return {'id': npc_id, 'combat_level': 0 }

  def _add_to_chunk(self, npc, chunk_x, chunk_y):
    self.npc_chunk_lookup[chunk_x][chunk_y][npc.slot_index] = npc

  def _remove_from_chunk(self, npc, chunk_x, chunk_y):
    self.npc_chunk_lookup[chunk_x][chunk_y].pop(npc.slot_index, None)

  def _get_chunk(self, x, y):
    return (x // 8, y // 8)

  def _next_slot(self):
    slot_index = self.current_slot
    self.current_slot += 1
    return slot_index


from enum import Enum
class NpcMode(Enum):
  WANDER = 1
  PATROL = 2
  PLAYERESCAPE = 3
  PLAYERFOLLOW = 4
  PLAYERFACE = 5
  PLAYERFACECLOSE = 6

class NpcMovement:
  def __init__(self, start_coord, end_coord, destination_tile, successful):
    self.start_coord = start_coord
    self.end_coord = end_coord
    self.destination_tile = destination_tile
    self.successful = successful


class Npc:
  def __init__(self, slot_index: int, x: int, y: int, npc_registry, walkability_strategy, opts={}):
    self.queue = []
    self.slot_index = slot_index
    self._x = x
    self._y = y
    self.respawn_coordinate = (x, y)
    self.travel_path = []

    self.npc_registry = npc_registry
    self.walkability_strategy = walkability_strategy
    self.npc_id = opts.get('id', None)
    self.name = opts.get('name', f'Npc {self.slot_index}{" (id: " + str(self.npc_id) + ")" if self.npc_id else ""}')
    self.max_hitpoints = opts.get('hitpoints', 1)
    self._combat_level = opts.get('combat_level', 1)
    self.respawn_time = opts.get('respawn_time', 50) # 50 tick respawn time, will be dependent on monster
    self.wanderrange = opts.get('wander_range', 5) # No clue what the default is here
    self.maxrange = opts.get('max_range', 8) # No clue what the default is here
    self.respawn()
    self.times_died = 0

  def is_dead(self):
    return self._is_dead

  def is_attackable(self):
    return self._combat_level != 0

  def respawn(self):
    self._is_dead = False
    self.hitpoints = self.max_hitpoints
    self.respawn_time_remaining = None
    # Move to its respawn location
    self._coordinate = self.respawn_coordinate
    # Reset destination tile, might be changed later in the tick
    self._destination_tile = self.respawn_coordinate
    self._mode = NpcMode.WANDER
    self.set_interaction(None)

  def die(self):
    self._is_dead = True
    self.hitpoints = 0
    self.respawn_time_remaining = self.respawn_time
    # TODO: Does the queue actually get cleared on death? Is there a death queue? Do we care here?
    self.queue = []
    self.times_died += 1
    self.set_interaction(None)

  def perform_timers(self):
    # Respawn timer
    if self.is_dead():
      self.respawn_time_remaining -= 1
      if self.respawn_time_remaining == 0:
        self.respawn()

  def add_to_queue(self, action: Action):
    self.queue.append(action)

  def perform_queue(self):
    new_queue = []
    for action in self.queue:
      # If action causes the npc to die, the queue will clear and we need to break
      action.act_on(self)
      if self.is_dead():
        break
    self.queue = new_queue

  def take_damage(self, amount, attacker):
    damage_taken = min(amount, self.hitpoints)
    self.hitpoints -= damage_taken
    if self.interacting_with is None:
      self.set_interaction(attacker)
    
    if self.interacting_with == attacker:
      if self.can_attack(attacker):
        self.mode = NpcMode.PLAYERFOLLOW
      else:
        self.mode = NpcMode.PLAYERESCAPE

    debug(f'Npc {self.slot_index} took {damage_taken} damage (hit a {amount})')
    if self.hitpoints <= 0:
      self.die()
    debug(f'Npc {self.slot_index} hitpoints remaining: {self.hitpoints}')
  
  def set_interaction(self, entity):
    if entity:
      debug(f'Npc {self.slot_index} interacting with new entity {entity}')
    self.interacting_with = entity

  def can_attack(self, player: 'Player'):
    # MELEE (non halberd)
    dist_x = player.coordinate[0] - self.respawn_coordinate[0]
    dist_y = player.coordinate[1] - self.respawn_coordinate[1]
    if dist_x >= dist_y:
      dist_x -= 1
    else:
      dist_y -= 1
    if max(dist_x, dist_y) <= self.maxrange:
      return True

    # TODO: Add case for range/mage/long melee

    return False

  @property
  def mode(self):
    return self._mode

  @mode.setter
  def mode(self, mode):
    if mode != self._mode:
      debug(f'Npc {self.slot_index} mode changed to {mode.name}')
    self._mode = mode

  def perform_move(self):
    if self.is_dead():
      return
    # TODO: Does dest tile change happen before or after movement? Seems to be before based on gech message

    # Choose dest tile based on strategy
    if self.mode == NpcMode.WANDER:
      self.wander()
    if self.mode == NpcMode.PLAYERESCAPE:
      self.retreat()
    if self.mode == NpcMode.PLAYERFOLLOW:
      self.follow()
    # Move
    self.move()

  def retreat(self):
    # Set dest tile to one of the maxrange corners based on relative location to player
    player = self.interacting_with
    distance_x = self.x - player.x # If positive, npc is to the EAST
    distance_y = self.y - player.y # If positive, npc is to the NORTH

    # Else cases have been confirmed here
    if distance_x > 0: # PLAYER IS WEST
      if distance_y > 0: # PLAYER IS SOUTH
        delta = (self.maxrange, self.maxrange) # NORTH EAST CORNER
      else: # PLAYER IS NORTH/EVEN
        delta = (self.maxrange, -self.maxrange) # SOUTH EAST CORNER
    else: # PLAYER IS EAST/EVEN
      if distance_y > 0: # PLAYER IS SOUTH
        delta = (-self.maxrange, self.maxrange) # NORTH WEST CORNER
      else: # PLAYER IS NORTH/EVEN
        delta = (-self.maxrange, -self.maxrange) # SOUTH WEST CORNER
    self.destination_tile = (self.respawn_coordinate[0] + delta[0], self.respawn_coordinate[1] + delta[1])

  def wander(self):
    should_pick_new_dest = random.randint(0, 7) == 0
    if should_pick_new_dest:
      self.destination_tile = (random.randint(-self.wanderrange, self.wanderrange) + self.respawn_coordinate[0], random.randint(-self.wanderrange, self.wanderrange) + self.respawn_coordinate[1])

  def follow(self):
    # Assumes the destination tile is one of the ones next to the player
    x = self.interacting_with.x
    y = self.interacting_with.y
    north_tile = (x, y+1)
    south_tile = (x, y-1)
    east_tile = (x+1, y)
    west_tile = (x-1, y)

    # If they are the same coordinate, choose a random tile
    if cheb(self.interacting_with.coordinate, self.coordinate) == 0:
      direction = 1 if random.random() < 0.5 else -1
      if random.random() < 0.5:
        (x+direction, y)
      else:
        (x, y+direction)

    north_tile_distance = cheb(north_tile, self.coordinate)
    south_tile_distance = cheb(south_tile, self.coordinate)
    east_tile_distance = cheb(east_tile, self.coordinate)
    west_tile_distance = cheb(west_tile, self.coordinate)
    
    min_dist = min(north_tile_distance, south_tile_distance, east_tile_distance, west_tile_distance)
    # Order of checks here is important since an Npc on the NE/NW tile will path to the N tile and SE/SW paths S
    if min_dist == north_tile_distance:
      self.destination_tile = north_tile
    elif min_dist == south_tile_distance:
      self.destination_tile = south_tile
    elif min_dist == east_tile_distance:
      self.destination_tile = east_tile
    else:
      self.destination_tile = west_tile

  def move(self):
    # Moving to the destination
    def get_delta(start_val, dest_val):
      if start_val == dest_val:
        return 0
      elif start_val > dest_val:
        return -1
      else:
        return 1
    dx = get_delta(self.x, self.destination_tile[0])
    dy = get_delta(self.y, self.destination_tile[1])
    
    if dx == 0 and dy == 0:
      debug(f'Npc {self.slot_index} is at destination tile already')
      if DEBUG_NPC_PATHING:
        self.travel_path.append(NpcMovement(self._coordinate, self._coordinate, self.destination_tile, self.mode.name))
      return

    new_coordinate = None
    # Attempt to move to the destination tile
    if self.walkability_strategy.is_walkable_tile(self.coordinate, (self.x + dx, self.y + dy)):
      new_coordinate = (self.x + dx, self.y + dy)
    elif dx != 0 and dy != 0:
      # If we were trying to go diagonally, but cant, try E/W followed by N/S
      if self.walkability_strategy.is_walkable_tile(self.coordinate, (self.x + dx, self.y)):
        new_coordinate =  (self.x + dx, self.y)
      elif self.walkability_strategy.is_walkable_tile(self.coordinate, (self.x, self.y + dy)):
        new_coordinate =  (self.x, self.y + dy)

    if DEBUG_NPC_PATHING:
      self.travel_path.append(NpcMovement(self._coordinate, new_coordinate, self.destination_tile, self.mode.name))
    if new_coordinate:
      self._coordinate = new_coordinate
    else:
      debug(f'Npc {self.slot_index} is stuck!')

  def perform_interact(self):
    if self.is_dead():
      return
    # TODO: Target the player
    pass

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  @property
  def coordinate(self):
    return (self.x, self.y)

  @coordinate.setter
  def _coordinate(self, coord: Tuple[int, int]):
    self.npc_registry.update_npc_location(self, self.coordinate, coord)
    self._x = coord[0]
    self._y = coord[1]

  @property
  def destination_tile(self):
    return self._destination_tile

  @destination_tile.setter
  def destination_tile(self, coord: Tuple[int, int] | None):
    if coord != self._destination_tile:
      debug(f'NPC {self.slot_index} picked a new coord as dest {coord} while in mode {self.mode.name}')
      self._destination_tile = coord

class HuntStrategy:
  def __init__(self, npc_registry, map_registry, player_registry):
    self.npc_registry = npc_registry
    self.map_registry = map_registry
    self.player_registry = player_registry

  def get_target(self, hunter):
    raise NotImplementedError

  def _zero_fill_right_shift(self, val, n):
    return (val >> n) if val >= 0 else ((val + 0x100000000) >> n)

  def has_line_of_sight(self, coord, end_coord):
    # Code is a translation of Runelite's code here:
    # https://github.com/runelite/runelite/blob/28821c16effced33780da52dccbb69e5757b63e2/runelite-api/src/main/java/net/runelite/api/coords/WorldArea.java#L570
    # TODO: Some sort of plane check to handle multiple planes
    # TODO: If you're inside an object, fail immediately

    if coord == end_coord:
      return True

    dx = end_coord[0] - coord[0]
    dy = end_coord[1] - coord[1]
    dx_abs = abs(dx)
    dy_abs = abs(dy)
    x_flags = 0
    y_flags = 0

    if dx < 0:
      x_flags |= Mask.RIGHT
    else:
      x_flags |= Mask.LEFT
    if dy < 0:
      y_flags |= Mask.TOP
    else:
      y_flags |= Mask.BOTTOM

    if dx_abs > dy_abs:
      x = coord[0]
      y_big = coord[1] << 16
      slope = (dy << 16) // dx_abs
      y_big += 0x8000
      y_big -= 1 if dy < 0 else 0
      direction = -1 if dx < 0 else 1
      while x != end_coord[0]:
        x += direction
        y = self._zero_fill_right_shift(y_big, 16)
        if self.map_registry.get_objs((x, y)).get('projectile_flags', 0) & x_flags != 0:
          # Hit something on the x axis
          return False
        y_big += slope
        next_y = self._zero_fill_right_shift(y_big, 16)
        if next_y != y and self.map_registry.get_objs((x, next_y)).get('projectile_flags', 0) & y_flags != 0:
          # Hit something on the y axis
          return False
    else:
      y = coord[1]
      x_big = coord[0] << 16
      slope = (dx << 16) // dy_abs
      x_big += 0x8000
      x_big -= 1 if dx < 0 else 0
      direction = -1 if dy < 0 else 1
      while y != end_coord[1]:
        y += direction
        x = self._zero_fill_right_shift(x_big, 16)

        if self.map_registry.get_objs((x, y)).get('projectile_flags', 0) & y_flags != 0:
          # Hit something on the y axis
          return False
        x_big += slope
        next_x = self._zero_fill_right_shift(x_big, 16)
        if next_x != x and self.map_registry.get_objs((next_x, y)).get('projectile_flags', 0) & x_flags != 0:
          # Hit something on the x axis
          return False
    return True


class CannonHuntStrategy(HuntStrategy):
  def has_line_of_sight(self, cannon_center, area_center, npc_coordinate):
    # Cannon LOS is weird. Needs LOS to the center spot it is targeting
    # and LOS from center spot to the target

    if not super().has_line_of_sight(cannon_center, npc_coordinate):
      return False
    if not super().has_line_of_sight(area_center, npc_coordinate):
      return False

    return True
  
  def get_target(self, cannon):
    origin = cannon.coordinate
    direction = cannon.direction
    # Cook code ahead
    ordinal_cannon_distances = [2, 5, 12]
    cardinal_cannon_distances = [3, 7, 14]
    cannon_ranges = [1, 2, 5]

    is_cardinal = (direction[0] + direction[1]) % 2 != 0
    distances = cardinal_cannon_distances if is_cardinal else ordinal_cannon_distances
    for i in range(3):
      center = (origin[0] + direction[0] * distances[i], origin[1] + direction[1] * distances[i])
      center_chunk = (center[0]//8, center[1]//8)

      npcs_in_range = []
      for x_chunk_offset in [1, 0, -1]:
        for y_chunk_offset in [1, 0, -1]:
          chunk = (center_chunk[0] + x_chunk_offset, center_chunk[1] + y_chunk_offset)
          for npc in self.npc_registry.get_living_npcs_in_chunk(chunk[0], chunk[1]):
            if npc.is_attackable():
              if cheb(center, npc.coordinate) <= cannon_ranges[i]:
                npcs_in_range.append(npc)
      npcs_in_range.sort(key=lambda npc: euclidean(center, npc.coordinate))

      if len(npcs_in_range) > 0:
        # The LOS check seems to happen after selecting a target, and if that target can't be hit the cannon does not fire
        target_npc = npcs_in_range[0]
        if self.has_line_of_sight(origin, center, target_npc.coordinate):
          return target_npc
        return None

    return None

class Cannon:

  # Cannon LOS is checked from center of cannon and center of checked area
  def __init__(self, x: int, y: int, player: 'Player', hunt_strategy: HuntStrategy):
    self._x = x
    self._y = y
    self.player = player
    # X, Y (positive is right and up resp.)
    self.direction = (0, 1)
    self.hunt_strategy = hunt_strategy

    self.MOVEMENTS = {
      0: {1: (1, 1), -1: (-1, -1)},
      1: {1: (1, 0), 0: (1, -1), -1: (0, -1)},
      -1: {-1: (-1, 0), 0: (-1, 1), 1: (0, 1)},
    }

  @property
  def coordinate(self):
    return (self._x, self._y)

  def process_tick(self):
    self.fire()
    self.turn()

  def turn(self):
    self.direction = self.MOVEMENTS[self.direction[0]][self.direction[1]]

  def fire(self):
    npc = self.get_target()
    if npc:
      self.queue_damage(npc)

  def queue_damage(self, npc: Npc):
    damage = random.randint(0, 25)
    npc.add_to_queue(DamageAction(damage, self.player))
  
  def get_target(self):
    return self.hunt_strategy.get_target(self)

class PlayerRegistry:
  def __init__(self) -> None:
    self._players = []

  @property
  def registered_players(self):
    return self._players

  def create_player(self, coordinate, cannon_strategy):
    player = Player(coordinate, cannon_strategy)
    self._players.append(player)
    return player

class Player:
  def __init__(self, coordinate, cannon_strategy):
    self._cannon = None
    self._x = coordinate[0] 
    self._y = coordinate[1] 
    self._cannon_strategy = cannon_strategy

  def perform_timers(self):
    if self.cannon():
      self.cannon().process_tick()

  def place_cannon(self, coordinate: Tuple[int, int]):
    self._cannon = Cannon(coordinate[0], coordinate[1], self, self._cannon_strategy)
    return self._cannon

  def cannon(self):
    return self._cannon

  @property
  def coordinate(self):
    return (self.x, self.y)
  
  @coordinate.setter
  def coordinate(self, new_coordinate):
    self._x = new_coordinate[0]
    self._y = new_coordinate[1]

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

class MapRegistry:
  def __init__(self, map_config):
    self.map_config = map_config

  def get_objs(self, coordinate):
    return self.map_config.get(coordinate[0], {}).get(coordinate[1], {})

if __name__ == '__main__':
  c = (2962, 3382)
  npc_registry = NpcRegistry()
  player_registry = PlayerRegistry()
  map_config = create_map_config(c)
  map_registry = MapRegistry(map_config)

  # Populate npc_registry
  npc_structs = relevant_npcs(c)
  npcs = []
  strategy = SimpleWalkabilityStrategy(map_registry, npc_registry, player_registry)
  for s in npc_structs:
    npc_registry.create_npc(s['x'], s['y'], strategy, opts=npc_registry.get_npc_stats(s))

  # Populate player_registry
  player = player_registry.create_player(c, CannonHuntStrategy(npc_registry, map_registry, player_registry))
  player.place_cannon(c)

  # Create and run engine
  import time
  engine = Engine(map_registry, npc_registry, player_registry)
  start_time = time.time()
  print('Starting the ticks...')
  engine.perform_ticks(6000)
  print('Done with the ticks... ' + str(time.time() - start_time))

  for npc in npc_registry.registered_npcs:
    if npc.times_died > 0:
      print(f'{npc.name} died {npc.times_died} times')