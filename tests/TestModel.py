import unittest
import os
from Model import Model
from dao import get_connection

class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = Model()
        self.connection = get_connection()

    def test_fetch_models_by_manufacturer(self):
        manufacturer = '130' #BMW

        exp = [
                (8, '1er', '130'),
                (9, '2er', '130'),
                (10, '3er', '130'),
                (11, '4er', '130'),
                (12, '5er', '130'),
                (13, '6er', '130'),
                (14, '7er', '130'),
                (15, '8er', '130'),
                (16, 'i3', '130'),
                (17, 'i4', '130'),
                (18, 'i8', '130'),
                (19, 'iX', '130'),
                (20, 'iX3', '130'),
                (21, 'X1', '130'),
                (22, 'X2', '130'),
                (23, 'X3', '130'),
                (24, 'X4', '130'),
                (25, 'X5', '130'),
                (26, 'X6', '130'),
                (27, 'X7', '130'),
                (28, 'Z1', '130'),
                (29, 'Z3', '130'),
                (30, 'Z4', '130'),
                (31, 'Z8', '130')
            ]

        act = self.model.fetch_models_by_brand(self.connection, manufacturer)
        self.assertEqual(exp, act)
