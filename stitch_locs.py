import json
from collections import defaultdict

# dump the first thing
# dump the second thing

# stitch together
locations_config = json.load(open('./out/data_osrs/location_configs.json', 'r'))
id_to_loc_config_map = {}
for config in locations_config:
  id_to_loc_config_map[config['id']] = config

# Free mem
locations_config = None

# Dump this lookup mapping to a file
output = open('id_to_loc_configs.json', 'w+')
output.write(json.dumps(id_to_loc_config_map, indent=2, sort_keys=True))
output.close

# Construct a dict locs[i][j] = [{x, y, id, etc}]
# To get i/js -> go through every json file in out/data_osrs/locations/x.json
chunk_mapping = defaultdict(lambda: defaultdict(list))
from pathlib import Path

pathlist = Path('./out/data_osrs/locations/').glob('*.json')
for path in pathlist:
    content = json.load(path.open())
    # Each json is responsible for all instances of that loc
    for loc_instance in content:
        chunk_x = loc_instance['i']
        chunk_y = loc_instance['j']
        # Really don't need the whole loc_instance since i, j are keys, but this helps with debugging
        chunk_mapping[chunk_x][chunk_y].append(loc_instance)

# Dump to files
output_directory = Path("output_configs")
output_directory.mkdir(parents=True, exist_ok=True)

for x, inner_dict in chunk_mapping.items():
  for y, data_list in inner_dict.items():
    # Generate the filename based on the x and y values
    filename = f'm_{x}_{y}.json'
    
    # Write the data_list to the JSON file
    with open(output_directory / filename, "w+") as file:
      json.dump(data_list, file, indent=2, sort_keys=True)