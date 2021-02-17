"""
Testnet

RDOC: 0xC3De9F38581f83e281f260d0DdbaAc0e102ff9F8
DOC: 0xCB46c0ddc60D18eFEB0E586C17Af6ea36452Dae0
WRBTC: 0x09b6ca5E4496238A1F176aEa6Bb607DB96c2286E
BPRO: 0x4dA7997A819bb46B6758B9102234c289dD2Ad3bf
RIF: 0x19F64674D8A5B4E652319F5e239eFd3bc969A1fE
RIFP: 0x23A1aA7b11e68beBE560a36beC04D1f79357f28d


1. DOC / WRBTC  <--
2. DOC / RDOC <--
3. DOC / BPRO
4. WRBTC / BPRO <--
5. DOC / RIF
6. RDOC / RIFP
7. RIF / RIFP <--

8. DOC/ADOC
9. ADOC/ABPRO




Mainnet

RDOC: 0x2d919F19D4892381D58edeBeca66D5642Cef1a1f
DOC: 0xe700691dA7b9851F2F35f8b8182c69c53CcaD9Db
WRBTC: 0x967f8799aF07DF1534d48A95a5C9FEBE92c53ae0
BPRO: 0x440CD83C160De5C96Ddb20246815eA44C7aBBCa8
RIF: 0x2acc95758f8b5f583470ba265eb685a8f45fc9d5
RIFP: 0xf4d27c56595Ed59B66cC7F03CFF5193e4bd74a61


1. DOC / WRBTC  <--
2. DOC / RDOC <--
3. DOC / BPRO
4. WRBTC / BPRO <--
5. DOC / RIF
6. RDOC / RIFP
7. RIF / RIFP <--
"""

import json
from moneyonchain.networks import NetworkManager
from moneyonchain.tex import DexAddTokenPairChanger
from moneyonchain.tex import ExternalOraclePriceProviderFallback, \
    TokenPriceProviderLastClosingPrice, \
    UnityPriceProvider, \
    MocBproUsdPriceProviderFallback, \
    MocBproBtcPriceProviderFallback, \
    MocRiskProUsdPriceProviderFallback, \
    MocRiskProReservePriceProviderFallback

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/add_pair.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


connection_network = 'rskTestnetPublic'
config_network = 'dexTestnet'

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

# load settings from file
settings = options_from_settings()

settings_pair = settings[config_network]['ADOC/ABPRO']

base_token = settings_pair['baseToken']
secondary_token = settings_pair['secondaryToken']
init_price = int(settings_pair['price'])
price_precision = int(settings_pair['precision'])
provider_type = settings_pair['provider']['type']
provider_external = settings_pair['provider']['address']

log.info("Deploying Price provider ...")

if provider_type in ['external']:
    price_provider = ExternalOraclePriceProviderFallback(network_manager)
    tx_receipt = price_provider.constructor(
        provider_external,
        base_token,
        secondary_token)
elif provider_type in ['unity']:
    price_provider = UnityPriceProvider(network_manager)
    tx_receipt = price_provider.constructor()
elif provider_type in ['bpro_usd']:
    price_provider = MocBproUsdPriceProviderFallback(network_manager)
    tx_receipt = price_provider.constructor(
        provider_external,
        base_token,
        secondary_token)
elif provider_type in ['bpro_btc']:
    price_provider = MocBproBtcPriceProviderFallback(network_manager)
    tx_receipt = price_provider.constructor(
        provider_external,
        base_token,
        secondary_token)
elif provider_type in ['riskpro_reserve']:
    price_provider = MocRiskProReservePriceProviderFallback(network_manager)
    tx_receipt = price_provider.constructor(
        provider_external,
        base_token,
        secondary_token)
elif provider_type in ['riskpro_usd']:
    price_provider = MocRiskProUsdPriceProviderFallback(network_manager)
    tx_receipt = price_provider.constructor(
        provider_external,
        base_token,
        secondary_token)
else:
    raise Exception("Invalid provider type")

price_provider_address = None
if tx_receipt:
    price_provider_address = tx_receipt.contract_address
    log.info("Price provider deployed Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying price provider")

