import json

from moneyonchain.networks import NetworkManager
from moneyonchain.moc import MoCSetCommissionMocProportionChanger


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/10_changer_proportion.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'rskTesnetPublic'
config_network = 'mocTestnetAlpha'

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


# load settings from file, take a look on settings.json
settings = options_from_settings()

contract_splitter = settings[config_network]['CommissionSplitter']
contract = MoCSetCommissionMocProportionChanger(network_manager)

if config_network in ['mocTestnetAlpha']:
    execute_change = True
else:
    execute_change = False

proportion = 200000000000000000
tx_hash, tx_receipt = contract.constructor(proportion,
                                           commission_splitter=contract_splitter,
                                           execute_change=execute_change)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    print("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
