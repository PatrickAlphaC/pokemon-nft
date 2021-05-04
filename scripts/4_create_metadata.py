#!/usr/bin/python3
import os
import requests
import json
from brownie import Pokemon, network
from metadata import sample_metadata
from pathlib import Path
import json
from scripts.helpful_scripts import METADATA_MAP

IPFS_URI = "https://ipfs.io/ipfs/{}"
PINATA_BASE_URL = 'https://api.pinata.cloud/pinning/pinFileToIPFS'


def main():
    print("Working on " + network.show_active())
    pokemon = Pokemon[len(Pokemon) - 1]
    number_of_pokemon = 151
    print(
        "The number of Pokémon you've deployed is: "
        + str(number_of_pokemon)
    )
    write_metadata(
        number_of_pokemon, pokemon)


def write_metadata(token_ids, nft_contract):
    for token_id in range(token_ids):
        collectible_metadata = sample_metadata.metadata_template
        battleStats = nft_contract.tokenIdToBattleStats(token_id)
        uniquePokemon = nft_contract.uniquePokemon(token_id)
        # pokemonName = battleStats('pokemonName')
        end_name = f"{token_id}-{battleStats['pokemonName']}.json"
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{end_name}"
        )
        # if Path(metadata_file_name).exists():
        #     print(
        #         "{} already found, delete it to overwrite!".format(
        #             metadata_file_name)
        #     )
        # else:
        print("Creating Metadata file: " + metadata_file_name)
        collectible_metadata["name"] = battleStats['pokemonName']
        collectible_metadata["description"] = f"A powerful {battleStats['type1']} and {battleStats['type2']} type Pokemon!"
        collectible_metadata["attributes"][0]["value"] = uniquePokemon['nickname']
        collectible_metadata["attributes"][1]["value"] = uniquePokemon['level']
        collectible_metadata["attributes"][2]["value"] = battleStats['hp']
        collectible_metadata["attributes"][3]["value"] = battleStats['atk']
        collectible_metadata["attributes"][4]["value"] = battleStats['def']
        collectible_metadata["attributes"][5]["value"] = battleStats['spa']
        collectible_metadata["attributes"][6]["value"] = battleStats['spd']
        collectible_metadata["attributes"][7]["value"] = battleStats['spe']
        collectible_metadata["attributes"][8]["value"] = uniquePokemon['ability']
        collectible_metadata["attributes"][9]["value"] = uniquePokemon['nature']
        collectible_metadata["attributes"][10]["value"] = uniquePokemon['shiny']
        collectible_metadata["attributes"][11]["value"] = uniquePokemon['item']
        collectible_metadata["attributes"][12]["value"] = battleStats['type1']
        collectible_metadata["attributes"][13]["value"] = battleStats['type2']

        image_hash = get_pokemon_image_uri(
            battleStats['pokemonName'], battleStats['number'])
        image_uri = IPFS_URI.format(image_hash)
        collectible_metadata["image"] = image_uri
        with open(metadata_file_name, "w+") as file:
            json.dump(collectible_metadata, file)
        print(f"File {metadata_file_name} created! Uploading to Pinata...")
        response = upload_to_pinata(metadata_file_name)
        map_file_name = f"./metadata/{network.show_active()}/{METADATA_MAP}"
        json_map = {}
        with open(map_file_name, "r") as map_file:
            json_map = json.load(map_file)
        with open(map_file_name, "w+") as map_file:
            print(f"Updating {map_file_name}")
            json_map[end_name] = IPFS_URI.format(
                response.json()['IpfsHash'])
            json.dump(json_map, map_file)
            print(IPFS_URI.format(response.json()['IpfsHash']))

        # curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


def upload_to_pinata(filepath):
    filename = filepath.split('/')[-1:][0]
    headers = {'pinata_api_key': os.getenv('PINATA_API_KEY'),
               'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')}
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(PINATA_BASE_URL,
                                 files={"file": (filename, image_binary)},
                                 headers=headers)
        print("Uploaded!")
        return response


def get_pokemon_image_uri(pokemon_name, pokemon_number):
    with open('./metadata/pokemon_ipfs_hashes.json') as file:
        pokemon_to_ipfs = json.load(file)
        string_pokemon_number = str(int(pokemon_number))
        while (len(string_pokemon_number) < 3):
            string_pokemon_number = "0" + string_pokemon_number

        hash = pokemon_to_ipfs[f'{string_pokemon_number}{pokemon_name}.png']
        return hash
