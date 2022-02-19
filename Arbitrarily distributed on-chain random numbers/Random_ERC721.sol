// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";


//https://blog.chain.link/random-numbers-nft-erc721/


contract Random_ERC721 is ERC721URIStorage, VRFConsumerBase {

    address owner;
    mapping (uint256 => int256[5]) public NFT_random_values;
    //Number that will be drawn by our generator (with different distributions)
    //These numbers can be negative

    //1 number uniformly drawn between [a,b]
    int256 a = 100;
    int256 b = 1000;
    //2 number normally distributed of mean x0 and std sigma
    int256 mu = 100000;
    uint256 sigma = 100;
    //3 number exponentially distributed of rate lambda
    uint256 lambda = 0.1 *10**18; //with 18 decimals
    //4 Number gamma distributed of rate lambda and shape parameter k
    uint256 k = 10;
    //5 number arbitrarily distributed with the quantile function (input 100 numbers as an example here)
    int256[] Quantile_function = [int256(24), 98, 221, 394, 615, 885, 1204, 1570, 1985, 2447, 2955, 3511, 4112, 4758, 5449, 6184, 6962, 7783, 8645, 9549, 10492, 11474, 12494, 13551, 14644, 15772, 16934, 18128, 19354, 20610, 21895, 23208, 24547, 25912, 27300, 28711, 30142, 31593, 33063, 34549, 36050, 37565, 39092, 40630, 42178, 43733, 45294, 46860, 48429, 49999, 51570, 53139, 54705, 56266, 57821, 59369, 60907, 62434, 63949, 65450, 66936, 68406, 69857, 71288, 72699, 74087, 75452, 76791, 78104, 79389, 80645, 81871, 83065, 84227, 85355, 86448, 87505, 88525, 89507, 90450, 91354, 92216, 93037, 93815, 94550, 95241, 95887, 96488, 97044, 97552, 98014, 98429, 98795, 99114, 99384, 99605, 99778, 99901, 99975];


    //For chainlink VRF
    address public VRFCoordinator;
    address public LinkToken;
    bytes32 internal keyHash;
    uint256 internal fee;
    uint256 public randomResult;

    mapping(bytes32 => address) requestToSender;
    mapping(bytes32 => uint256) requestToTokenId;

    string blockchain = "polygon_mumbai"; //see last function at the bottom of the page
    address _VRFCoordinator = 0x8C7382F9D8f56b33781fE506E897a4F1e2d17255;
    address _LinkToken = 0x326C977E6efc84E512bB9C30f76E30c160eD06FB;

    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds; //Counter to keep track of the number of NFT we minted and make sure we dont try to mint the same twice
    Counters.Counter private _requestIds;
    


    constructor()
        VRFConsumerBase(_VRFCoordinator, _LinkToken)
        ERC721("RandomNFT", "RNFT")   
    {
        (VRFCoordinator, LinkToken, keyHash, fee) = get_VRF_parameters(blockchain); 
    }

    function mint_batches_NFTs(string[] memory copyright_URIs) public returns (uint256[] memory)  {
        uint i=0;
        uint l = copyright_URIs.length;
        uint256[] memory tokenIDs = new uint256[](l);
        for (i = 0; i < l; i++) {
            uint256 tokenID = mint_new_NFT(copyright_URIs[i]);
            tokenIDs[i] = tokenID;
            }
        return tokenIDs; //returns the list of tokenIDs that were minted
    }    

    function mint_new_NFT(string memory tokenURI) public returns (uint256) {
        require(msg.sender == owner, "only owner can mint");
        uint256 newItemId = _tokenIds.current();
        _mint(msg.sender, newItemId);
        _setTokenURI(newItemId, tokenURI);
        _Fill_random_NFT_variables_with_ChainlinkVRF(newItemId);
        _tokenIds.increment();
        return newItemId;
    }



    // Below are all the code related to the generation of trees

    function _Fill_random_NFT_variables_with_ChainlinkVRF(uint256 Tree_ID) internal returns (bytes32) {
        // Call the chainlink VRF for a random number to leter fill in the NFT values
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK - fill contract with faucet");

        bytes32 requestId = requestRandomness(keyHash, fee);
        requestToTokenId[requestId] = Tree_ID;
        requestToSender[requestId] = msg.sender;

        return requestId;
    }

    function fulfillRandomness(bytes32 requestId, uint256 random_number) internal override {
        
        //Fill the NFT variables with the random number obtained from Chainlink 
        //(called automatically by chainlink when number is generated)
        
        //1 number uniformly drawn between [a,b]
        int256 number_1 = randint(random_number, a, b, 1)[0];

        //2 number normally distributed of mean mu and std sigma
        int256 number_2 = NormalRNG(random_number, mu, sigma, 1)[0];

        //3 number exponentially distributed of rate lambda
        int256 number_3 = ExpRNG(random_number, a, lambda, 1)[0];

        //4 Number gamma distributed of rate lambda and shape parameter k
        int256 number_4 = GammaRNG(random_number, lambda, k, 1)[0];

        //5 Number arbitrarily distributed with quantile functions
        int256 number_5 = QuantileRNG(random_number, Quantile_function, 1)[0];

        //Stroe the obtained values
        int256[5] memory new_values = [number_1,number_2,number_3,number_4,number_5];
        uint256 newTokenId = requestToTokenId[requestId];
        NFT_random_values[newTokenId] = new_values;
    }


    function NormalRNG(uint256 random_number, int256 _mu, uint256 _sigma, uint256 _n) internal pure returns (int256[] memory)
    {
        //generate n random integers normally distributed of mean x0 and standard deviation std
        uint256[] memory random_array = expand(random_number, _n);
        int256[] memory final_array = new int256[](_n);

        for (uint256 i = 0; i < _n; i++) {
            //by Centrali Limit Thoerem, the count of 1’s, after proper transformation
            //is approximately normally distributed, in our case of mean 256/2 = 128 and std = 8
            uint256 result = _countOnes(random_array[i]); 
            //transforming the result to match x0 and std
            final_array[i] = int256(int(result) * int(_sigma)/8) - 128*int(_sigma)/8 + _mu;
        }

        return final_array;
    }


    function ExpRNG(uint256 random_number, int256 _a, uint256 _lambda, uint256 _n) internal pure returns (int256[] memory)
    {
        //generate n random integers exponentially distributed of rate lambda and minimum a
        //_lambda is the rate with 18 decimals
        uint256[] memory random_array = expand(random_number, _n);
        int256[] memory final_array = new int256[](_n);

        for (uint256 i = 0; i < _n; i++) {
            uint256 result = log2(random_array[i]); //multiply by 1/log(2) to adjust log base
            //transforming the result to match x0 and std
            final_array[i] = (-int(result)+256)*10**18/int(_lambda)*100000/144269 + _a;
        }

        return final_array;
    }


    function GammaRNG(uint256 random_number, uint256 _lambda, uint256 _k, uint256 _n) internal pure returns (int256[] memory)
    {
        //generate n random integers normally distributed of mean x0 and standard deviation std
        uint256[] memory random_array = expand(random_number, _n);
        int256[] memory final_array = new int256[](_n);

        for (uint256 i = 0; i < _n; i++) {
            int256[] memory results = ExpRNG(random_array[i], 0, _lambda, _k);

            final_array[i] = getArraySum(results);
        }

        return final_array;
    }


    //Arbitrary distribution with quantiles
    function QuantileRNG(uint256 random_number, int256[] memory _Quantile_function ,uint256 _n) internal pure returns (int256[] memory)
    {
        //generate n random integers normally distributed of mean x0 and standard deviation std
        int256[] memory random_quantiles =  randint(random_number, 0, int(_Quantile_function.length), _n);
        int256[] memory final_array = new int256[](_n);

        for (uint256 i = 0; i < _n; i++) {
            final_array[i] = _Quantile_function[uint(random_quantiles[i])];
        }

        return final_array;
    }




    function randint(uint256 random_number, int256 _a, int256 _b, uint256 _n) public pure returns (int256[] memory){ //returns n random integer between a and b (b included)

        //generate n random integers uniformly distributed between a and b
        
        require(_a<_b,"a should be lower than b");
        require(_n>0,"n should be higher than 0");

        uint256[] memory random_array = expand(random_number, _n);
        int256[] memory final_array = new int256[](_n);
        
        uint i=0;
        for (i = 0; i < _n; i++) {
            final_array[i] = (int(random_array[i]) % (_b-_a+1)) + _a;
            }

        return final_array;

    }

    function expand(uint256 randomValue, uint256 n) public pure returns (uint256[] memory expandedValues) {
        //generate n pseudorandom numbers from a single one
        //https://docs.chain.link/docs/chainlink-vrf-best-practices/#getting-multiple-random-numbers
        expandedValues = new uint256[](n);
        for (uint256 i = 0; i < n; i++) {
            expandedValues[i] = uint256(keccak256(abi.encode(randomValue, i)));
        }
        return expandedValues;
    }


    function _countOnes(uint256 n) internal pure returns (uint256 count) {
        //Count the number of ones in the binary representation
        /// internal function in assembly to count number of 1's
        /// https://www.geeksforgeeks.org/count-set-bits-in-an-integer/
        assembly {
            for { } gt(n, 0) { } {
                n := and(n, sub(n, 1))
                count := add(count, 1)
            }
        }
    }


    function log2(uint x) internal pure returns (uint y){
        //https://ethereum.stackexchange.com/questions/8086/logarithm-math-operation-in-solidity
        assembly {
            let arg := x
            x := sub(x,1)
            x := or(x, div(x, 0x02))
            x := or(x, div(x, 0x04))
            x := or(x, div(x, 0x10))
            x := or(x, div(x, 0x100))
            x := or(x, div(x, 0x10000))
            x := or(x, div(x, 0x100000000))
            x := or(x, div(x, 0x10000000000000000))
            x := or(x, div(x, 0x100000000000000000000000000000000))
            x := add(x, 1)
            let m := mload(0x40)
            mstore(m,           0xf8f9cbfae6cc78fbefe7cdc3a1793dfcf4f0e8bbd8cec470b6a28a7a5a3e1efd)
            mstore(add(m,0x20), 0xf5ecf1b3e9debc68e1d9cfabc5997135bfb7a7a3938b7b606b5b4b3f2f1f0ffe)
            mstore(add(m,0x40), 0xf6e4ed9ff2d6b458eadcdf97bd91692de2d4da8fd2d0ac50c6ae9a8272523616)
            mstore(add(m,0x60), 0xc8c0b887b0a8a4489c948c7f847c6125746c645c544c444038302820181008ff)
            mstore(add(m,0x80), 0xf7cae577eec2a03cf3bad76fb589591debb2dd67e0aa9834bea6925f6a4a2e0e)
            mstore(add(m,0xa0), 0xe39ed557db96902cd38ed14fad815115c786af479b7e83247363534337271707)
            mstore(add(m,0xc0), 0xc976c13bb96e881cb166a933a55e490d9d56952b8d4e801485467d2362422606)
            mstore(add(m,0xe0), 0x753a6d1b65325d0c552a4d1345224105391a310b29122104190a110309020100)
            mstore(0x40, add(m, 0x100))
            let magic := 0x818283848586878898a8b8c8d8e8f929395969799a9b9d9e9faaeb6bedeeff
            let shift := 0x100000000000000000000000000000000000000000000000000000000000000
            let alpha := div(mul(x, magic), shift)
            y := div(mload(add(m,sub(255,alpha))), shift)
            y := add(y, mul(256, gt(arg, 0x8000000000000000000000000000000000000000000000000000000000000000)))
        }  
    }

    function getArraySum(int256[] memory _array) 
        public 
        pure 
        returns (int256 sum_) 
    {
        sum_ = 0;
        for (uint i = 0; i < _array.length; i++) {
            sum_ += _array[i];
        }
    }



    function get_VRF_parameters(string memory chain_name) private pure returns (address, address, bytes32, uint256)
    {
        bool blockchain_exists;
        address VRFCoordinator_;
        address LinkToken_;
        bytes32 keyHash_;
        uint256 fee_;

        if (keccak256(bytes(chain_name)) == keccak256(bytes("polygon_mumbai"))) {
            VRFCoordinator_ = 0x8C7382F9D8f56b33781fE506E897a4F1e2d17255;
            LinkToken_ = 0x326C977E6efc84E512bB9C30f76E30c160eD06FB;
            keyHash_ = 0x6e75b569a01ef56d18cab6a8e71e6600d6ce853834d4a5748b720d06f878b3a4;
            fee_ = 0.0001*10**18;
            blockchain_exists = true;
        }

        require ( blockchain_exists==true, "VRF not available on this blockchain");

        return (VRFCoordinator_, LinkToken_, keyHash_, fee_);

    /*
    https://docs.chain.link/docs/vrf-contracts/

    Polygon Mumbai Testnet
        LINK Token	0x326C977E6efc84E512bB9C30f76E30c160eD06FB
        VRF Coordinator	0x8C7382F9D8f56b33781fE506E897a4F1e2d17255
        Key Hash	0x6e75b569a01ef56d18cab6a8e71e6600d6ce853834d4a5748b720d06f878b3a4
        Fee	0.0001 LINK
        Testnet LINK and MATIC are available from the official Matic faucet and https://faucets.chain.link/mumbai.

    Binance Smart Chain Testnet
        LINK	0x84b9B910527Ad5C03A9Ca831909E21e236EA7b06
        VRF Coordinator	0xa555fC018435bef5A13C6c6870a9d4C11DEC329C
        Key Hash	0xcaf3c3727e033261d383b315559476f48034c13b18f8cafed4d871abe5049186
        Fee	0.1 LINK
        Testnet LINK is available from https://faucets.chain.link/chapel

    Rinkeby Testnet
        LINK	0x01BE23585060835E02B77ef475b0Cc51aA1e0709
        VRF Coordinator	0xb3dCcb4Cf7a26f6cf6B120Cf5A73875B7BBc655B
        Key Hash	0x2ed0feb3e7fd2022120aa84fab1945545a9f2ffc9076fd6156fa96eaff4c1311
        Fee	0.1 LINK
        Testnet LINK is available from https://faucets.chain.link/rinkeby

    Kovan Testnet
        LINK	0xa36085F69e2889c224210F603D836748e7dC0088
        VRF Coordinator	0xdD3782915140c8f3b190B5D67eAc6dc5760C46E9
        Key Hash	0x6c3699283bda56ad74f6b855546325b68d482e983852a7a82979cc4807b641f4
        Fee	0.1 LINK
        Testnet LINK are available from https://faucets.chain.link/kovan
    */

    }


}


