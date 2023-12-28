# Henke's model

players = []
npc = []


class Action:
  def act_on(self, entity):
    raise NotImplementedError

class Npc:

  def __init__(self, hitpoints: int):
    self.hitpoints = hitpoints
    self.queue = []

  def is_dead(self):
    return self.hitpoints <= 0

  def add_to_queue(self, action: Action):
    self.queue.append(action)

  def perform_queue(self):
    new_queue = []
    for action in self.queue:
      action.act_on(self)
      # TODO: Does the queue actually get cleared on death?
      if self.is_dead():
        break
    self.queue = new_queue

  def take_damage(self, amount):
    print(f'Taking {amount} damage')
    self.hitpoints -= amount
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

class DamageAction(Action):
  def __init__(self, damage):
    self.damage = damage

  def act_on(self, npc: Npc):
    npc.take_damage(self.damage)

class Cannon:

  def __init__(self, x: int, y: int):
    self._x = x
    self._y = y
    self.direction = (0, 0)

  def process_tick(self):
    print('Processing cannon tick')
    self.fire()
    self.turn()

  def turn(self):
    pass

  def fire(self):
    # TODO: Somehow pick an npc
    npc = npcs[0]
    self.queue_damage(npc)

  def queue_damage(self, npc: Npc):
    damage = 10
    npc.add_to_queue(DamageAction(damage))

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

npcs = [Npc(100)]
player = Player()
player.place_cannon(1, 1)
players = [player]
def perform_tick():
  # Process client input

  for npc in npcs:
    # Each npc do
    #   stalls end
    #   timers (poison?)
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

while True:
  perform_tick()
  print(f'{npcs[0].hitpoints}')
  if npcs[0].is_dead():
    break