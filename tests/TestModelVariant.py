import unittest
import os
from ModelVariants import ModelVariants
from dao import get_connection

class TestModelDetail(unittest.TestCase):
    def setUp(self):
        self.modelVaraints = ModelVariants()
        self.connection = get_connection()

    def test_fetch_models_details(self):
        BMW_3_SERIES_2003_LIMOUSINE_BENZIN = 358

        exp = [
            (1350, '316g', '358'),
            (1351, '316i', '358'),
            (1352, '316ti', '358'),
            (1353, '318i', '358'),
            (1354, '318ti', '358'),
            (1355, '320i', '358'),
            (1356, '325i', '358'),
            (1357, '325ti', '358'),
            (1358, '325xi', '358'),
            (1359, '330i', '358'),
            (1360, '330xi', '358'),
            (1361, 'M3', '358')
            ]

        act = self.modelVaraints.fetch_model_variants(self.connection, BMW_3_SERIES_2003_LIMOUSINE_BENZIN)
        self.assertEqual(exp, act)
