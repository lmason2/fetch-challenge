from handlers.utils import validate_receipt

import unittest

class TestReceiptValidation(unittest.TestCase):

    def test_valid_receipt(self):
        receipt = {
            "retailer": "target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }

        assert validate_receipt(receipt) is True

    def test_invalid_name(self):
        receipt = {
            "retailer": ";",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }

        assert validate_receipt(receipt) is False

    def test_invalid_date(self):
        receipt = {
            "retailer": "target",
            "purchaseDate": "2022-01-50",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }

        assert validate_receipt(receipt) is False

        receipt.update({
            'purchaseDate': '2022-13-01'
        })
        assert validate_receipt(receipt) is False

        receipt.update({
            'purchaseDate': '24-12-01'
        })
        assert validate_receipt(receipt) is False

        receipt.update({
            'purchaseDate': '2022-12-01'
        })
        assert validate_receipt(receipt) is True

    def test_invalid_time(self):
        receipt = {
            "retailer": "target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "25:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }

        assert validate_receipt(receipt) is False

        receipt.update({
            'purchaseTime': '12:60'
        })
        assert validate_receipt(receipt) is False

        receipt.update({
            'purchaseTime': '12;10'
        })
        assert validate_receipt(receipt) is False

        receipt.update({
            'purchaseTime': '1210'
        })
        assert validate_receipt(receipt) is False

        receipt.update({
            'purchaseTime': '12:10'
        })
        assert validate_receipt(receipt) is True

    def test_invalid_total(self):
        receipt = {
            "retailer": "target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "12:13",
            "total": "125",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }

        assert validate_receipt(receipt) is False

        receipt.update({
            'total': '125.0'
        })
        assert validate_receipt(receipt) is False

        receipt.update({
            'total': '125.000'
        })
        assert validate_receipt(receipt) is False

        receipt.update({
            'total': '.25'
        })
        assert validate_receipt(receipt) is False

        receipt.update({
            'total': '125.00'
        })
        assert validate_receipt(receipt) is True

    def test_invalid_items(self):
        receipt = {
            "retailer": "target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "12:13",
            "total": "125.00",
            "items": [
                {"shortDescription": ";", "price": "1.25"}
            ]
        }

        assert validate_receipt(receipt) is False

        receipt['items'][0].update({
            'shortDescription': 'Pepsi - 12-oz',
            'price': '1'
        })
        assert validate_receipt(receipt) is False

        receipt['items'][0].update({
            'price': '1.000'
        })
        assert validate_receipt(receipt) is False

        receipt['items'][0].update({
            'price': '1.0'
        })
        assert validate_receipt(receipt) is False

        receipt['items'][0].update({
            'price': '.25'
        })
        assert validate_receipt(receipt) is False

        receipt['items'][0].update({
            'price': '1.25'
        })
        assert validate_receipt(receipt) is True