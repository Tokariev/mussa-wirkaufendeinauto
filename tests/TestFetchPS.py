import unittest
from EnginePower import EnginePower
from dao import get_connection

class TestModelDetail(unittest.TestCase):
    def setUp(self):
        self.enginePower = EnginePower()
        self.connection = get_connection()

    def test_fetch_models_details(self):
        BMW_3_SERIES_2003_LIMOUSINE_BENZIN_316i = 1351

        exp = [
            (1702, 85, 1351) # 85 kW
            ]

        act = self.enginePower.fetch_engine_powers(self.connection, BMW_3_SERIES_2003_LIMOUSINE_BENZIN_316i)
        self.assertEqual(exp, act)
