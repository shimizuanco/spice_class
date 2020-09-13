import unittest
from sc_sln import ScSln


class TestScSln(unittest.TestCase):
    def test_invoke(self):
        with ScSln('/home/hugh/spice/sel_v02.tm') as ss:
            print(type(ss))
            actual = ss.invoke()
            expected = True
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
