import json
from collections import defaultdict
from enum import Enum
from pathlib import Path
# Take in coord (absolute coords) + plane
# Get 3x3 of chunks around that coord
# Load those files and populate objects needed

LOC_ID_TO_CONFIG_MAP = {}
locations_config = json.load(open('./out/data_osrs/location_configs.json', 'r'))
id_to_loc_config_map = {}
for config in locations_config:
  LOC_ID_TO_CONFIG_MAP[config['id']] = config

NPC_MAP = json.load(open('./npcs_reduced.json', 'r'))

class Mask:
  TOP = 1
  RIGHT = 2
  BOTTOM = 4
  LEFT = 8
  TOP_LEFT = 16
  TOP_RIGHT = 32
  BOTTOM_LEFT = 64
  BOTTOM_RIGHT = 128
  OBJECT = 256

def create_map_config(coordinate):
  center_chunk = (coordinate[0]//64, coordinate[1]//64)
  mapping = defaultdict(lambda: defaultdict(dict))
  for i in [-1, 0, 1]:
    for j in [-1, 0, 1]:
      chunk_to_load = (center_chunk[0] + i, center_chunk[1] + j)
      file_path = Path(f'./output_configs/m_{chunk_to_load[0]}_{chunk_to_load[1]}.json')
      if file_path.exists():
        with file_path.open() as chunk_file:
          locs = json.load(chunk_file)
          for loc in locs:
            # Only do plane 0 for now, see how long it takes anyone to notice
            if loc['plane'] != 0:
              continue

            current_data = mapping[chunk_to_load[0]*64 + loc['x']][chunk_to_load[1]*64 + loc['y']]
            existing_blockers = current_data['movement_flags'] if current_data else 0
            existing_projectile_flags = current_data['projectile_flags'] if current_data else 0

            blocks_projectiles = LOC_ID_TO_CONFIG_MAP[loc['id']].get('blocks_projectiles', True)
            rotation = loc.get('rotation', 0)
            typee = loc['type']
            blockers = 0
            if typee == 0:
              blockers |= [Mask.LEFT, Mask.TOP, Mask.RIGHT, Mask.BOTTOM][rotation]
            if typee == 1 or typee == 3:
              blockers |= [Mask.TOP_LEFT, Mask.TOP_RIGHT, Mask.BOTTOM_RIGHT, Mask.BOTTOM_LEFT][rotation]
            if typee == 2:
              blockers |= [Mask.TOP + Mask.LEFT, Mask.TOP + Mask.RIGHT, Mask.BOTTOM + Mask.RIGHT, Mask.BOTTOM + Mask.LEFT][rotation]
            if typee == 9:
              blockers |= Mask.TOP + Mask.LEFT + Mask.RIGHT + Mask.BOTTOM + Mask.OBJECT
            # Add blockers for the basic objects
            if blockers != 0:
              # Load the flags we have for this tile, if there are any. Then or together to get all blockers
              projectile_flags = blockers if blocks_projectiles else 0
              result = {'movement_flags': existing_blockers | blockers, 'projectile_flags': existing_projectile_flags | projectile_flags}
              mapping[chunk_to_load[0]*64 + loc['x']][chunk_to_load[1]*64 + loc['y']] = result

            # Special weird case of bigger objects
            if typee == 10:
              if rotation % 2 == 0:
                dim_x = LOC_ID_TO_CONFIG_MAP[loc['id']].get('dim_x', 1)
                dim_y = LOC_ID_TO_CONFIG_MAP[loc['id']].get('dim_y', 1)
              else:
                dim_x = LOC_ID_TO_CONFIG_MAP[loc['id']].get('dim_y', 1)
                dim_y = LOC_ID_TO_CONFIG_MAP[loc['id']].get('dim_x', 1)
              blockers = Mask.TOP + Mask.LEFT + Mask.RIGHT + Mask.BOTTOM
              projectile_flags = blockers if blocks_projectiles else 0
              result = {'movement_flags': existing_blockers | blockers, 'projectile_flags': existing_projectile_flags | projectile_flags}
              for w in range(dim_x):
                for z in range(dim_y):
                  mapping[chunk_to_load[0]*64 + loc['x'] + w][chunk_to_load[1]*64 + loc['y'] + z] = result
  return mapping

def relevant_npcs(coordinate):
  bottom_left_coord = ((coordinate[0]//64 - 1)*64, (coordinate[1]//64 - 1)*64)
  top_right_coord = ((coordinate[0]//64 + 1)*64 + 63, (coordinate[1]//64 + 1)*64 + 63)
  npcs = []
  for npc in NPC_MAP:
    x = npc['x']
    y = npc['y']
    plane = npc['p']
    # TODO: Make this allow multiplane
    if plane != 0:
      continue
    if bottom_left_coord[0] <= x <= top_right_coord[0] and bottom_left_coord[1] <= y <= top_right_coord[1]:
      npcs.append(npc)

  return npcs

if __name__ == '__main__':
  start_coord = (3350, 9527)
  chunk_map = create_map_config(start_coord)
  output_file = Path("mapping.json")
  with open(output_file, "w+") as file:
    json.dump(chunk_map, file, indent=2, sort_keys=True)