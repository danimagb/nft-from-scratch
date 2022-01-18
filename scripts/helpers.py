from brownie import (
    network,
    accounts,
    config,
    interface
)

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"
NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]



def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None


def fund_with_link(
    nft_contract, account=None, amount=1000000000000000000
):
    account = account if account else get_account()
    link_token = interface.LinkTokenInterface(
        config["networks"][network.show_active()]["link_token"]
    )
    tx = link_token.transfer(nft_contract, amount, {"from": account})
    print(f"Funded {nft_contract.address}")
    return tx


def get_verify_status():
    verify = (
        config["networks"][network.show_active()]["verify"]
        if config["networks"][network.show_active()].get("verify")
        else False
    )
    return verify


def get_dog_breed(breed_number):
    switch = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}
    return switch[breed_number]

def get_player(player_id):
    switch = {0: "CRISTIANO_RONALDO", 1: "LIONEL_MESSI", 2: "MOHAMED_SALAH"}
    return switch[player_id]