""" Test class for BodyType.py """

import unittest
import os
from BodyType import BodyType
from dao import get_connection

class TestBodyType(unittest.TestCase):

    def setUp(self):
        self.body_type = BodyType()
        self.connection = get_connection()

    def test_fetch_body_types(self):
        BMW_3er = '10'
        BUILT_YEAR_2010 = '2010'

        exp = [
            (183, '10', '2010', '1008'),
            (184, '10', '2010', '1009'),
            (185, '10', '2010', '1023'),
            (186, '10', '2010', '1025')]

        act = self.body_type.fetch_body_types(self.connection, BMW_3er, BUILT_YEAR_2010)
        self.assertEqual(exp, act)