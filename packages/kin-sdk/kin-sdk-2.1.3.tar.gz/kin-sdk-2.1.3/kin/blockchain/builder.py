"""Contains the builder class to build transactions"""

from kin_base.builder import Builder as BaseBuilder
from kin_base.keypair import Keypair
from kin_base.memo import NoneMemo
from kin_base.exceptions import StellarAddressInvalidError

from .utils import is_valid_address, is_valid_secret_key


class Builder(BaseBuilder):
    """
    This class overrides :class:`kin_base.builder` to provide additional functionality.
    """

    def __init__(self, network, horizon, fee, secret=None, address=None):
        if secret:
            if not is_valid_secret_key(secret):
                raise ValueError('invalid secret key')
            address = Keypair.from_seed(secret).address().decode()
        elif address:
            if not is_valid_address(address):
                raise StellarAddressInvalidError('invalid address: {}'.format(address))
        else:
            raise Exception('either secret or address must be provided')

        # call baseclass constructor to init base class variables
        super(Builder, self).__init__(secret=secret, address=address, sequence=1, fee=fee)

        # custom overrides

        self.network = network
        self.horizon = horizon

    def clear(self):
        """"Clears the builder so it can be reused."""
        self.ops = []
        self.time_bounds = None
        self.memo = NoneMemo()
        self.tx = None
        self.te = None

    def get_sequence(self):
        """Alternative implementation to expose exceptions"""
        return self.horizon.account(self.address).get('sequence')

    def next(self):
        """
        Alternative implementation that does not create a new builder but clears the current one and increments
        the account sequence number.
        """
        self.clear()
        self.sequence = str(int(self.sequence) + 1)

    def sign(self, secret=None):
        """
        Alternative implementation that does not use the self-managed sequence, but always fetches it from Horizon.
        """
        if not secret:  # only get the new sequence for my own account
            self.sequence = self.get_sequence()
        super(Builder, self).sign(secret)
