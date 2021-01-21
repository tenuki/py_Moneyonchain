# Money On Chain

Python API to Money On Chain projects.

### Versions

There are 3 versions not compatible with each others

* Release 0.X.X: (STABLE) This is current master, this will deprecated in our future.
* Release 1.X.X: (ALPHA) This is will introduced breaking changes in contract not compatible with older versions
* Release 2.X.X: (ALPHA) This is will introduced breaking changes, rework of the api, make support using brownie lib

### Requirements

* Python 3.6+ support

### Installation

```
pip3 install moneyonchain
```

or with specific version

```
pip3 install moneyonchain==2.0.0
```


### Usage

#### Network manager 

Network manager manage connection to node and other specific to current connected network. By default if you run the
first time .install(), this will install current used networks of our enviroments by brownie.

First time you are going to interect with our api you will need to install predefined connections networks

```
from moneyonchain.networks import NetworkManager

connection_network='rskTesnetPublic'
config_network = 'mocTestnet'

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network=connection_network,
    config_network=config_network)

# run install() if is the first time and you want to install
# networks connection from brownie
network_manager.install()

```

#### Connection table

| Network Name      | Network node          | Host                               | Chain    |
|-------------------|-----------------------|------------------------------------|----------|
| rskTesnetPublic   | RSK Testnet Public    | https://public-node.testnet.rsk.co | 31       |    
| rskTesnetLocal    | RSK Testnet Local     | http://localhost:4444              | 31       |
| rskMainnetPublic  | RSK Mainnet Public    | https://public-node.rsk.co         | 30       |
| rskMainnetLocal   | RSK Mainnet Local     | http://localhost:4444              | 30       |


Example 1. Connect by default to RSK Testnet public node and to mocTestnet enviroment and print is connected

```
from moneyonchain.networks import NetworkManager


connection_network='rskTesnetPublic'
config_network = 'mocTestnet'

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network=connection_network,
    config_network=config_network)

# run install() if is the first time and you want to install
# networks connection from brownie
# network_manager.install()

# Connect to network
network_manager.connect()

print(network_manager.is_connected())

# finally disconnect from network
network_manager.disconnect()

```

#### Enviroment table

| Network Name      | Project | Enviroment                       | Network    |
|-------------------|---------|----------------------------------|------------|
| mocTestnetAlpha   | MOC     |                                  | Testnet    |
| mocTestnet        | MOC     | moc-testnet.moneyonchain.com     | Testnet    |
| mocMainnet2       | MOC     | alpha.moneyonchain.com           | Mainnet    |
| rdocTestnetAlpha  | RIF     |                                  | Testnet    |
| rdocTestnet       | RIF     | rif-testnet.moneyonchain.com     | Testnet    |
| rdocMainnet       | RIF     | rif.moneyonchain.com             | Mainnet    |
| dexTestnet        | TEX     | tex-testnet.moneyonchain.com     | Testnet    |
| dexMainnet        | TEX     | tex.moneyonchain.com             | Mainnet    |

#### Price provider

Get the last price from MOC or RDOC contract.

See example in source/example/price_provider.py


```
from moneyonchain.manager import ConnectionManager
from moneyonchain.price_provider import PriceProvider

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

# Connect to MoC enviroment network
network = 'mocTestnet'
connection_manager = ConnectionManager(network=network)
log.info("Connecting to %s..." % network)
log.info("Connected: {conectado}".format(conectado=connection_manager.is_connected))

price_provider = PriceProvider(connection_manager)

log.info("Last price: {0}".format(price_provider.price()))

```

result:

```
INFO:root:Connecting to mocTestnet...
INFO:root:Connected: True
INFO:root:Last price: 10725.4
```

RDOC Contract:

```
from moneyonchain.manager import ConnectionManager
from moneyonchain.price_provider import PriceProvider

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

# Connect to MoC enviroment network
network = 'rdocTestnet'
connection_manager = ConnectionManager(network=network)
log.info("Connecting to %s..." % network)
log.info("Connected: {conectado}".format(conectado=connection_manager.is_connected))

price_provider = PriceProvider(connection_manager)

log.info("Last price: {0}".format(price_provider.price()))
```

Result:

```
INFO:root:Connecting to rdocTestnet...
INFO:root:Connected: True
INFO:root:Last price: 0.092123288999999996
```

#### Token Prices

Get token prices in Dollar

```
from moneyonchain.manager import ConnectionManager
from moneyonchain.moc import MoC

network = 'mocMainnet2'
connection_manager = ConnectionManager(network=network)
print("Connecting to %s..." % network)
print("Connected: {conectado}".format(conectado=connection_manager.is_connected))

contract = MoC(connection_manager)
print("Bitcoin price in usd: {0}".format(contract.bitcoin_price()))
print("BPRO price in usd: {0}".format(contract.bpro_price()))
print("BTC2X price in usd: {0}".format(contract.btc2x_tec_price() * contract.bitcoin_price()))

```

result:

```
Connecting to mocMainnet2...
Connected: True
Bitcoin price in usd: 9405.100000000000247435
BPRO price in usd: 9702.108188434730668324
BTC2X price in usd: 11869.45000000000341040779478
```


#### DOC Token example

Connect to moc-testnet avalaible trought https://moc-testnet.moneyonchain.com
DoCToken is Dollar on Chain Token

