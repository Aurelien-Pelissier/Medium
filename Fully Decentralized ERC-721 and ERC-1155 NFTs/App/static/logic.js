const web3 = new Web3(window.ethereum);
const serverUrl = "";
const appId = "";
Moralis.start({ serverUrl, appId });

const nft721_contract_address = "0x73374074a68F14082B02f07Cf5977D1d881863CC";
const nft1155_contract_address = "0xfB4c37dD4BebaBAE4C0faa7002e0149100ca2091";

/*
Available deployed contracts for ERC721:
AVAX testnet      0x73374074a68F14082B02f07Cf5977D1d881863CC
Ethereum Rinkeby  0x0Fb6EF3505b9c52Ed39595433a21aF9B5FCc4431
Polygon Mumbai    0x351bbee7C6E9268A1BF741B098448477E08A0a53
BSC Testnet       0x88624DD1c725C6A95E223170fa99ddB22E1C6DDD

Available deployed contracts for ERC1155:
AVAX testnet      0xfB4c37dD4BebaBAE4C0faa7002e0149100ca2091
Ethereum Rinkeby  0x48A89BA403D049fda25a0fe5a5Ff4F1B41dc541b
Polygon Mumbai    0xe4f4b2678bC2b646d93A87c90fb90170373fE850
BSC Testnet       0x373f230f4A38553Df4b0028b2FD578a251deC7e5
*/


//frontend logic

document.getElementById("btn-login").onclick = login;

async function login() {
  user = await Moralis.authenticate();
  document.getElementById("upload721").removeAttribute("disabled");
  document.getElementById("file721").removeAttribute("disabled");
  document.getElementById("name721").removeAttribute("disabled");
  document.getElementById("description721").removeAttribute("disabled");

  document.getElementById("upload1155").removeAttribute("disabled");
  document.getElementById("file1155").removeAttribute("disabled");
  document.getElementById("name1155").removeAttribute("disabled");
  document.getElementById("description1155").removeAttribute("disabled");
  document.getElementById("amount1155").removeAttribute("disabled");

  const txt = 'Login Successfull with address ' + ethereum.selectedAddress
  console.log(txt)
  notifyLogin(txt)
}



async function upload721(){
  const fileInput = document.getElementById("file721");
  const data = fileInput.files[0];
  const imageFile = new Moralis.File(data.name, data);
  document.getElementById('upload721').setAttribute("disabled", null);
  document.getElementById('file721').setAttribute("disabled", null);
  document.getElementById('name721').setAttribute("disabled", null);
  document.getElementById('description721').setAttribute("disabled", null);

  console.log('Uploading file to IPFS...')
  await imageFile.saveIPFS();
  const imageURI = imageFile.ipfs();
  const metadata = {
    "name":document.getElementById("name721").value,
    "description":document.getElementById("description721").value,
    "image":imageURI
  };
  const metadataFile = new Moralis.File("metadata.json", {base64 : btoa(JSON.stringify(metadata))});
  await metadataFile.saveIPFS();
  const metadataURI = metadataFile.ipfs();
  console.log(metadataURI);
  console.log('Minting NFT...');

  const txt = await mintToken721(metadataURI).then(notifyERC721);
  console.log('Successfully minted');
}




async function upload1155(){
  const fileInput = document.getElementById("file1155");
  const data = fileInput.files[0];
  const imageFile = new Moralis.File(data.name, data);
  document.getElementById('upload1155').setAttribute("disabled", null);
  document.getElementById('file1155').setAttribute("disabled", null);
  document.getElementById('name1155').setAttribute("disabled", null);
  document.getElementById('description1155').setAttribute("disabled", null);
  document.getElementById('amount1155').setAttribute("disabled", null);

  console.log('Uploading file to IPFS...')
  await imageFile.saveIPFS();
  const imageURI = imageFile.ipfs();
  const metadata = {
    "name":document.getElementById("name1155").value,
    "description":document.getElementById("description1155").value,
    "image":imageURI
  };
  const metadataFile = new Moralis.File("metadata.json", {base64 : btoa(JSON.stringify(metadata))});
  await metadataFile.saveIPFS();
  const metadataURI = metadataFile.ipfs();
  const amount = document.getElementById("amount1155").value;
  console.log(metadataURI);
  console.log('Minting NFT...');

  const txt = await mintToken1155(metadataURI,amount).then(notifyERC1155);
  console.log('Successfully minted');
}




async function mintToken721(_uri){
  const encodedFunction = web3.eth.abi.encodeFunctionCall({
    name: "mintToken",
    type: "function",
    inputs: [{
      type: 'string',
      name: 'tokenURI'
      }]
  }, [_uri]);

  const transactionParameters = {
    to: nft721_contract_address,
    from: ethereum.selectedAddress,
    data: encodedFunction
  };
  const txt = await ethereum.request({
    method: 'eth_sendTransaction',
    params: [transactionParameters]
  });
  return txt;
}


async function mintToken1155(_uri, _amount){
  const encodedFunction = web3.eth.abi.encodeFunctionCall({
    name: "mintToken",
    type: "function",
    inputs: [{
      type: 'string',
      name: 'tokenURI'
      },{
      type: 'uint256',
      name: 'amount'      
      }]
  }, [_uri,_amount]);

  const transactionParameters = {
    to: nft1155_contract_address,
    from: ethereum.selectedAddress,
    data: encodedFunction
  };
  const txt = await ethereum.request({
    method: 'eth_sendTransaction',
    params: [transactionParameters]
  });
  return txt;
}



async function notifyLogin(_txt){
  document.getElementById("resultSpaceLogin").innerHTML =  
  `<input disabled = "true" id="result" type="text" class="form-control" placeholder="Description" aria-label="URL" aria-describedby="basic-addon1" value="${_txt}">`;
} 
async function notifyERC721(_txt){
  document.getElementById("resultSpaceERC721").innerHTML =  
  `<input disabled = "true" id="result" type="text" class="form-control" placeholder="Description" aria-label="URL" aria-describedby="basic-addon1" value="Your ERC721 NFT was successfully minted in transaction ${_txt}">`;
} 
async function notifyERC1155(_txt){
  document.getElementById("resultSpaceERC1155").innerHTML =  
  `<input disabled = "true" id="result" type="text" class="form-control" placeholder="Description" aria-label="URL" aria-describedby="basic-addon1" value="Your ERC1155 NFT was successfully minted in transaction ${_txt}">`;
} 

