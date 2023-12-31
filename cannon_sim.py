import math
import random
from collections import defaultdict
from typing import Tuple
from enum import Enum
from create_map import create_map_config, LOC_ID_TO_CONFIG_MAP, relevant_npcs

players = []
npcs = []
world_map = {}

DEBUG = False
def debug(msg):
  if DEBUG == True:
    print(msg)

def get_npc_stats(npc_struct):
  npc_id = npc_struct['id']
  if npc_id in [3269, 11942, 11943, 11944, 3270, 11945, 3271, 11946, 11947, 3273, 3274]:
    return {'id': npc_id, 'max_range': 4, 'wander_range': 2, 'hitpoints': 22, 'combat_level': 10, 'name': 'Guard'}
  return {'id': npc_id}

def cheb(point1, point2):
  return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

def euclidean(point1, point2):
  return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

npc_chunk_lookup = defaultdict(lambda: defaultdict(dict))
def get_npcs_in_chunk(chunk_x, chunk_y):
  return npc_chunk_lookup[chunk_x][chunk_y].values()

def get_living_npcs_in_chunk(chunk_x, chunk_y):
  return [n for n in npc_chunk_lookup[chunk_x][chunk_y].values() if n.is_dead() is False]

def get_living_npcs_in_chunk_by_abs_coordinate(coordinate):
  chunk = get_chunk(coordinate[0], coordinate[1])
  return get_living_npcs_in_chunk(chunk[0], chunk[1])

def add_to_chunk(npc, chunk_x, chunk_y):
  npc_chunk_lookup[chunk_x][chunk_y][npc.slot_index] = npc

def remove_from_chunk(npc, chunk_x, chunk_y):
  npc_chunk_lookup[chunk_x][chunk_y].pop(npc.slot_index, None)

