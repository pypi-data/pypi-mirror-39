import unittest
from infra import Machine, Cluster

class TestMachine(unittest.TestCase):
    def setUp(self):
        self.m = Machine()
        
    def test_cpu_budget(self):
        self.assertEqual(self.m.cpu_budget, 6000,
                         'incorrect default budget')


class TestCluster(unittest.TestCase):
    def setUp(self):
        self.c = Cluster()
        self.m = Machine()
        
    def test_cpu_budget(self):
        self.assertEqual(self.c.cpu_budget, 3 * self.m.cpu_budget,
                         'incorrect default budget')

    def test_get_used_search_capacity(self):
        self.assertEqual(self.c.get_used_search_capacity(1, 1), 0)
        self.assertEqual(self.c.get_used_search_capacity(1000, 10), 0.556)
        self.assertEqual(self.c.get_used_search_capacity(18000, 1), 1)