if price_provider_address:
    log.info("Deploying add pair changer....")

    contract = DexAddTokenPairChanger(network_manager)

    tx_receipt = contract.deploy(
        base_token,
        secondary_token,
        price_provider_address,
        price_precision,
        init_price,
        execute_change=False)

    if tx_receipt:
        log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
        tx_receipt.info()
        tx_receipt.info_to_log()
    else:
        log.info("Error deploying changer")

"""
1.DOC/WRBTC

2020-11-20 08:32:34 default      INFO     Connecting to dexMainnet...
2020-11-20 08:32:35 default      INFO     Connected: True
2020-11-20 08:32:35 default      INFO     Deploying Price provider ...
2020-11-20 08:32:35 root         INFO     Deploying new contract...
2020-11-20 08:33:52 root         INFO     Deployed contract done!
2020-11-20 08:33:52 root         INFO     0xb496361ab3a5b1124b57612f863969f79f721564b430ec9e886e27947d6aa666
2020-11-20 08:33:52 root         INFO     AttributeDict({'transactionHash': HexBytes('0xb496361ab3a5b1124b57612f863969f79f721564b430ec9e886e27947d6aa666'), 'transactionIndex': 2, 'blockHash': HexBytes('0x624b523fe35f2f0f9ce63eae5030b08c16d6075bdf1643b0e4e4db917e5e71c7'), 'blockNumber': 2878303, 'cumulativeGasUsed': 839770, 'gasUsed': 328241, 'contractAddress': '0xE9ffC82f1a2D3E796Fe5167c372b84F15a1Db7f7', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:33:52 root         INFO     Contract Address: 0xE9ffC82f1a2D3E796Fe5167c372b84F15a1Db7f7
2020-11-20 08:33:52 default      INFO     Price provider deployed Contract Address: 0xE9ffC82f1a2D3E796Fe5167c372b84F15a1Db7f7
2020-11-20 08:33:52 default      INFO     Deploying add pair changer....
2020-11-20 08:33:52 root         INFO     Deploying new contract...
2020-11-20 08:34:53 root         INFO     Deployed contract done!
2020-11-20 08:34:53 root         INFO     0xf7a87e05250d84a9d152c838d02caccc74db4c544809532a4ddb2952b681a128
2020-11-20 08:34:53 root         INFO     AttributeDict({'transactionHash': HexBytes('0xf7a87e05250d84a9d152c838d02caccc74db4c544809532a4ddb2952b681a128'), 'transactionIndex': 1, 'blockHash': HexBytes('0x3f503f9c21255cbe95ff1a998081a1cb611df9342b1740ae2f1161731d906232'), 'blockNumber': 2878304, 'cumulativeGasUsed': 628330, 'gasUsed': 567254, 'contractAddress': '0x9a2eA7310C5058467454F8E3F99aD25f0Af5ED19', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:34:53 root         INFO     Changer Contract Address: 0x9a2eA7310C5058467454F8E3F99aD25f0Af5ED19
2020-11-20 08:34:53 root         INFO     Executing change....
2020-11-20 08:35:19 root         INFO     0x58247731732d86ab1caaab9c7d63470104d8d573aa318f761178f63fe1862826
2020-11-20 08:35:19 root         INFO     AttributeDict({'transactionHash': HexBytes('0x58247731732d86ab1caaab9c7d63470104d8d573aa318f761178f63fe1862826'), 'transactionIndex': 0, 'blockHash': HexBytes('0x7a7738708a578777125a8a502bb8b1a942f1f19a2d060ec6004ad70c76363dbf'), 'blockNumber': 2878306, 'cumulativeGasUsed': 901793, 'gasUsed': 901793, 'contractAddress': None, 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': '0x036CaF1d8B11d46F5D819241cFFAC06cDF9Fd230', 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:35:19 root         INFO     Change successfull!
2020-11-20 08:35:19 default      INFO     Changer Contract Address: None

2. DOC/RDOC

2020-11-20 08:37:20 default      INFO     Connecting to dexMainnet...
2020-11-20 08:37:21 default      INFO     Connected: True
2020-11-20 08:37:21 default      INFO     Deploying Price provider ...
2020-11-20 08:37:21 root         INFO     Deploying new contract...
2020-11-20 08:38:27 root         INFO     Deployed contract done!
2020-11-20 08:38:27 root         INFO     0x0d021078d1888a6742e332a6e5ebc20f3b6b344753c0f68f02d8940dab86e50b
2020-11-20 08:38:27 root         INFO     AttributeDict({'transactionHash': HexBytes('0x0d021078d1888a6742e332a6e5ebc20f3b6b344753c0f68f02d8940dab86e50b'), 'transactionIndex': 0, 'blockHash': HexBytes('0x4741b90c4e7da42a253da3138f4506b61bd476c4f52e1fc445c869223421cb39'), 'blockNumber': 2878310, 'cumulativeGasUsed': 96379, 'gasUsed': 96379, 'contractAddress': '0xafcC9b6E4a58E9A505F5bbe6b93798feF3131FF7', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:38:27 root         INFO     Contract Address: 0xafcC9b6E4a58E9A505F5bbe6b93798feF3131FF7
2020-11-20 08:38:27 default      INFO     Price provider deployed Contract Address: 0xafcC9b6E4a58E9A505F5bbe6b93798feF3131FF7
2020-11-20 08:38:27 default      INFO     Deploying add pair changer....
2020-11-20 08:38:27 root         INFO     Deploying new contract...
2020-11-20 08:39:55 root         INFO     Deployed contract done!
2020-11-20 08:39:55 root         INFO     0x77a4bdea875f7b709f4dd8cd42b7c9388fc6078ba16c5d9996b5498bb9cb6e71
2020-11-20 08:39:55 root         INFO     AttributeDict({'transactionHash': HexBytes('0x77a4bdea875f7b709f4dd8cd42b7c9388fc6078ba16c5d9996b5498bb9cb6e71'), 'transactionIndex': 1, 'blockHash': HexBytes('0xef3f77cf3b8529432e876102f6676f8cd2e9f98434a4aa5a44b791aa484e777d'), 'blockNumber': 2878312, 'cumulativeGasUsed': 627059, 'gasUsed': 567126, 'contractAddress': '0x2ab00B3f74019c62F5F455F0DaBf4D4c9CC52f7F', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:39:55 root         INFO     Changer Contract Address: 0x2ab00B3f74019c62F5F455F0DaBf4D4c9CC52f7F
2020-11-20 08:39:55 root         INFO     Executing change....
2020-11-20 08:40:51 root         INFO     0xf1961e4cde1298443dd794e31993abf4541ce35a3bbd3dc22d5cbd33f4dcc5f5
2020-11-20 08:40:51 root         INFO     AttributeDict({'transactionHash': HexBytes('0xf1961e4cde1298443dd794e31993abf4541ce35a3bbd3dc22d5cbd33f4dcc5f5'), 'transactionIndex': 1, 'blockHash': HexBytes('0x006d1f107bc6d1de6b6ccc0d0f1b86ce6ebfc834b43341549150f13fddf32968'), 'blockNumber': 2878313, 'cumulativeGasUsed': 1146677, 'gasUsed': 871793, 'contractAddress': None, 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': '0x036CaF1d8B11d46F5D819241cFFAC06cDF9Fd230', 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:40:51 root         INFO     Change successfull!
2020-11-20 08:40:51 default      INFO     Changer Contract Address: None

3. DOC/BPRO

2020-11-20 08:41:40 default      INFO     Connecting to dexMainnet...
2020-11-20 08:41:41 default      INFO     Connected: True
2020-11-20 08:41:41 default      INFO     Deploying Price provider ...
2020-11-20 08:41:41 root         INFO     Deploying new contract...
2020-11-20 08:42:28 root         INFO     Deployed contract done!
2020-11-20 08:42:28 root         INFO     0x859dea093d2552242b44b965794e2453a76eb1790dc0d5a558c84d85efb35855
2020-11-20 08:42:28 root         INFO     AttributeDict({'transactionHash': HexBytes('0x859dea093d2552242b44b965794e2453a76eb1790dc0d5a558c84d85efb35855'), 'transactionIndex': 1, 'blockHash': HexBytes('0x10a5c4383f64eff3ffe6a96b06ad5e9a5bf5630e9e0776883c45cdcf3661fce4'), 'blockNumber': 2878315, 'cumulativeGasUsed': 472868, 'gasUsed': 403588, 'contractAddress': '0x5FC3aaC83E24825D54f494e8bEe932e66EAF972b', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:42:28 root         INFO     Contract Address: 0x5FC3aaC83E24825D54f494e8bEe932e66EAF972b
2020-11-20 08:42:28 default      INFO     Price provider deployed Contract Address: 0x5FC3aaC83E24825D54f494e8bEe932e66EAF972b
2020-11-20 08:42:28 default      INFO     Deploying add pair changer....
2020-11-20 08:42:28 root         INFO     Deploying new contract...
2020-11-20 08:43:32 root         INFO     Deployed contract done!
2020-11-20 08:43:32 root         INFO     0xe7c02e26fbbf77f1595a45606ac2b42fadc33e7469339df3c0ab5d51125a0a17
2020-11-20 08:43:32 root         INFO     AttributeDict({'transactionHash': HexBytes('0xe7c02e26fbbf77f1595a45606ac2b42fadc33e7469339df3c0ab5d51125a0a17'), 'transactionIndex': 0, 'blockHash': HexBytes('0x6888d315435dc5960a589b62580b5ce7efba8e3b517e69b5195e6b6f5700bd00'), 'blockNumber': 2878316, 'cumulativeGasUsed': 567254, 'gasUsed': 567254, 'contractAddress': '0xEbE37DdF8d47Eda70510556Ea68A4aB9CA32d8d6', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:43:32 root         INFO     Changer Contract Address: 0xEbE37DdF8d47Eda70510556Ea68A4aB9CA32d8d6
2020-11-20 08:43:32 root         INFO     Executing change....
2020-11-20 08:44:55 root         INFO     0x14449ce9be18387bd129f2882e9875a3659d438421cc0594f84ded9b2a04660a
2020-11-20 08:44:55 root         INFO     AttributeDict({'transactionHash': HexBytes('0x14449ce9be18387bd129f2882e9875a3659d438421cc0594f84ded9b2a04660a'), 'transactionIndex': 1, 'blockHash': HexBytes('0xc3d760cf8a608ce76d9876b79f572af0738093d620ab2dd5ae6e3b53217e9e7b'), 'blockNumber': 2878318, 'cumulativeGasUsed': 1138845, 'gasUsed': 871793, 'contractAddress': None, 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': '0x036CaF1d8B11d46F5D819241cFFAC06cDF9Fd230', 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:44:55 root         INFO     Change successfull!
2020-11-20 08:44:55 default      INFO     Changer Contract Address: None


4.WRBTC/BPRO

2020-11-20 08:46:00 default      INFO     Connecting to dexMainnet...
2020-11-20 08:46:01 default      INFO     Connected: True
2020-11-20 08:46:01 default      INFO     Deploying Price provider ...
2020-11-20 08:46:01 root         INFO     Deploying new contract...
2020-11-20 08:46:32 root         INFO     Deployed contract done!
2020-11-20 08:46:32 root         INFO     0xcc81ad8f6e323e3a01a1342e5c879b1eea5aa1f8e41d0277a614d73ca7c224db
2020-11-20 08:46:32 root         INFO     AttributeDict({'transactionHash': HexBytes('0xcc81ad8f6e323e3a01a1342e5c879b1eea5aa1f8e41d0277a614d73ca7c224db'), 'transactionIndex': 0, 'blockHash': HexBytes('0x57d72a2f496a0c1934b5504c81296b2a077e26403eb6f5fe69362932df5d2701'), 'blockNumber': 2878321, 'cumulativeGasUsed': 403716, 'gasUsed': 403716, 'contractAddress': '0xB23dB83429073359b43701bBA91CE3eA8d171f0D', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:46:32 root         INFO     Contract Address: 0xB23dB83429073359b43701bBA91CE3eA8d171f0D
2020-11-20 08:46:32 default      INFO     Price provider deployed Contract Address: 0xB23dB83429073359b43701bBA91CE3eA8d171f0D
2020-11-20 08:46:32 default      INFO     Deploying add pair changer....
2020-11-20 08:46:32 root         INFO     Deploying new contract...
2020-11-20 08:47:24 root         INFO     Deployed contract done!
2020-11-20 08:47:24 root         INFO     0xd39a83922609015cc2138dee51bd88bf2c7e37563589f3499d65e2f0c9c763e3
2020-11-20 08:47:24 root         INFO     AttributeDict({'transactionHash': HexBytes('0xd39a83922609015cc2138dee51bd88bf2c7e37563589f3499d65e2f0c9c763e3'), 'transactionIndex': 1, 'blockHash': HexBytes('0x7095d031060cd572cae99868f72e02fa4a66bdbd8e52584e4cd832ace8b856ab'), 'blockNumber': 2878322, 'cumulativeGasUsed': 627123, 'gasUsed': 567190, 'contractAddress': '0x10ACdDDB0539333b26BC516Dd3E8Bf8B9DBb53c5', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:47:24 root         INFO     Changer Contract Address: 0x10ACdDDB0539333b26BC516Dd3E8Bf8B9DBb53c5
2020-11-20 08:47:24 root         INFO     Executing change....
2020-11-20 08:48:23 root         INFO     0xcda3db6cb8701c0d9810aa6ade7b487222bea9fd457e708eb90464deb014a08a
2020-11-20 08:48:23 root         INFO     AttributeDict({'transactionHash': HexBytes('0xcda3db6cb8701c0d9810aa6ade7b487222bea9fd457e708eb90464deb014a08a'), 'transactionIndex': 1, 'blockHash': HexBytes('0xcab4edfb9b4b71f6b2843aba44c3468f73e8592540d20586d6d5fd0e6916b727'), 'blockNumber': 2878324, 'cumulativeGasUsed': 1170845, 'gasUsed': 873412, 'contractAddress': None, 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': '0x036CaF1d8B11d46F5D819241cFFAC06cDF9Fd230', 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:48:23 root         INFO     Change successfull!
2020-11-20 08:48:23 default      INFO     Changer Contract Address: None

5.DOC/RIF

2020-11-20 08:49:12 default      INFO     Connecting to dexMainnet...
2020-11-20 08:49:13 default      INFO     Connected: True
2020-11-20 08:49:13 default      INFO     Deploying Price provider ...
2020-11-20 08:49:13 root         INFO     Deploying new contract...
2020-11-20 08:49:53 root         INFO     Deployed contract done!
2020-11-20 08:49:53 root         INFO     0xf8551e893c45322436ca6f20e34e0364ea8fa60b768854b35350d6c5bfbbbaac
2020-11-20 08:49:53 root         INFO     AttributeDict({'transactionHash': HexBytes('0xf8551e893c45322436ca6f20e34e0364ea8fa60b768854b35350d6c5bfbbbaac'), 'transactionIndex': 1, 'blockHash': HexBytes('0x36b0bae51cde551551e0231aaefe954897e4c508abe62f87cc9e01dcaa8d3125'), 'blockNumber': 2878327, 'cumulativeGasUsed': 372597, 'gasUsed': 328177, 'contractAddress': '0x7E3b468d58605BB04eD7fD93C3B9451826a40026', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:49:53 root         INFO     Contract Address: 0x7E3b468d58605BB04eD7fD93C3B9451826a40026
2020-11-20 08:49:53 default      INFO     Price provider deployed Contract Address: 0x7E3b468d58605BB04eD7fD93C3B9451826a40026
2020-11-20 08:49:53 default      INFO     Deploying add pair changer....
2020-11-20 08:49:53 root         INFO     Deploying new contract...
2020-11-20 08:50:39 root         INFO     Deployed contract done!
2020-11-20 08:50:39 root         INFO     0x3af957b90e9b9e8947a1711fd4ccd1146e8ccb52eff7e311863e91f98f7cf914
2020-11-20 08:50:39 root         INFO     AttributeDict({'transactionHash': HexBytes('0x3af957b90e9b9e8947a1711fd4ccd1146e8ccb52eff7e311863e91f98f7cf914'), 'transactionIndex': 1, 'blockHash': HexBytes('0x7f6fffbf07e6f39184b5ae25ca265d3cd149472bde05ffc9a76dcba7a4c64e47'), 'blockNumber': 2878329, 'cumulativeGasUsed': 834809, 'gasUsed': 567062, 'contractAddress': '0x9C79873A58DEe23c572F669466229a1a29a48b1f', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:50:39 root         INFO     Changer Contract Address: 0x9C79873A58DEe23c572F669466229a1a29a48b1f
2020-11-20 08:50:39 root         INFO     Executing change....
2020-11-20 08:52:04 root         INFO     0x96e6efab9cef7b873976594f01f5c174bf058d713aace4a16b47b53a0f47ad70
2020-11-20 08:52:04 root         INFO     AttributeDict({'transactionHash': HexBytes('0x96e6efab9cef7b873976594f01f5c174bf058d713aace4a16b47b53a0f47ad70'), 'transactionIndex': 1, 'blockHash': HexBytes('0x6fcc83a6106842146e7d97922f1f0cac18e19b448cb17f1bc158d76eed80834b'), 'blockNumber': 2878331, 'cumulativeGasUsed': 941073, 'gasUsed': 871793, 'contractAddress': None, 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': '0x036CaF1d8B11d46F5D819241cFFAC06cDF9Fd230', 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:52:04 root         INFO     Change successfull!
2020-11-20 08:52:04 default      INFO     Changer Contract Address: None

6. RDOC/RIFP

2020-11-20 08:54:29 default      INFO     Connecting to dexMainnet...
2020-11-20 08:54:30 default      INFO     Connected: True
2020-11-20 08:54:30 default      INFO     Deploying Price provider ...
2020-11-20 08:54:30 root         INFO     Deploying new contract...
2020-11-20 08:54:46 root         INFO     Deployed contract done!
2020-11-20 08:54:46 root         INFO     0x0480b13caa192e50539c0340bc8e2965faa82b342b2bbee7b3f8340a175093e4
2020-11-20 08:54:46 root         INFO     AttributeDict({'transactionHash': HexBytes('0x0480b13caa192e50539c0340bc8e2965faa82b342b2bbee7b3f8340a175093e4'), 'transactionIndex': 1, 'blockHash': HexBytes('0xe295ce9f21d45c493493234dfe2eafa6d4accb1c709bcfca1a1bbdfc77bcd2c3'), 'blockNumber': 2878339, 'cumulativeGasUsed': 459865, 'gasUsed': 403716, 'contractAddress': '0x70b7149657B6a4823986b299E5BC6409e4dfC9E7', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:54:46 root         INFO     Contract Address: 0x70b7149657B6a4823986b299E5BC6409e4dfC9E7
2020-11-20 08:54:46 default      INFO     Price provider deployed Contract Address: 0x70b7149657B6a4823986b299E5BC6409e4dfC9E7
2020-11-20 08:54:46 default      INFO     Deploying add pair changer....
2020-11-20 08:54:46 root         INFO     Deploying new contract...
2020-11-20 08:55:46 root         INFO     Deployed contract done!
2020-11-20 08:55:46 root         INFO     0x8dd7d9f07386e1258028ea5ed4f5d8dca7b68d705ffe74cb1e1fabe31fed29d4
2020-11-20 08:55:46 root         INFO     AttributeDict({'transactionHash': HexBytes('0x8dd7d9f07386e1258028ea5ed4f5d8dca7b68d705ffe74cb1e1fabe31fed29d4'), 'transactionIndex': 1, 'blockHash': HexBytes('0xd83482b317f68034a577738b210de9aeb2d80bd220b048b4ebe09b7ffd1cb9dc'), 'blockNumber': 2878341, 'cumulativeGasUsed': 611610, 'gasUsed': 567190, 'contractAddress': '0xE339dC87102d00d352874631287e09b15124DB54', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:55:46 root         INFO     Changer Contract Address: 0xE339dC87102d00d352874631287e09b15124DB54
2020-11-20 08:55:46 root         INFO     Executing change....
2020-11-20 08:56:15 root         INFO     0x4c6ebfd4ad025fd091fef08abf540563e76d33eeab135210cca7e17903ff5ee2
2020-11-20 08:56:15 root         INFO     AttributeDict({'transactionHash': HexBytes('0x4c6ebfd4ad025fd091fef08abf540563e76d33eeab135210cca7e17903ff5ee2'), 'transactionIndex': 0, 'blockHash': HexBytes('0x59675e03f7560ad4edb8ca5a750e2f62c4f240a86bf31445810444a5d8fd1bcf'), 'blockNumber': 2878343, 'cumulativeGasUsed': 873348, 'gasUsed': 873348, 'contractAddress': None, 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': '0x036CaF1d8B11d46F5D819241cFFAC06cDF9Fd230', 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:56:15 root         INFO     Change successfull!
2020-11-20 08:56:15 default      INFO     Changer Contract Address: None

7. RIF/RIFP

2020-11-20 08:57:25 default      INFO     Connecting to dexMainnet...
2020-11-20 08:57:26 default      INFO     Connected: True
2020-11-20 08:57:26 default      INFO     Deploying Price provider ...
2020-11-20 08:57:26 root         INFO     Deploying new contract...
2020-11-20 08:58:47 root         INFO     Deployed contract done!
2020-11-20 08:58:47 root         INFO     0xbebb90c198acd0337b4ee552e530f58d97d42193a8f70d4f058cdcba105a6351
2020-11-20 08:58:47 root         INFO     AttributeDict({'transactionHash': HexBytes('0xbebb90c198acd0337b4ee552e530f58d97d42193a8f70d4f058cdcba105a6351'), 'transactionIndex': 1, 'blockHash': HexBytes('0x172605e85c7f5fe3df3cd1fd585de8ec9f587a630245704377f3cd87cbeb6dbc'), 'blockNumber': 2878346, 'cumulativeGasUsed': 459152, 'gasUsed': 403716, 'contractAddress': '0x2B88Faac0054236de9cC0CB54F1b85619a348e10', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:58:47 root         INFO     Contract Address: 0x2B88Faac0054236de9cC0CB54F1b85619a348e10
2020-11-20 08:58:47 default      INFO     Price provider deployed Contract Address: 0x2B88Faac0054236de9cC0CB54F1b85619a348e10
2020-11-20 08:58:47 default      INFO     Deploying add pair changer....
2020-11-20 08:58:47 root         INFO     Deploying new contract...
2020-11-20 08:59:21 root         INFO     Deployed contract done!
2020-11-20 08:59:21 root         INFO     0x26e31424c6dccea00d7e731a6df2dac73328877ee06196b2b173f6b218ec1ce8
2020-11-20 08:59:21 root         INFO     AttributeDict({'transactionHash': HexBytes('0x26e31424c6dccea00d7e731a6df2dac73328877ee06196b2b173f6b218ec1ce8'), 'transactionIndex': 1, 'blockHash': HexBytes('0xe87c177803ecda5b15eea3d6f4921d52c9107d4503960a44483d0dfefe160955'), 'blockNumber': 2878348, 'cumulativeGasUsed': 628202, 'gasUsed': 567126, 'contractAddress': '0x95E8224a42239F47AedA750FC3CD81989f64ca11', 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 08:59:21 root         INFO     Changer Contract Address: 0x95E8224a42239F47AedA750FC3CD81989f64ca11
2020-11-20 08:59:21 root         INFO     Executing change....
2020-11-20 09:00:09 root         INFO     0x93beadd69f4cc70ecf953dbda11548cb1a790d129ca722d8ddaa369fa5dd4728
2020-11-20 09:00:09 root         INFO     AttributeDict({'transactionHash': HexBytes('0x93beadd69f4cc70ecf953dbda11548cb1a790d129ca722d8ddaa369fa5dd4728'), 'transactionIndex': 1, 'blockHash': HexBytes('0x5bd172f68241af6cd3d4c058c68ebf33a28aae0a0d3e233e5d59fdf93cf4d000'), 'blockNumber': 2878349, 'cumulativeGasUsed': 917832, 'gasUsed': 873412, 'contractAddress': None, 'logs': [], 'from': '0xB1ef062C364750DeECdCaCBf7190ed591B7a0Bfe', 'to': '0x036CaF1d8B11d46F5D819241cFFAC06cDF9Fd230', 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-11-20 09:00:09 root         INFO     Change successfull!
2020-11-20 09:00:09 default      INFO     Changer Contract Address: None


"""