def get_chunk(x, y):
  return (x // 8, y // 8)

def is_walkable_tile(old_coord, new_coord):
  # Not walkable if there is an npc there or object that restricts movement
  for npc in get_living_npcs_in_chunk_by_abs_coordinate(new_coord):
    # TODO: Allow if the transparent flag is set
    if npc.coordinate == (new_coord[0], new_coord[1]):
      return False

  # Get the object at new_coord
  objs_on_coord = world_map[new_coord[0]][new_coord[1]]
  if objs_on_coord:
    for loc in objs_on_coord:
      debug('Would have bumped into an object!')
      if LOC_ID_TO_CONFIG_MAP[loc['id']].get('is_transparent', False) is False:
        return False


  return True

def next_slot_func():
  count = 0
  def inner():
    nonlocal count
    count += 1
    return count
  return inner
next_slot = next_slot_func()


class Action:
  def act_on(self, entity):
    raise NotImplementedError

class NpcMode(Enum):
  WANDER = 1
  PATROL = 2
  PLAYERESCAPE = 3
  PLAYERFOLLOW = 4
  PLAYERFACE = 5
  PLAYERFACECLOSE = 6

class Npc:

  def __init__(self, x: int, y: int, opts={}):
    self.queue = []
    self.slot_index = next_slot() # This should eventually be passed in
    self._x = x
    self._y = y
    self.respawn_coordinate = (x, y)
    chunk = get_chunk(x, y)
    add_to_chunk(self, chunk[0], chunk[1])

    self.npc_id = opts.get('id', None)
    self.name = opts.get('name', f'Npc {self.slot_index}{" (id: " + str(self.npc_id) + ")" if self.npc_id else ""}')
    self.max_hitpoints = opts.get('hitpoints', 1)
    self._combat_level = opts.get('combat_level', 0)
    self.respawn_time = opts.get('respawn_time', 50) # 50 tick respawn time, will be dependent on monster
    self.wanderrange = opts.get('wander_range', 5) # No clue what the default is here
    self.maxrange = opts.get('max_range', 8) # No clue what the default is here
    self.set_interaction(None)
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
    if self.can_attack():
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
      return

    new_coordinate = None
    # Attempt to move to the destination tile
    if is_walkable_tile(self.coordinate, (self.x + dx, self.y + dy)):
      new_coordinate = (self.x + dx, self.y + dy)
    elif dx != 0 and dy != 0:
      # If we were trying to go diagonally, but cant, try E/W followed by N/S
      if is_walkable_tile(self.coordinate, (self.x + dx, self.y)):
        new_coordinate =  (self.x + dx, self.y)
      elif is_walkable_tile(self.coordinate, (self.x, self.y + dy)):
        new_coordinate =  (self.x, self.y + dy)

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
    old_chunk = get_chunk(self._x, self._y)
    new_chunk = get_chunk(coord[0], coord[1])
    if new_chunk != old_chunk:
      remove_from_chunk(self, old_chunk[0], old_chunk[1])
      add_to_chunk(self, new_chunk[0], new_chunk[1])
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

class Cannon:

  # Cannon LOS is checked from center of cannon and center of checked area
  def __init__(self, x: int, y: int, player: 'Player'):
    self._x = x
    self._y = y
    self.player = player
    # X, Y (positive is right and up resp.)
    self.direction = (0, 1)

    self.MOVEMENTS = {
      0: {1: (1, 1), -1: (-1, -1)},
      1: {1: (1, 0), 0: (1, -1), -1: (0, -1)},
      -1: {-1: (-1, 0), 0: (-1, 1), 1: (0, 1)},
    }

  def process_tick(self):
    self.fire()
    self.turn()

  def turn(self):
    # Definitely some way to not hardcode but I can't be bothered
    self.direction = self.MOVEMENTS[self.direction[0]][self.direction[1]]

  def fire(self):
    npc = self.get_target()
    if npc:
      self.queue_damage(npc)

  def queue_damage(self, npc: Npc):
    damage = random.randint(0, 25)
    npc.add_to_queue(DamageAction(damage, self.player))
  
  def get_target(self):
    origin = (self._x, self._y)
    direction = self.direction
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
                for npc in get_living_npcs_in_chunk(chunk[0], chunk[1]):
                    if npc.is_attackable():
                      if cheb(center, npc.coordinate) <= cannon_ranges[i]:
                          npcs_in_range.append(npc)

        npcs_in_range.sort(key=lambda npc: euclidean(center, npc.coordinate))

        if len(npcs_in_range) > 0:
            return npcs_in_range[0]

    return None

class Player:
  def __init__(self):
    self._cannon = None
    self._x = c[0] + 2 
    self._y = c[1] + 1 

  def perform_timers(self):
    if self.cannon():
      self.cannon().process_tick()

  def place_cannon(self, coordinate: Tuple[int, int]):
    self._cannon = Cannon(coordinate[0], coordinate[1], self)

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


c = (2962, 3382)
world_map = create_map_config(c)
npc_structs = relevant_npcs(c)
npcs = []
for s in npc_structs:
  npcs.append(Npc(s['x'], s['y'], opts=get_npc_stats(s)))

player = Player()
player.place_cannon(c)
players = [player]
def perform_tick():
  # Process client input
  for npc in npcs:
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
  for player in players:
    # Each player do
    #   stalls end
    #   queue (take damage)
    #   timers (poison?)
    player.perform_timers() # This fires the cannon
    #   area queue
    #   interaction with items/objects
    #   * (not v0) movement
    #   * (not v0) interaction with players/npcs

class DamageAction(Action):
  def __init__(self, damage: int, attacker: Player):
    self.damage = damage
    self.attacker = attacker

  def act_on(self, npc: Npc):
    npc.take_damage(self.damage, self.attacker)

tick_num = 0
while tick_num < 6000:
  debug(f'{tick_num}')
  perform_tick()
  tick_num += 1
for npc in npcs:
  if npc.times_died > 0:
    print(f'{npc.name} died {npc.times_died} times')