
from block_io.bitcoinutils_patches import *

import unittest

class TestBitcoinUtilsAmounts(unittest.TestCase):
    
    def setUp(self):
        None

    def test_amount_precision(self):

        self.assertEqual(bitcoinutils.utils.to_satoshis("0.12345678"), 12345678)
        self.assertEqual(bitcoinutils.utils.to_satoshis("1.12345678"), 112345678)
        self.assertEqual(bitcoinutils.utils.to_satoshis("10000000"), 1000000000000000)
        self.assertEqual(bitcoinutils.utils.to_satoshis("10000000.12345678"), 1000000012345678)
        
