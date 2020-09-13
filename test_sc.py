import unittest
from sc import Sc
import logging


class TestSc(unittest.TestCase):
    def test_invoke(self):
        logging.basicConfig(level=logging.DEBUG)
        with Sc('/home/hugh/spice/sel_v02.tm') as sc:
            sc.invoke()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
