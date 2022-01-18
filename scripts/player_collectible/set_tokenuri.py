#!/usr/bin/python3
from brownie import  PlayerCollectible, accounts, network, config
from metadata import sample_metadata
from scripts.helpers import get_player, OPENSEA_FORMAT

player_metadata_dic = {
    "CRISTIANO_RONALDO": "https://ipfs.io/ipfs/QmQYCqC9SWWSn7Jk6nbkRQU5eJnqd4SzFBVfkCb7aRaBqg?0-CRISTIANO_RONALDO.json",
    "LIONEL_MESSI": "https://ipfs.io/ipfs/QmRjfXWmtjAb18jZivhhqTcCNmfvtkuBvoJDd9i57CqMwS?filename=0-LIONEL_MESSI.json",
    "MOHAMED_SALAH": "https://ipfs.io/ipfs/QmaCeKL8yKFHM8gQbX8VV2xab3fRDf3qnn3BKfqCnCaq77?filename=1-MOHAMED_SALAH.json",
}

def main():
    print("Working on " + network.show_active())
    player_collectible = PlayerCollectible[len(PlayerCollectible) - 1]
    number_of_player_collectibles = player_collectible.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_player_collectibles)
    )
    for token_id in range(number_of_player_collectibles):
        print("Setting tokenURI of {}".format(token_id))
        player = get_player(player_collectible.tokenIdToPlayer(token_id))
        ##if not player_collectible.tokenURI(token_id).startswith("https://"):
        print("Setting tokenURI of {}".format(token_id))
        set_tokenURI(token_id, player_collectible,
                        player_metadata_dic[player])
        ##else:
            ##print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
