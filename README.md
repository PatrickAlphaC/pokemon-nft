# Pokemon NFTs

Matic Contract: https://explorer-mainnet.maticvigil.com/address/0x7e039939FEA5a979e6366cb905d407C4bc92FB59/transactions

<br/>
<p align="center">
<a href="https://chain.link" target="_blank">
<img src="https://raw.githubusercontent.com/PatrickAlphaC/pokemon-nft/main/img/logo.png" width="225" alt="NFT Pokemon">
</a>
</p>
<br/>

This is a repo to work with and use NFTs smart contracts in a python environment, using the Chainlink-mix as a starting point. 

If you'd like to see another repo using random NFTs that are deployed to mainnet, check out the [D&D package](https://github.com/PatrickAlphaC/dungeons-and-dragons-nft).

## Prerequisites

Please install or have installed the following:

- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)
## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.

```bash
pip install eth-brownie
```

2. Clone this repo
```
brownie bake nft-mix
cd nft
```

1. [Install ganache-cli](https://www.npmjs.com/package/ganache-cli)

```bash
npm install -g ganache-cli
```

If you want to be able to deploy to testnets, do the following. 

4. Set your environment variables

Set your `WEB3_INFURA_PROJECT_ID`, and `PRIVATE_KEY` [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html). 

You can get a `WEB3_INFURA_PROJECT_ID` by getting a free trial of [Infura](https://infura.io/). At the moment, it does need to be infura with brownie. You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.io/). 

You'll also need testnet rinkeby ETH and LINK. You can get LINK and ETH into your wallet by using the [rinkeby faucets located here](https://docs.chain.link/docs/link-token-contracts#rinkeby). If you're new to this, [watch this video.](https://www.youtube.com/watch?v=P7FX_1PePX0)

Pinata keys can be found on [Pinata](https://pinata.cloud/pinmanager).

You can add your environment variables to the `.env` file:

```
export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
export PRIVATE_KEY=<PRIVATE_KEY>
export PINATA_API_KEY=<KEY>
export PINATA_API_SECRET=<KEY>
```

AND THEN RUN `source .env` TO ACTIVATE THE ENV VARIABLES
(You'll need to do this everytime you open a new terminal, or [learn how to set them easier](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html))


Or you can run the above in your shell. 


# Usage
```
brownie run scripts/1_deploy_pokemon.py --network rinkeby
```
Optional:
```
brownie run scripts/2_add_base_pokemon_stats.py --network rinkeby
```
Then:
```
brownie run scripts/3_create_pokemon.py --network rinkeby
brownie run scripts/4_create_metadata.py --network rinkeby
brownie run scripts/5_set_tokenuri.py --network rinkeby
```

### Misc
There are some helpful scripts in `helpful_scripts.py`.

# Viewing on OpenSea
After running the last script, you'll see output like:
```
Awesome! You can view your NFT at https://testnets.opensea.io/assets/0x25F955AA3B6Ad6A3cd47Abd6FB55a277F751B7A0/0
Please give up to 20 minutes, and hit the "refresh metadata" button
```
## Testing

```
brownie test
```

## Linting

```
pip install black 
pip install autoflake
autoflake --in-place --remove-unused-variables -r .
black .
```

## Resources

To get started with Brownie:

* [Chainlink Documentation](https://docs.chain.link/docs)
* Check out the [Chainlink documentation](https://docs.chain.link/docs) to get started from any level of smart contract engineering. 
* Check out the other [Brownie mixes](https://github.com/brownie-mix/) that can be used as a starting point for your own contracts. They also provide example code to help you get started.
* ["Getting Started with Brownie"](https://medium.com/@iamdefinitelyahuman/getting-started-with-brownie-part-1-9b2181f4cb99) is a good tutorial to help you familiarize yourself with Brownie.
* For more in-depth information, read the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/).

Shoutout to [TheLinkMarines](https://twitter.com/TheLinkMarines) on twitter for the puppies!

Any questions? Join our [Discord](https://discord.gg/2YHSAey)

## License

This project is licensed under the [MIT license](LICENSE).

<!-- personalityValue = `uint32`
S = TrainerID xor SecretID xor PersonalityValue31..16 xor PersonalityValue15..0
shininess = 1/4096
personalityValue = `uint32`
[Shiny](https://bulbapedia.bulbagarden.net/wiki/Shiny_Pok%C3%A9mon) -->
