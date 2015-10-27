#!/usr/bin/env python
'''setUpClass,tearDownClass'''
import unittest


def addnum(a, b):
	return a+b


def delnum(a, b):
	return a-b


class TestFun(unittest.TestCase):

	@classmethod #run befor all testcases
	def setUpClass(cls):
		pass

	def setUp(self):
		print 'do before class....'

	@unittest.skip("skip")
	def test_Add(self):
		print 'test add................'
		self.assertEqual(2, addnum(1, 1))

	#@unittest.skipif(os.path.isfile("~/1.json")!=true,"can't find config")
	def test_Del(self):
		print 'test del................'
		self.assertEqual(0, delnum(1, 1))

	def tearDown(self):
		print 'do after class....'

	@classmethod #run after all testcases
	def tearDownClass(cls):
		pass


if __name__ == "__main__":
	suite1 = unittest.TestLoader().loadTestsFromTestCase(TestFun)
	suite2 = unittest.TestLoader().loadTestsFromTestCase(TestFun)
	allsuits = unittest.TestSuite([suite1, suite2])
	unittest.TextTestRunner(verbosity=2).run(allsuits)
