import unittest
import os
from Model import Model
from dao import get_connection

class TestModelDetail(unittest.TestCase):
    def setUp(self):
        self.model = Model()
        self.connection = get_connection()

    def test_fetch_models_details(self):
        BMW_3_SERIES_2010_KOMBI_BENZIN = 335