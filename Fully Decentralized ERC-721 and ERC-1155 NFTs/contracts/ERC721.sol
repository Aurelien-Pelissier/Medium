// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyNFT_ERC721 is ERC721URIStorage {


    
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds; //Counter to keep track of the number of NFT we minted and make sure we dont try to mint the same twice

    constructor() ERC721("NFT_name", "NFT_symbol") {} //Here you can chose the name and the ID of your NFT

    function mintToken(string memory tokenURI) public returns (uint256) {
        uint256 newItemId = _tokenIds.current();
        _mint(msg.sender, newItemId);
        _setTokenURI(newItemId, tokenURI);

        _tokenIds.increment();

        return newItemId;
    }
}