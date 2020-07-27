#!/usr/bin/env python
import unittest
from app import utils


class Generate_sign(unittest.TestCase):
    def test_sign_hashing_pay_case_1(self):
        data = {
            'amount': 111.22,
            'currency': '643',
            'shop_id': 5,
            'description': 'item_description value',
            'shop_order_id': '333',
        }
        required_keys = ['amount', 'currency', 'shop_id', 'shop_order_id']
        secret_key = 'SecretKey01'
        sign_source_string = utils.dict_values_concatenator(data, required_keys) + secret_key
        generated_sign = utils.generate_sign(sign_source_string)
        self.assertEqual(
            generated_sign,
            '9bd879c8dc4d5f65666549f38637062f36b1dc82f8894e093f7d0224c6cfcf4c')

    def test_sign_hashing_pay_case_2(self):
        data = {
            'amount': 0.22,
            'currency': '643',
            'shop_id': 5,
            'description': 'item_description value',
            'shop_order_id': '111',
        }
        secret_key = 'SecretKey01'
        required_keys = ['amount', 'currency', 'shop_id', 'shop_order_id']
        sign_source_string = utils.dict_values_concatenator(data, required_keys) + secret_key
        generated_sign = utils.generate_sign(sign_source_string)
        self.assertEqual(
            generated_sign,
            '4920340db7ae5b58e09bdb288f8542feddceb94f90cb495caec899074250f454')

    def test_sign_hashing_invoice_case_1(self):
        data = {
            'currency': '643',
            'sign':'9cf003e3ad9da90ff00b06349b677261d5539f7e0540fb976c45537a141222c1',
            'payway': 'payeer_rub',
            'amount': '12.34',
            'shop_id': '5',
            'shop_order_id': '4126',
            'description': 'Test invoice',
        }
        secret_key = 'SecretKey01'
        required_keys = ['amount', 'currency', 'payway', 'shop_id',
        'shop_order_id']
        sign_source_string = utils.dict_values_concatenator(data, required_keys) + secret_key
        generated_sign = utils.generate_sign(sign_source_string)
        self.assertEqual(
            generated_sign,
            '9cf003e3ad9da90ff00b06349b677261d5539f7e0540fb976c45537a141222c1')

    def test_sign_hashing_invoice_case_2(self):
        data = {
            'currency': '643',
            'sign':'9cf003e3ad9da90ff00b06349b677261d5539f7e0540fb976c45537a141222c1',
            'payway': 'payeer_rub',
            'amount': '0.34',
            'shop_id': '5',
            'shop_order_id': 9999,
            'description': 'Test invoice',
        }
        secret_key = 'SecretKey01'
        required_keys = ['amount', 'currency', 'payway', 'shop_id',
        'shop_order_id']
        sign_source_string = utils.dict_values_concatenator(data, required_keys) + secret_key
        generated_sign = utils.generate_sign(sign_source_string)
        self.assertEqual(
            generated_sign,
            '3d695b82bbd596442691467df23836b0186fd528e30e19b18f6e632026fe2171')

    def test_sign_hashing_bill_case_1(self):
        data = {
            'payer_currency': 999,
            'shop_amount': '33.44',
            'shop_currency': 643,
            'shop_id': 5,
            'shop_order_id': 'b83367ae-f295-4e8b-85ef-b57b3ded394a',
        }
        secret_key = 'SecretKey01'
        required_keys = ['payer_currency', 'shop_amount', 'shop_currency', 'shop_id', 'shop_order_id']
        sign_source_string = utils.dict_values_concatenator(data, required_keys) + secret_key
        generated_sign = utils.generate_sign(sign_source_string)
        self.assertEqual(
            generated_sign,
            '82adcc2b6511307ee4607cbadc7f23dad8eabb65e4e5c6cada0cc81ee70cc2f6')


if __name__ == '__main__':
    unittest.main(verbosity=2)
