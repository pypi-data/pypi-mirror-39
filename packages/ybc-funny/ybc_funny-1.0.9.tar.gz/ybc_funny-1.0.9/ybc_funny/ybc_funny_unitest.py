import unittest
from ybc_funny import *


class MyTestCase(unittest.TestCase):
    def test_jizhuanwan(self):
        self.assertIsNotNone(jizhuanwan())

    def test_raokouling(self):
        self.assertIsNotNone(raokouling())

    def test_xiehouyu(self):
        self.assertIsNotNone(xiehouyu())

    def test_miyu(self):
        self.assertIsNotNone(miyu())


if __name__ == '__main__':
    unittest.main()
