
import json
import asyncio
from beacontools import BeaconScanner,  EddystoneUIDFrame
from web3 import Web3



list_a = []
list_b= []



def callback(bt_addr, rssi, packet, additional_info):
    received_ble = packet.namespace+packet.instance
    print("ble: "+received_ble)
    compare_bles(received_ble)


def compare_bles(received_ble):
    global list_a
    if received_ble in list_a :
        print("Access A granted")
    else:
        print("Access A denied")
    
    global list_b
    if received_ble in  list_b:
        print("Access B granted")
        print("")
    else:
        print("Access B denied ")
        print("")
        


def getContracts_a(count):
   #get all addresses from smart contract
  for x_add in range(count):
    currentcontract = contract.functions.ble_addresses_a(x_add).call()
    global list_a
    list_a.append(currentcontract)
    list_a = list(set(list_a))

  


def getContracts_b(count):
  # get all addresses from smart contract
  for x_add in range(count):
    currentcontract = contract.functions.ble_addresses_b(x_add).call()
    global list_b
    list_b.append(currentcontract)
    list_b = list(set(list_b))

def printLists():
    print("List Access A: ")
    print(*list_a, sep = ", ")
    print("")
    print("List Access B: ")
    print(*list_b, sep = ", ")
    print("")


#Ethereum Node
infura_url = 'https://rinkeby.infura.io/v3/fcbf73400bbb48b28291758dd4e2b8f5'
web3 = Web3(Web3.HTTPProvider(infura_url))
print(web3.isConnected())



#Smart Contract 
abi = json.loads('[{"inputs":[{"internalType":"address payable","name":"_wallet_reciever","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"string","name":"ble_add","type":"string"}],"name":"addAdress","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"ble_addresses_a","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"ble_addresses_b","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"count_a","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"count_b","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
address = web3.toChecksumAddress("0xdf24542177e1e86e016fea56bca8002597147d1e")
contract = web3.eth.contract(address = address, abi=abi)
print(contract)


scanner = BeaconScanner(
    callback,
    packet_filter=[EddystoneUIDFrame]
)

#for access A
async def ble_sc():
  while True:
    try:
      getContracts_a(contract.functions.count_a().call())
    except Exception as e:
      print(str(e))
  #for access B
    try:
      getContracts_b(contract.functions.count_b().call())
    except Exception as e:
      print(str(e))
    printLists()
    await asyncio.sleep(10)

async def scanBle():
  while True:
    scanner.start()
    await asyncio.sleep(2)
    
    
loop = asyncio.get_event_loop()
cors = asyncio.wait([ble_sc(), scanBle()])
loop.run_until_complete(cors)
