#!/usr/bin/python3
import os
import requests
import json
from brownie import PlayerCollectible, network
from metadata import sample_metadata
from scripts.helpers import get_player
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

player_to_image_uri = {
    "CRISTIANO_RONALDO": "https://ipfs.io/ipfs/QmZFGFBKhnHZsZZZNw4vG36ZDsADYAkMXWFctj9Q1EuLo1?filename=cristiano-ronaldo.png",
    "LIONEL_MESSY": "https://ipfs.io/ipfs/QmRrhqo2gc4hNP3UqvdDWDjFKqCXRcmDFH2rBXFz9mbPbU?filename=lionel-messi.png",
    "MOHAMED_SALAH": "https://ipfs.io/ipfs/QmV7n4WCoR2wHdRjmvsAuWfNMYfFCEH9c1Fi5CHvoFFGyofilename=mohamed-salah.png",
}


def main():
    print("Working on " + network.show_active())
    player_collectible = PlayerCollectible[len(PlayerCollectible) - 1]
    number_of_player_collectibles = player_collectible.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_player_collectibles)
    )
    write_metadata(number_of_player_collectibles, player_collectible)


def write_metadata(token_ids, nft_contract):
    for token_id in range(token_ids):
        collectible_metadata = sample_metadata.metadata_template
        player = get_player(nft_contract.tokenIdToPlayer(token_id))
        metadata_file_name = (
            "./metadata/{}/players/".format(network.show_active())
            + str(token_id)
            + "-"
            + player
            + ".json"
        )
        if Path(metadata_file_name).exists():
            print(
                "{} already found, delete it to overwrite!".format(
                    metadata_file_name)
            )
        else:
            print("Creating Metadata file: " + metadata_file_name)
            collectible_metadata["name"] = get_player(
                nft_contract.tokenIdToPlayer(token_id)
            ).replace('_', ' ')
            collectible_metadata["description"] = "The incredible {}!".format(
                collectible_metadata["name"].replace('_', ' ')
            )
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(
                    player.lower().replace('_', '-'))
                image_to_upload = upload_to_ipfs(image_path)
            image_to_upload = (
                player_to_image_uri[player] if not image_to_upload else image_to_upload
            )
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
    return image_uri
