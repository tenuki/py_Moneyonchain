"""
If is the first time to py_Moneyonchain we need brownie framework installed

`pip install eth-brownie==1.12.2`

and to install connection nodes required to connect, also run :

```
console> brownie networks add RskNetwork rskTestnetPublic host=https://public-node.testnet.rsk.co chainid=31 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskTestnetLocal host=http://localhost:4444 chainid=31 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskMainnetPublic host=https://public-node.rsk.co chainid=30 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskMainnetLocal host=http://localhost:4444 chainid=30 explorer=https://blockscout.com/rsk/mainnet/api
```

To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./mint_btcx.py

Where replace with your PK, and also you need to have funds in this account
"""

from decimal import Decimal
from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC

connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_main = MoC(network_manager).from_abi()

vendor_account = Web3.toChecksumAddress('0xDda74880D638451e6D2c8D3fC19987526A7Af730')
#vendor_account = Web3.toChecksumAddress('0xf69287F5Ca3cC3C6d3981f2412109110cB8af076')
amount_want_to_mint = Decimal(0.001)

BUCKET_X2 = '0x5832000000000000000000000000000000000000000000000000000000000000'
bucket = BUCKET_X2

total_amount, commission_value, markup_value, interest_value = moc_main.amount_mint_btc2x(
    amount=amount_want_to_mint,
    vendor_account=vendor_account)

print("To mint {0} BTC2X need {1} RBTC. Commission {2}. Markup {3}. Interest: {4}".format(
    format(amount_want_to_mint, '.18f'),
    format(total_amount, '.18f'),
    format(commission_value, '.18f'),
    format(markup_value, '.18f'),
    format(interest_value, '.18f')))

tx_args = moc_main.tx_arguments()

tx_args['amount'] = int(total_amount * moc_main.precision)
tx_receipt = moc_main.sc.mintBProxVendors(
    bucket, int(amount_want_to_mint * moc_main.precision),
    vendor_account,
    tx_args)

tx_receipt.info()

# finally disconnect from network
network_manager.disconnect()
