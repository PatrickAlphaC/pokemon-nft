import pytest
from brownie import network, Pokemon


def test_can_create_pokemon(
    get_account,
    get_vrf_coordinator,
    get_keyhash,
    get_link_token,
    chainlink_fee,
    get_seed
):
    # Arrange
    if network.show_active() not in ["development"] or "fork" in network.show_active():
        pytest.skip("Only for local testing")
    pokemon = Pokemon.deploy(
        get_vrf_coordinator.address,
        get_link_token.address,
        get_keyhash,
        chainlink_fee,
        {"from": get_account},
    )
    # bulbasaur lvl 100 stats for atk
    bulbasaur_attack = pokemon.getCalculatedStat(49, 31, 0, 100)
    bulbasaur_hp = pokemon.getCalculatedHPStat(45, 31, 0, 100)
    assert bulbasaur_attack == 134
    assert bulbasaur_hp == 231
    assert isinstance(pokemon.tokenCounter(), int)
