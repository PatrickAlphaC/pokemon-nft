import json
import collections

pokemon_dict = {}
with open('./metadata/pokemon_ipfs_hashes.json', 'r') as file:
    lines = file.readlines()
    pokemon = ""
    hashed = ""
    for line in lines:
        if "Uploading" in line:
            pokemon = line.split(" ")[1].replace("\n", "").replace(" ", "")
        if 'IpfsHash' in line:
            hashed = line.split(",")[0].split(
                ":")[1].replace("'", "").replace(" ", "")
        if "{" in line:
            pokemon_dict[pokemon] = hashed

print(pokemon_dict)
