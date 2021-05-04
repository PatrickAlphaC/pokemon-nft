from brownie import accounts, config, interface, network

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"
METADATA_MAP = 'MAP.json'


def fund(nft_contract, amount=1):
    dev = accounts.add(config["wallets"]["from_key"])
    # Get the most recent PriceFeed Object
    interface.LinkTokenInterface(
        config["networks"][network.show_active()]["link_token"]
    ).transfer(
        nft_contract, config["networks"][network.show_active()]["fee"] * amount, {
            "from": dev}
    )


def get_eth_usd_price_feed_address():
    if network.show_active() == "development":
        mock_price_feed = MockV3Aggregator.deploy(
            18, 2000, {"from": accounts[0]})
        return mock_price_feed.address
    if network.show_active() in config["networks"]:
        return config["networks"][network.show_active()]["eth_usd_price_feed"]
