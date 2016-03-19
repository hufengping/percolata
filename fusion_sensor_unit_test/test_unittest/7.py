#!/usr/bin/env python
'''HTMLTestRunner'''
import unittest
import HTMLTestRunner


def addnum(a, b):
	return a+b


def delnum(a, b):
	return a-b


class TestFun(unittest.TestCase):

	def setUp(self):
		print 'do before class....'

	def test_Add(self):
		print 'test add................'
		self.assertEqual(2, addnum(1, 1))

	def test_Del(self):
		print 'test del................'
		self.assertEqual(0, delnum(1, 1))

	def tearDown(self):
		print 'do after class....'


if __name__ == "__main__":
	suite1 = unittest.TestSuite()
	suite1.addTest(TestFun('test_Add'))
	suite1.addTest(TestFun('test_Del'))
	fp = file('my_report.html', 'wb')
	runner = HTMLTestRunner.HTMLTestRunner(
											stream=fp,
											title='Percolata Test Report',
											description='Fusion Sensor 2.0 TestCase-0210'
											)
	runner.run(suite1)
