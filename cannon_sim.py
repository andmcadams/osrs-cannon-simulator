import math
import random
from collections import defaultdict
from typing import Tuple

players = []
npc = []

def cheb(point1, point2):
  return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

def euclidean(point1, point2):
  return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

npc_chunk_lookup = defaultdict(lambda: defaultdict(dict))
def get_npcs_in_chunk(chunk_x, chunk_y):
  return npc_chunk_lookup[chunk_x][chunk_y].values()

def get_living_npcs_in_chunk(chunk_x, chunk_y):
  return [n for n in npc_chunk_lookup[chunk_x][chunk_y].values() if n.is_dead() is False]

def add_to_chunk(npc, chunk_x, chunk_y):
  npc_chunk_lookup[chunk_x][chunk_y][npc.slot_index] = npc

def remove_from_chunk(npc, chunk_x, chunk_y):
  npc_chunk_lookup[chunk_x][chunk_y].pop(npc.slot_index, None)

def get_chunk(x, y):
  return (x // 8, y // 8)

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

class Npc:

  def __init__(self, x: int, y: int, max_hitpoints: int, opts={}):
    self.max_hitpoints = max_hitpoints
    self.queue = []
    self.slot_index = next_slot() # This should eventually be passed in
    self._x = x
    self._y = y
    self.respawn_coordinate = (x, y)
    chunk = get_chunk(x, y)
    add_to_chunk(self, chunk[0], chunk[1])

    self.respawn_time = opts.get('respawn_time', 80) # 20 tick respawn time, will be dependent on monster
    self.respawn()
    self.times_died = 0

  def is_dead(self):
    return self._is_dead

  def respawn(self):
    self._is_dead = False
    self.hitpoints = self.max_hitpoints
    self.respawn_time_remaining = None
    # Move to its respawn location
    self._coordinate = self.respawn_coordinate

  def die(self):
    self._is_dead = True
    self.hitpoints = 0
    self.respawn_time_remaining = self.respawn_time
    # TODO: Does the queue actually get cleared on death? Is there a death queue? Do we care here?
    self.queue = []
    self.times_died += 1


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

  def take_damage(self, amount):
    damage_taken = min(amount, self.hitpoints)
    self.hitpoints -= damage_taken
    print(f'Took {damage_taken} damage (hit a {amount})')
    if self.hitpoints <= 0:
      self.die()
    print(f'Hitpoints remaining: {self.hitpoints}')

  def perform_move(self):
    if self.is_dead():
      return
    # TODO: Move somewhere
    pass

  def perform_interact(self):
    if self.is_dead():
      return
    # TODO: Target the player
    pass

  def x(self):
    return self._x

  def y(self):
    return self._y

  @property
  def coordinate(self):
    return (self.x(), self.y())

  @coordinate.setter
  def _coordinate(self, coord: Tuple[int, int]):
    old_chunk = get_chunk(self._x, self._y)
    new_chunk = get_chunk(coord[0], coord[1])
    if new_chunk != old_chunk:
      remove_from_chunk(self, old_chunk[0], old_chunk[1])
      add_to_chunk(self, new_chunk[0], new_chunk[1])
    self._x = coord[0]
    self._y = coord[1]

class DamageAction(Action):
  def __init__(self, damage):
    self.damage = damage

  def act_on(self, npc: Npc):
    npc.take_damage(self.damage)

class Cannon:

  def __init__(self, x: int, y: int):
    self._x = x
    self._y = y
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
    npc.add_to_queue(DamageAction(damage))
  
  def get_target(self):
    origin = (self._x, self._y)
    direction = self.direction
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
                    if cheb(center, npc.coordinate) <= cannon_ranges[i]:
                        npcs_in_range.append(npc)

        npcs_in_range.sort(key=lambda x: euclidean(center, npc.coordinate))

        if len(npcs_in_range) > 0:
            return npcs_in_range[0]

    return None

class Player:
  def __init__(self):
    self._cannon = None

  def perform_timers(self):
    if self.cannon():
      self.cannon().process_tick()

  def place_cannon(self, x: int, y: int):
    self._cannon = Cannon(x, y)

  def cannon(self):
    return self._cannon

npcs = [Npc(2, 0, 100), Npc(2, 0, 100)]
player = Player()
player.place_cannon(0, 0)
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

tick_num = 0
while tick_num < 200:
  print(f'{tick_num}')
  perform_tick()
  tick_num += 1
for npc in npcs:
  print(npc.times_died)