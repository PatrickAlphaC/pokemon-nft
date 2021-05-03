#!/usr/bin/python3
from brownie import Pokemon, accounts, config
from scripts.helpful_scripts import fund
import time

STATIC_SEED = 123


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    pokemon = Pokemon[len(Pokemon) - 1]
    fund(pokemon)
    transaction = pokemon.createRandomPokemon(STATIC_SEED, {"from": dev})
    transaction.wait(1)
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)
    time.sleep(60)
    requestId = transaction.events["requestedPokemon"]["requestId"]
    token_id = pokemon.requestIdToTokenId(requestId)
    transaction_two = pokemon.updateCreatedPokemon(token_id, {"from": dev})
    transaction_two.wait(1)
    pokemon_name = pokemon.uniquePokemon(token_id)
    battle_stats = pokemon.tokenIdToBattleStats(token_id)
    print(f"{pokemon_name} \n {battle_stats}")
