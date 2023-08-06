import bimgn
import unittest


class Test_001:
    def __init__(self):
        self.task = bimgn.BioTask()

    def test_simple_int(self):
        assert True is 1

    def test_configuration(self):
        assert self.task.max_ram_memory == '5g'


if __name__ == '__main__':
    unittest.main()
