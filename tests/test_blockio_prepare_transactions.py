from block_io import BlockIo

import os
import unittest
import time

import json

class TestBlockIoPrepareTransactions(unittest.TestCase):

    def setUp(self):

        self.blockio = BlockIo("", "d1650160bd8d2bb32bebd139d0063eb6063ffa2f9e4501ad", 2)
        self.dtrust_keys = [
            "b515fd806a662e061b488e78e5d0c2ff46df80083a79818e166300666385c0a2",
            "1584b821c62ecdc554e185222591720d6fe651ed1b820d83f92cdc45c5e21f",
            "2f9090b8aa4ddb32c3b0b8371db1b50e19084c720c30db1d6bb9fcd3a0f78e61",
            "6c1cefdfd9187b36b36c3698c1362642083dcc1941dc76d751481d3aa29ca65"
        ]

        self.sweep_key = BlockIo.Key.from_wif("cTj8Ydq9LhZgttMpxb7YjYSqsZ2ZfmyzVprQgjEzAzQ28frQi4ML").privkey_hex().decode("utf-8");
        self.maxDiff = None

    def load_json_file(self, path):
        json_file = open(os.path.join(os.path.dirname(__file__), path))
        data = json.load(json_file)
        json_file.close()

        return data

    def test_summarize_prepared_transaction(self):
        # tests response of summarize_prepared_transaction

        prepare_transaction_response = self.load_json_file("data/json/prepare_transaction_response_with_blockio_fee_and_expected_unsigned_txid.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_with_blockio_fee_and_expected_unsigned_txid.json")
        summarize_prepared_transaction_response = self.load_json_file("data/json/summarize_prepared_transaction_response_with_blockio_fee_and_expected_unsigned_txid.json")

        summary = self.blockio.summarize_prepared_transaction(prepare_transaction_response)

        self.assertDictEqual(summarize_prepared_transaction_response, summary)
        
        response = self.blockio.create_and_sign_transaction(prepare_transaction_response)

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_expected_unsigned_txid(self):
        # tests success and failure for expected_unsigned_txid

        prepare_transaction_response = self.load_json_file("data/json/prepare_transaction_response_with_blockio_fee_and_expected_unsigned_txid.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_with_blockio_fee_and_expected_unsigned_txid.json")

        # success
        response = self.blockio.create_and_sign_transaction(prepare_transaction_response)
        self.assertDictEqual(create_and_sign_transaction_response, response)

        # failure
        prepare_transaction_response['data']['expected_unsigned_txid'] += 'x'
        try:
            response = self.blockio.create_and_sign_transaction(prepare_transaction_response)
            self.assertEqual(True, False) # shouldn't happen
        except Exception as e:
            self.assertEqual(str(e), "Expected unsigned transaction ID mismatch. Please report this error to support@block.io.")

    def test_prepare_sweep_transaction_p2pkh(self):
        # P2PKH sweep

        prepare_transaction_response = self.load_json_file("data/json/prepare_sweep_transaction_response_p2pkh.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_sweep_p2pkh.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=[self.sweep_key])

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_sweep_transaction_p2wpkh_over_p2sh(self):
        # P2WPKH-over-P2SH sweep

        prepare_transaction_response = self.load_json_file("data/json/prepare_sweep_transaction_response_p2wpkh_over_p2sh.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_sweep_p2wpkh_over_p2sh.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=[self.sweep_key])

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_sweep_transaction_p2wpkh(self):
        # P2WPKH sweep

        prepare_transaction_response = self.load_json_file("data/json/prepare_sweep_transaction_response_p2wpkh.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_sweep_p2wpkh.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=[self.sweep_key])

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_transaction_dtrust_p2sh_3_of_5_keys(self):
        # P2SH dTrust partial
        
        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_p2sh.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_p2sh_3_of_5_keys.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_transaction_dtrust_p2sh_4_of_5_keys(self):
        # P2SH dTrust full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_p2sh.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_p2sh_4_of_5_keys.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[:4])

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_transaction_dtrust_p2wsh_over_p2sh_3_of_5_keys(self):
        # P2WSH-over-P2SH dTrust partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_p2wsh_over_p2sh.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_p2wsh_over_p2sh_3_of_5_keys.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_transaction_dtrust_p2wsh_over_p2sh_4_of_5_keys(self):
        # P2WSH-over-P2SH dTrust full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_p2wsh_over_p2sh.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_p2wsh_over_p2sh_4_of_5_keys.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[:4])

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_transaction_dtrust_witness_v0_3_of_5_keys(self):
        # P2WSH (WITNESS_V0) dTrust partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_witness_v0.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_witness_v0_3_of_5_keys.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_transaction_dtrust_witness_v0_4_of_5_keys(self):
        # P2WSH (WITNESS_V0) dTrust full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_witness_v0.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_witness_v0_4_of_5_keys.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[:4])

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_transaction(self):
        # mixed inputs

        prepare_transaction_response = self.load_json_file("data/json/prepare_transaction_response.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response)

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_transaction_witness_v1_output(self):
        # WITNESS_V1 output

        prepare_transaction_response = self.load_json_file("data/json/prepare_transaction_response_witness_v1_output.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_witness_v1_output.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response)

        self.assertDictEqual(create_and_sign_transaction_response, response)

