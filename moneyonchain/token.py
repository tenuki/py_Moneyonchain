"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import json
import os
import datetime
import logging

from moneyonchain.contract import Contract


class ERC20Token(Contract):

    log = logging.getLogger()

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def name(self):
        return self.sc.functions.name().call()


class DoCToken(ERC20Token):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/DocToken.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/DocToken.bin'))

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['DoCToken']

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # finally load the contract
        self.load_contract()

    def name(self):
        return self.sc.functions.name().call()
