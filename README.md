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
from moneyonchain.networks import NetworkManager
from moneyonchain.oracle import PriceProvider

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

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

price_provider = PriceProvider(network_manager)

log.info("Last price: {0}".format(price_provider.price()))

# finally disconnect from network
network_manager.disconnect()

```

result:

```
INFO:root:Connecting to mocTestnet...
INFO:root:Connected: True
INFO:root:Last price: 10725.4
```

RDOC Contract:

```
from moneyonchain.networks import NetworkManager
from moneyonchain.oracle import PriceProvider

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

connection_network='rskTesnetPublic'
config_network = 'rdocTestnet'

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

price_provider = PriceProvider(network_manager)

log.info("Last price: {0}".format(price_provider.price()))

# finally disconnect from network
network_manager.disconnect()

```

Result:

```
INFO:root:Connecting to rdocTestnet...
INFO:root:Connected: True
INFO:root:Last price: 0.092123288999999996
```


#### Mint BPro example

To run this script need private key, where replace with your PK in **PRIVATE_KEY**, and also you need to have funds in this account

```
martin@martin-desktop:~$ export ACCOUNT_PK_SECRET=PRIVATE_KEY
martin@martin-desktop:~$ python ./mint_bpro.py
```

Example code

```
from decimal import Decimal
from moneyonchain.networks import NetworkManager
from moneyonchain.moc import MoC

connection_network = 'rskTesnetPublic'
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


moc_main = MoC(network_manager).from_abi()

amount_want_to_mint = Decimal(0.001)

total_amount, commission_value = moc_main.amount_mint_bpro(amount_want_to_mint)
print("To mint {0} bitpro need {1} RBTC. Commision {2}".format(format(amount_want_to_mint, '.18f'),
                                                               format(total_amount, '.18f'),
                                                               format(commission_value, '.18f')))

print("Please wait to the transaction be mined!...")
tx_receipt = moc_main.mint_bpro(amount_want_to_mint)

# finally disconnect from network
network_manager.disconnect()

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
