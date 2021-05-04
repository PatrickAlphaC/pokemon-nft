#!/usr/bin/python3
from brownie import Pokemon, accounts, network, config, interface
import json


def main():
    flatten()


def flatten():
    file = open("./Pokemon_flattened.json", "w+")
    json.dump(Pokemon.get_verification_info(), file)
    file.close()
