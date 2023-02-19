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
        BUILT_YEAR_2003_ID = '134'

        exp = [
            (213, 1007, 134),
            (214, 1008, 134),
            (215, 1023, 134),
            (216, 1025, 134)] # Limousine

        act = self.body_type.fetch_body_types(self.connection, BUILT_YEAR_2003_ID)
        self.assertEqual(exp, act)