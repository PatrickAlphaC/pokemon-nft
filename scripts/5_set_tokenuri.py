#!/usr/bin/python3
from brownie import Pokemon, accounts, network, config
from metadata import sample_metadata
from scripts.helpful_scripts import OPENSEA_FORMAT, METADATA_MAP
import requests
import os
import json


def main():
    print("Working on " + network.show_active())
    pokemon = Pokemon[len(Pokemon) - 1]
    number_of_pokemon = 152
    print(f"The number of Pokemon you've deployed is: {number_of_pokemon}")
    for token_id in range(number_of_pokemon):
        tokenuri = get_token_uri(token_id, pokemon)
        if not pokemon.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, pokemon, tokenuri)
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, pokemon, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    pokemon.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(pokemon.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')


def get_token_uri(token_id, pokemon):
    # pinlist_url = "https://api.pinata.cloud/data/pinList?status=pinned"
    # headers = {'pinata_api_key': os.getenv('PINATA_API_KEY'),
    #            'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')}
    # response = requests.get(pinlist_url, headers=headers)
    battleStats = pokemon.tokenIdToBattleStats(token_id)
    pokemon_name = battleStats['pokemonName']
    map_file = f"metadata/{network.show_active()}/{METADATA_MAP}"
    with open(map_file, 'r') as file:
        map = json.load(file)
        return map[f'{token_id}-{pokemon_name}.json']
