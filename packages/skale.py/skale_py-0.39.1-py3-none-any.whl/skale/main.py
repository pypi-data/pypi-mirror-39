import logging

from web3 import Web3, WebsocketProvider

from skale.utils.helper import generate_custom_config, load_skale_env_config, generate_ws_addr, get_abi
import skale.contracts as contracts
from skale.blockchain_env import BlockchainEnv

logger = logging.getLogger(__name__)


class Skale:
    def __init__(self, skale_env, ip=None, ws_port=None, abi_filepath=None):
        env_config = generate_custom_config(ip, ws_port) if (
                    skale_env == BlockchainEnv.CUSTOM) else load_skale_env_config(skale_env)
        logger.info(f'Init skale-py: skale_env: {skale_env}, env_config: {env_config}')
        ws_addr = generate_ws_addr(env_config['ip'], env_config['ws_port'])
        self.web3 = Web3(WebsocketProvider(ws_addr))
        self.abi = get_abi(skale_env, abi_filepath)
        self.__contracts = {}
        self.__init_contracts()
        self.nonces = {}

    def __init_contracts(self):
        self.add_lib_contract('manager', contracts.Manager)
        self.add_lib_contract('token', contracts.Token)
        self.add_lib_contract('schains', contracts.SChains)

        self.add_lib_contract('nodes', contracts.Nodes)
        # self.add_lib_contract('groups', contracts.Groups)
        self.add_lib_contract('validators', contracts.Validators)

    def add_lib_contract(self, name, contract_class):
        address = self.abi[f'skale_{name}_address']
        abi = self.abi[f'skale_{name}_abi']

        self.add_contract(name, contract_class(self, name, address, abi))

    def add_contract(self, name, skale_contract):
        logger.debug(f'Init contract: {name}')
        self.__contracts[name] = skale_contract

    def get_contract_by_name(self, name):
        return self.__contracts[name]

    def __getattr__(self, name):
        if name not in self.__contracts:
            raise AttributeError(name)
        return self.get_contract_by_name(name)
