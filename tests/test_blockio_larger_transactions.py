from block_io import BlockIo

import os
import unittest
import time

import json

class TestBlockIoLargerTransactions(unittest.TestCase):

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

    def test_prepare_dtrust_transaction_p2sh_3of5_195_inputs(self):
        # dTrust P2WSH-over-P2SH with 195 inputs partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_P2SH_3of5_195inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_P2SH_3of5_195inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_p2sh_4of5_195_inputs(self):
        # dTrust P2WSH-over-P2SH with 195 inputs full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_P2SH_4of5_195inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_P2SH_4of5_195inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:4])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_p2wsh_over_p2sh_3of5_251_inputs(self):
        # dTrust P2WSH-over-P2SH with 251 inputs partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_P2WSH-over-P2SH_3of5_251inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_P2WSH-over-P2SH_3of5_251inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_p2wsh_over_p2sh_3of5_252_inputs(self):
        # dTrust P2WSH-over-P2SH with 252 inputs partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_P2WSH-over-P2SH_3of5_252inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_P2WSH-over-P2SH_3of5_252inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_p2wsh_over_p2sh_3of5_253_inputs(self):
        # dTrust P2WSH-over-P2SH with 253 inputs partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_P2WSH-over-P2SH_3of5_253inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_P2WSH-over-P2SH_3of5_253inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_p2wsh_over_p2sh_4of5_251_inputs(self):
        # dTrust P2WSH-over-P2SH with 251 inputs full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_P2WSH-over-P2SH_4of5_251inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_P2WSH-over-P2SH_4of5_251inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:4])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_p2wsh_over_p2sh_4of5_252_inputs(self):
        # dTrust P2WSH-over-P2SH with 252 inputs full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_P2WSH-over-P2SH_4of5_252inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_P2WSH-over-P2SH_4of5_252inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:4])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_p2wsh_over_p2sh_4of5_253_inputs(self):
        # dTrust P2WSH-over-P2SH with 253 inputs full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_P2WSH-over-P2SH_4of5_253inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_P2WSH-over-P2SH_4of5_253inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:4])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_3of5_251_inputs(self):
        # dTrust WITNESS_V0 with 251 inputs partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_WITNESS_V0_3of5_251inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_WITNESS_V0_3of5_251inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_3of5_252_inputs(self):
        # dTrust WITNESS_V0 with 252 inputs partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_WITNESS_V0_3of5_252inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_WITNESS_V0_3of5_252inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_3of5_253_inputs(self):
        # dTrust WITNESS_V0 with 253 inputs partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_WITNESS_V0_3of5_253inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_WITNESS_V0_3of5_253inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_3of5_251_outputs(self):
        # dTrust WITNESS_V0 with 251 outputs partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_witness_v0_3of5_251outputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_witness_v0_3of5_251outputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_3of5_252_outputs(self):
        # dTrust WITNESS_V0 with 252 outputs partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_witness_v0_3of5_252outputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_witness_v0_3of5_252outputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_3of5_253_outputs(self):
        # dTrust WITNESS_V0 with 253 outputs partial

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_witness_v0_3of5_253outputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_witness_v0_3of5_253outputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys[0:3])

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_4of5_251_inputs(self):
        # dTrust WITNESS_V0 with 251 inputs full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_WITNESS_V0_4of5_251inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_WITNESS_V0_4of5_251inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys)

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_4of5_252_inputs(self):
        # dTrust WITNESS_V0 with 252 inputs full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_WITNESS_V0_4of5_252inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_WITNESS_V0_4of5_252inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys)

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_4of5_253_inputs(self):
        # dTrust WITNESS_V0 with 253 inputs full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_WITNESS_V0_4of5_253inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_WITNESS_V0_4of5_253inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys)

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_4of5_251_outputs(self):
        # dTrust WITNESS_V0 with 251 outputs full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_witness_v0_4of5_251outputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_witness_v0_4of5_251outputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys)

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_4of5_252_outputs(self):
        # dTrust WITNESS_V0 with 252 outputs full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_witness_v0_4of5_252outputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_witness_v0_4of5_252outputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys)

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_dtrust_transaction_witness_v0_4of5_253_outputs(self):
        # dTrust WITNESS_V0 with 253 outputs full

        prepare_transaction_response = self.load_json_file("data/json/prepare_dtrust_transaction_response_witness_v0_4of5_253outputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_dtrust_witness_v0_4of5_253outputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response, keys=self.dtrust_keys)

        self.assertDictEqual(create_and_sign_transaction_response, response)
        
    def test_prepare_transaction_p2sh_1of2_251_inputs(self):
        # P2SH transaction with 251 inputs

        prepare_transaction_response = self.load_json_file("data/json/prepare_transaction_response_P2WSH-over-P2SH_1of2_251inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_P2WSH-over-P2SH_1of2_251inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response)

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_transaction_p2sh_1of2_252_inputs(self):
        # P2SH transaction with 252 inputs

        prepare_transaction_response = self.load_json_file("data/json/prepare_transaction_response_P2WSH-over-P2SH_1of2_252inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_P2WSH-over-P2SH_1of2_252inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response)

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_transaction_p2sh_1of2_253_inputs(self):
        # P2SH transaction with 253 inputs

        prepare_transaction_response = self.load_json_file("data/json/prepare_transaction_response_P2WSH-over-P2SH_1of2_253inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_P2WSH-over-P2SH_1of2_253inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response)

        self.assertDictEqual(create_and_sign_transaction_response, response)

    def test_prepare_transaction_p2sh_1of2_762_inputs(self):
        # P2SH transaction with 762 inputs

        prepare_transaction_response = self.load_json_file("data/json/prepare_transaction_response_P2WSH-over-P2SH_1of2_762inputs.json")
        create_and_sign_transaction_response = self.load_json_file("data/json/create_and_sign_transaction_response_P2WSH-over-P2SH_1of2_762inputs.json")

        response = self.blockio.create_and_sign_transaction(prepare_transaction_response)

        self.assertDictEqual(create_and_sign_transaction_response, response)
