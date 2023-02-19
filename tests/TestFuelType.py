import unittest
import os
from FuelType import FuelType
from dao import get_connection



class TstFuelType(unittest.TestCase):

    def setUp(self):
        self.cut = FuelType()
        self.connection = get_connection()

    def test_fetch_fuel_types(self):
        BMW_3_SERIES_2003_LIMOUSINE = 216
        act = self.cut.fetch_fuel_types(self.connection, BMW_3_SERIES_2003_LIMOUSINE)
        exp = [
            (358, 1039, 216), # Benzin
            (359, 1040, 216)
        ]
        self.assertEqual(exp, act)
