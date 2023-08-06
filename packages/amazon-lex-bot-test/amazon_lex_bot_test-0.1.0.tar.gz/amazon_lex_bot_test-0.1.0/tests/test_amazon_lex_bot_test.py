#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `amazon_lex_bot_test` package."""

import unittest

from amazon_lex_bot_test import amazon_lex_bot_test as albt


class TestAmazon_lex_bot_test(unittest.TestCase):
    """Tests for `amazon_lex_bot_test` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_slots(self):
        """Tests slot values."""

        post_conditions = {
            'dialogState': 'ReadyForFulfillment',
            'slots': {
                'CarType': 'economy',
                'DriverAge': '38',
                'PickUpCity': 'new york',
                'PickUpDate': '.*',
                'ReturnDate': '.*'
            }
        }
        response = {
            'dialogState': 'ReadyForFulfillment',
            'intentName': 'BookCar',
            'message': None,
            'messageFormat': None,
            'responseCard': None,
            'sessionAttributes': {},
            'slotToElicit': None,
            'slots': {
                'CarType': 'economy',
                'DriverAge': '38',
                'PickUpCity': 'new york',
                'PickUpDate': '2018-12-14',
                'ReturnDate': '2018-12-15'
            }
        }

        check_result = albt.test_response(postConditions=post_conditions, response=response)
        assert check_result['slots']

    def test_slots(self):
        """Tests slot values."""

        post_conditions = {
            'dialogState': 'ReadyForFulfillment',
            'slots': {
                'CarType': 'economy',
                'DriverAge': '38',
                'PickUpCity': 'new york',
                'PickUpDate': '2018-12-23',
                'ReturnDate': '.*'
            }
        }
        response = {
            'dialogState': 'ReadyForFulfillment',
            'intentName': 'BookCar',
            'message': None,
            'messageFormat': None,
            'responseCard': None,
            'sessionAttributes': {},
            'slotToElicit': None,
            'slots': {
                'CarType': 'economy',
                'DriverAge': '38',
                'PickUpCity': 'new york',
                'PickUpDate': '2018-12-14',
                'ReturnDate': '2018-12-15'
            }
        }

        check_result = albt.test_response(postConditions=post_conditions, response=response)
        assert not check_result['slots']
