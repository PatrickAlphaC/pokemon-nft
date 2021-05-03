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
    publish_source = True
    pokemon = Pokemon.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link_token"],
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": dev},
        publish_source=publish_source,
    )
    return pokemon
