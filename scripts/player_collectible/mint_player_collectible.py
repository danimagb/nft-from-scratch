from brownie import PlayerCollectible, accounts, config
from scripts.helpers import fund_with_link, get_player
import time

def main():
    dev = accounts.add(config["wallets"]["from_key"])
    player_collectable = PlayerCollectible[len(PlayerCollectible) - 1]
    fund_with_link(player_collectable)
    transaction = player_collectable.createCollectible("None", {"from": dev})
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)
    time.sleep(65)
    requestId = transaction.events["requestedPlayerCollectible"]["requestId"]
    token_id = player_collectable.requestIdToTokenId(requestId)
    player = get_player(player_collectable.tokenIdToPlayer(token_id))
    print("Player of tokenId {} is {}".format(token_id, player))