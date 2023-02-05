import unittest
import os
from FuelType import FuelType
from dao import get_connection



class TstFuelType(unittest.TestCase):

    def setUp(self):
        self.cut = FuelType()
        self.connection = get_connection()

    def test_fetch_fuel_types(self):
        BMW_3_SERIES_2010_KOMBI = 185
        act = self.cut.fetch_fuel_types(self.connection, BMW_3_SERIES_2010_KOMBI)
        exp = [
            (335, 185, 1039),
            (336, 185, 1040),
        ]
        self.assertEqual(exp, act)
