pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract PlayerCollectible is ERC721, VRFConsumerBase {

    bytes32 internal keyHash;
    uint256 public fee;
    uint256 public tokenCounter;

    enum Player{CRISTIANO_RONALDO, LIONEL_MESSI, MOHAMED_SALAH}

    // Another way to do this instead of having all these maps would be with a struct
    mapping(bytes32 => address) public requestIdToSender;
    mapping (bytes32 => string) public requestIdToTokenURI;
    mapping (uint256 => Player) public tokenIdToPlayer;
    mapping (bytes32 => uint256) public requestIdToTokenId;

    event requestedPlayerCollectible(bytes32 indexed requestId);

    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash) public
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Player", "plr")
    {
        keyHash = _keyhash;
        fee = 0.1 * 10 ** 18; // 0.1 LINK
        tokenCounter = 0;
    }

    function createCollectible(string memory tokenURI) public returns (bytes32) 
    {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;

        emit requestedPlayerCollectible(requestId); // Emmitting an event its the closest thing to Ethereum logging that exists
    }

    //We kick of the requestRandomness request in the createCollectible
    //The chainlink node reponds by calling this fulfillRandomness function with the generated random 
    //Chainglink calls the VRFCoordinator, which calls this function)
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override
    {
        address playerCollectibleOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;

        //functions inherited from openzeppelin ERC721
        _safeMint(playerCollectibleOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);

        Player player = Player(randomNumber % 3);
        tokenIdToPlayer[newItemId] = player;
        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public
    {
        require(
            // Function inherited from openzeppelin ERC721 to check if the sender is the owner of the Token
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
