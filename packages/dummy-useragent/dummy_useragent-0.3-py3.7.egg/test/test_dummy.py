import unittest
from dummy_useragent import UserAgent


class Test_Dummy(unittest.TestCase):
    # def test_chrome(self):
    #     u = UserAgent()
    #     u.refresh()

    def test_us(self):
        u = UserAgent()
        c = u.random()
        print(c)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
