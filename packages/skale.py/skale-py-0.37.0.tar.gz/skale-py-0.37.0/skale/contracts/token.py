from skale.contracts import BaseContract


class Token(BaseContract):

    def get_balance(self, address):
        return self.contract.functions.balanceOf(address).call()
