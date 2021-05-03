#!/usr/bin/python3
from brownie import Pokemon, accounts, network, config
from scripts.helpful_scripts import fund
import asyncio
import json


def main():
    print(config["wallets"]["from_key"])
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    # publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False # Currently having an issue with this
    publish_source = False
    pokemon = Pokemon[len(Pokemon) - 1]
    asyncio.run(createBaseStats(pokemon, dev))
    # string memory pokemonName, uint256 hp, uint256 def, uint256 atk, uint256 spa, uint256 spd, uint256 spe, string memory type1, string memory type2, uint256 number
    print("Going...")
    return pokemon


async def createBaseStats(pokemon, dev):
    tasks = get_tasks(pokemon, dev)
    responses = await asyncio.gather(*tasks)


def get_tasks(pokemon, dev):
    tasks = []
    index = 0
    with open('./metadata/pokemon.csv', 'r') as file:
        for row in file:
            print(row)
            index = index + 1
            if index == 1:
                continue
            row = row.split(",")
            tasks.append(pokemon.createBaseStatPokemon(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], {"from": dev}))
    return tasks
