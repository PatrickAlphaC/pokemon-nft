#!/usr/bin/python3
from brownie import Pokemon, accounts, config
from scripts.helpful_scripts import fund
import time

STATIC_SEED = 123


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    pokemon = Pokemon[len(Pokemon) - 1]
    size = pokemon.lengthOfListOfPokemonNames()
    fund(pokemon, amount=size)
    token_id_starting_point = 29
    # Wait on the loop above to finish
    time.sleep(60)
    # For random Pokemon
    # transaction_two = pokemon.updateCreatedPokemon(token_id, "", {"from": dev})
    # else, we can make a pokemon for each one:
    for token_id in range(len(token_ids)):
        pokemon_name = pokemon.listOfPokemonNames(token_id)
        transaction_two = pokemon.updateCreatedPokemon(
            token_id, str(pokemon_name), {"from": dev})
        transaction_two.wait(1)
        pokemon_name = pokemon.uniquePokemon(token_id)
        battle_stats = pokemon.tokenIdToBattleStats(token_id)
        print(f"{pokemon_name} \n {battle_stats}")
# Sandslash
