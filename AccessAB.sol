pragma solidity ^0.8.0;

contract AccessAB{
    
    
    
    uint256 public count_a;
    uint256 public count_b;
    address payable wallet_reciever;
    string[] public ble_addresses_a;
    string[] public ble_addresses_b;
  
  
  constructor(address payable _wallet_reciever) public{
      wallet_reciever = _wallet_reciever;
  }
  
    function addAdress(string memory ble_add)  public payable {
         if (msg.value == 2000) {
             ble_addresses_a.push(ble_add);
             count_a +=1;
             }
         else if (msg.value ==3000){ 
             ble_addresses_b.push(ble_add);
             count_b +=1;
         }
         
        wallet_reciever.transfer(msg.value);
    }
    
}