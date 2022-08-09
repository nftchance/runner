from django.test import TestCase

from utils.tests.user import create_user

from org.permission_constants import org_permissions
from org.utils import load_permissions

from coin.models import Coin

class CoinTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.secondary_user = create_user(username="secondaryuser@example.com")        
        
        load_permissions("org", org_permissions)

        self.coin = Coin.objects.create(name="RUNNER", symbol="RUN")

    def test_can_mint_coin(self):
        self.assertEqual(self.user.balance, 0)
        self.coin.mint(self.user, 1)
        self.assertEqual(self.user.balance, 1)

    def test_can_burn_coin(self):
        self.coin.mint(self.user, 1)
        self.assertEqual(self.user.balance, 1)
        self.coin.burn(self.user, 1)
        self.assertEqual(self.user.balance, 0)

    def test_can_transfer_coin(self):
        self.coin.mint(self.user, 1)
        self.assertEqual(self.user.balance, 1)
        self.coin.transfer(self.user, self.secondary_user, 1)
        self.assertEqual(self.user.balance, 0)
        self.assertEqual(self.secondary_user.balance, 1)

    def test_cannot_transfer_coin_to_self(self):
        self.coin.mint(self.user, 100)
        self.assertEqual(self.user.balance, 100)
        
        # assert raise of value error
        with self.assertRaises(ValueError) as e:
            self.coin.transfer(self.user, self.user, 1)
            self.assertEqual(str(e.exception), "Cannot transfer coin to self.")

        self.assertEqual(self.user.balance, 100)

    def test_cannot_transfer_coin_exceeding_balance(self):
        self.coin.mint(self.user, 1)
        self.assertEqual(self.user.balance, 1)
        
        # assert raise of value error
        with self.assertRaises(ValueError) as e:
            self.coin.transfer(self.user, self.secondary_user, 2)
            self.assertEqual(str(e.exception), "Exceeds balance.")

        self.assertEqual(self.user.balance, 1)
        self.assertEqual(self.secondary_user.balance, 0)