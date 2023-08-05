import logging

from django.test import TestCase
from django_eth.tests.factories import get_eth_address_with_key

from ..ethereum_service import EthereumServiceProvider
from .factories import deploy_example_erc20, deploy_safe, generate_safe
from .test_safe_service import TestCaseWithSafeContractMixin

logger = logging.getLogger(__name__)


class TestSafeCreationTx(TestCase, TestCaseWithSafeContractMixin):
    @classmethod
    def setUpTestData(cls):
        cls.ethereum_service = EthereumServiceProvider()
        cls.w3 = cls.ethereum_service.w3

    def test_erc20_balance(self):
        amount = 1000
        account, _ = get_eth_address_with_key()
        erc20_contract = deploy_example_erc20(self.w3, amount, account, deployer=self.w3.eth.accounts[0])
        token_balance = self.ethereum_service.get_erc20_balance(account, erc20_contract.address)
        self.assertTrue(token_balance, amount)

        another_account, _ = get_eth_address_with_key()
        token_balance = self.ethereum_service.get_erc20_balance(another_account, erc20_contract.address)
        self.assertEqual(token_balance, 0)
