// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyNFT_ERC1155 is ERC1155 {
    //Contract inspired from https://www.youtube.com/watch?v=19SSvs32m8I&ab_channel=ArturChmaro

    mapping (uint256 => string) private _tokenURIs;   //We create the mapping for TokenID -> URI
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds; //Counter to keep track of the number of NFT we minted and make sure we dont try to mint the same twice
    
    constructor() ERC1155("I_dont_care_about_the_URI_because_Im_gonna_change_it_later") {}

    function mintToken(string memory tokenURI, uint256 amount) public returns(uint256) {
        uint256 newItemId = _tokenIds.current();
        _mint(msg.sender, newItemId, amount, "");  //_mint(account, id, amount, data), data is usually set to ""
        _setTokenUri(newItemId, tokenURI);

        _tokenIds.increment();

        return newItemId;
    }
    
    function uri(uint256 tokenId) override public view returns (string memory) { //We override the uri function of the EIP-1155: Multi Token Standard (https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC1155/ERC1155.sol)
        return(_tokenURIs[tokenId]);
    }
    
    function _setTokenUri(uint256 tokenId, string memory tokenURI) private {
        _tokenURIs[tokenId] = tokenURI; 
    }
}