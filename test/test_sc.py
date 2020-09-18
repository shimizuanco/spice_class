import unittest
from sc import Sc
import logging
from spiceypy.utils.exceptions import SpiceyError, SpiceNOSUCHFILE


class TestSc(unittest.TestCase):
    def test_invoke_ok01_cascading(self):
        logging.basicConfig(level=logging.INFO)
        with Sc('/home/hugh/spice/sel_v02.tm') as sc:
            actual = sc.invoke()
            with Sc('/home/hugh/spice/lro_v02.tm') as sc2:
                actual = sc2.invoke()
                with Sc('/home/hugh/spice/lro_v02.tm') as sc3:
                    actual = sc3.invoke()
        self.assertTrue(actual)

    def test_invoke_ok02_parallel(self):
        logging.basicConfig(level=logging.INFO)
        with Sc('/home/hugh/spice/sel_v02.tm') as sc, Sc('/home/hugh/spice/lro_v02.tm') as sc2:
            actual1 = sc.invoke()
            actual2 = sc2.invoke()
        self.assertTrue(actual1 and actual2)

    def test_invoke_ng01_nosuchfile(self):
        logging.basicConfig(level=logging.INFO)
        with self.assertRaises(SpiceNOSUCHFILE):
            with Sc('/home/hugh/spice/sel_v02.tm2') as sc:
                sc.invoke()


if __name__ == '__main__':
    unittest.main()