``` 
from moneyonchain.manager import ConnectionManager
from moneyonchain.token import DoCToken


network = 'mocTestnet'
connection_manager = ConnectionManager(network=network)
print("Connecting to %s..." % network)
print("Connected: {conectado}".format(conectado=connection_manager.is_connected))

account = '0xCD8a1C9aCC980Ae031456573e34Dc05CD7dAE6e3'

print("Connecting to DoCToken")
doc_token = DoCToken(connection_manager)
print("Token Name: {0}".format(doc_token.name()))
print("Token Symbol: {0}".format(doc_token.symbol()))
print("Total Supply: {0}".format(doc_token.total_supply()))
print("Account: {0} Balance DOC: {1}".format(account, doc_token.balance_of(account)))
```

this print

```
Connecting to mocTestnet...
Connected: True
Connecting to DoCToken
Token Name: Dollar on Chain
Token Symbol: DOC
Total Supply: 62398.334981863939176967
Account: 0xCD8a1C9aCC980Ae031456573e34Dc05CD7dAE6e3 Balance DOC: 443.294681738027382034
```


#### RIF Token example balance

**Mainnet**

Connect to RDOC Mainnet avalaible trought https://rif.moneyonchain.com

``` 
from moneyonchain.manager import ConnectionManager
from moneyonchain.token import RIF


network = 'rdocMainnet'
connection_manager = ConnectionManager(network=network)
print("Connecting to %s..." % network)
print("Connected: {conectado}".format(conectado=connection_manager.is_connected))

account = '0xCD8a1C9aCC980Ae031456573e34Dc05CD7dAE6e3'

print("Connecting to RIF TOKEN")
rif_token = RIF(connection_manager)
print("Token Name: {0}".format(rif_token.name()))
print("Token Symbol: {0}".format(rif_token.symbol()))
print("Total Supply: {0}".format(rif_token.total_supply()))
print("Account: {0} Balance RIF: {1}".format(account, rif_token.balance_of(account)))
```

this print

```
Connecting to rdocMainnet...
Connected: True
Connecting to RIF TOKEN
Token Name: tRIF Token
Token Symbol: tRIF
Total Supply: 1000000000
Account: 0xCD8a1C9aCC980Ae031456573e34Dc05CD7dAE6e3 Balance RIF: 391.072191029720048275
```



**Testnet**

Connect to RDOC Testnet avalaible trought https://rif-testnet.moneyonchain.com

``` 
from moneyonchain.manager import ConnectionManager
from moneyonchain.token import RIF


network = 'rdocTestnet'
connection_manager = ConnectionManager(network=network)
print("Connecting to %s..." % network)
print("Connected: {conectado}".format(conectado=connection_manager.is_connected))

account = '0xCD8a1C9aCC980Ae031456573e34Dc05CD7dAE6e3'

print("Connecting to RIF TOKEN")
rif_token = RIF(connection_manager)
print("Token Name: {0}".format(rif_token.name()))
print("Token Symbol: {0}".format(rif_token.symbol()))
print("Total Supply: {0}".format(rif_token.total_supply()))
print("Account: {0} Balance RIF: {1}".format(account, rif_token.balance_of(account)))
```

this print

```
Connecting to rdocTestnet...
Connected: True
Connecting to RIF TOKEN
Token Name: tRIF Token
Token Symbol: tRIF
Total Supply: 1000000000
Account: 0xCD8a1C9aCC980Ae031456573e34Dc05CD7dAE6e3 Balance RIF: 391.072191029720048275
```



#### Mint BPro example

To run this script need private key, where replace with your PK in **PRIVATE_KEY**, and also you need to have funds in this account

```
martin@martin-desktop:~$ export ACCOUNT_PK_SECRET=PRIVATE_KEY
martin@martin-desktop:~$ python ./example_moc_mint_bpro.py
```

Example code

```
from decimal import Decimal
from web3 import Web3
from moneyonchain.manager import ConnectionManager
from moneyonchain.moc import MoC


network = 'mocTestnet'
connection_manager = ConnectionManager(network=network)
print("Connecting to %s..." % network)
print("Connected: {conectado}".format(conectado=connection_manager.is_connected))

print("Connecting to MoC Main Contract")
moc_main = MoC(connection_manager)

amount_want_to_mint = Decimal(0.001)

total_amount, commission_value = moc_main.amount_mint_bpro(amount_want_to_mint)
print("To mint {0} bitpro need {1} RBTC. Commision {2}".format(format(amount_want_to_mint, '.18f'),
                                                               format(total_amount, '.18f'),
                                                               format(commission_value, '.18f')))

# Mint BPro
# This transaction is not async, you have to wait to the transaction is mined
print("Please wait to the transaction be mined!...")
tx_hash, tx_receipt, tx_logs = moc_main.mint_bpro(amount_want_to_mint)
if tx_logs:
    print("Transaction done!")
    amount = Decimal(Web3.fromWei(tx_logs[0]['args']['amount'], 'ether'))
    amount_usd = moc_main.bpro_amount_in_usd(amount)
    print("You mint {0} BPro equivalent to {1} USD".format(format(amount, '.18f'), format(amount_usd, '.3f')))
else:
    print("Transaction Failed")
```

this print

```
Connecting to mocTestnet...
Connected: True
Connecting to MoC Main Contract
To mint 0.001000000000000000 bitpro need 0.001001000000000000 RBTC. Commision 0.000001000000000000
Please wait to the transaction be mined!...
Transaction done!
You mint 0.000965723337947316 BPro equivalent to 7.107 USD
```
