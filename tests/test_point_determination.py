from app.handlers.utils import (determine_points, get_points_from_retailer, get_points_from_total, 
                            get_points_from_items, get_points_from_purchase_date, get_points_from_purchase_time)

import unittest

class TestOverallPointDetermination(unittest.TestCase):

    def test_empty_receipt(self):
        receipt = {}
        points = determine_points(receipt)
        assert 10 == points

    def test_example_receipts(self):
        receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                "shortDescription": "Mountain Dew 12PK",
                "price": "6.49"
                },{
                "shortDescription": "Emils Cheese Pizza",
                "price": "12.25"
                },{
                "shortDescription": "Knorr Creamy Chicken",
                "price": "1.26"
                },{
                "shortDescription": "Doritos Nacho Cheese",
                "price": "3.35"
                },{
                "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                "price": "12.00"
                }
            ],
            "total": "35.35"
        }
        points = determine_points(receipt)
        assert points == 28


        receipt = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                }
            ],
            "total": "9.00"
        }
        points = determine_points(receipt)
        print(points)
        assert points == 109

class TestAlphaNumericPointDetermination(unittest.TestCase):
    
    def test_non_string(self):
        points = get_points_from_retailer(1)
        assert 0 == points

    def test_all_specials(self):
        points = get_points_from_retailer('***')
        assert 0 == points

    def test_all_letters(self):
        points = get_points_from_retailer('please give me this job')
        assert 19 == points

    def test_all_numbers(self):
        points = get_points_from_retailer('12345')
        assert 5 == points

    def test_combination(self):
        points = get_points_from_retailer('test 1234 test')
        assert 12 == points

    def test_passing_none(self):
        points = get_points_from_retailer(None)
        assert 0 == points

class TestTotalPointDetermination(unittest.TestCase):

    def test_non_number(self):
        points = get_points_from_total('string')
        assert points == 0

    def test_total_is_integer_and_quarter_multiple(self):
        points = get_points_from_total('10.00')
        assert points == 75

    def test_total_is_quarter_multiple_not_integer(self):
        points = get_points_from_total('10.25')
        assert points == 25

    def test_total_is_none(self):
        points = get_points_from_total(None)
        assert points == 0

    def test_total_is_neither_integer_or_multiple(self):
        points = get_points_from_total('10.33')
        assert points == 0

class TestItemsPointDetermination(unittest.TestCase):
    
    def test_non_list(self):
        points = get_points_from_items('string')
        assert points == 0

    def test_empty_list(self):
        points = get_points_from_items([])
        assert points == 0

    def test_list_without_correct_keys(self):
        item = {
            'random_key': 'wrong'
        }
        points = get_points_from_items([item])
        assert points == 0

    def test_list_length_points(self):
        item = {
            'random_key': 'wrong'
        }
        points = get_points_from_items([item, item])
        assert points == 5

        points = get_points_from_items([item, item, item])
        assert points == 5

        points = get_points_from_items([item, item, item, item])
        assert points == 10

    def test_price_is_none(self):
        item = {
            'shortDescription': 'something', 
            'no_price': 'wrong'
        }
        points = get_points_from_items([item])
        assert points == 0

    def test_description_is_none(self):
        item = {
            'no_description': 'wrong',
            'price': "100.00"
        }
        points = get_points_from_items([item])
        assert points == 0

    def test_no_points_for_item_valid(self):
        item = {
            'shortDescription': 'test',
            'price': "100.00"
        }
        points = get_points_from_items([item])
        assert points == 0

    def test_valid_point_earners(self):
        item = {
            'shortDescription': 'tes',
            'price': "100.00"
        }
        points = get_points_from_items([item])
        assert points == 20

        item = {
            'shortDescription': ' withspace ',
            'price': "100.00"
        }
        points = get_points_from_items([item])
        assert points == 20

        item = {
            'shortDescription': ' withspace ',
            'price': "300.00"
        }
        points = get_points_from_items([item])
        assert points == 60

        item = {
            'shortDescription': ' withspace ',
            'price': "300.00"
        }
        points = get_points_from_items([item, item])
        assert points == 125

class TestPurchaseDatePointDetermination(unittest.TestCase):

    def test_date_is_list(self):
        points = get_points_from_purchase_date([])
        assert points == 0

    def test_date_is_none(self):
        points = get_points_from_purchase_date(None)
        assert points == 0

    def test_date_is_bad_string(self):
        points = get_points_from_purchase_date('bad')
        assert points == 0

    def test_date_is_even(self):
        date = "2022-01-02"
        points = get_points_from_purchase_date(date)
        assert points == 0

    def test_date_is_odd(self):
        date = "2022-01-03"
        points = get_points_from_purchase_date(date)
        assert points == 6

class TestPurchaseTimePointDetermination(unittest.TestCase):
    def test_time_is_list(self):
        points = get_points_from_purchase_time([])
        assert points == 0

    def test_time_is_none(self):
        points = get_points_from_purchase_time(None)
        assert points == 0

    def test_time_is_bad_string(self):
        points = get_points_from_purchase_time('bad')
        assert points == 0

    def test_time_is_at_two(self):
        time = "14:00"
        points = get_points_from_purchase_time(time)
        assert points == 0

    def test_time_is_at_four(self):
        time = "16:00"
        points = get_points_from_purchase_time(time)
        assert points == 0

    def test_time_is_not_point_earner(self):
        date = "12:00"
        points = get_points_from_purchase_time(date)
        assert points == 0

    def test_time_is_point_earner(self):
        date = "14:30"
        points = get_points_from_purchase_time(date)
        assert points == 10

        date = "15:00"
        points = get_points_from_purchase_time(date)
        assert points == 10

        date = "15:30"
        points = get_points_from_purchase_time(date)
        assert points == 10
            