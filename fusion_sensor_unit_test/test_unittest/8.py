#!/usr/bin/env python
'''add something to HTMLTestRunner'''
import unittest,time
import HTMLTestRunner


def addnum(a, b):
	return a+b


def delnum(a, b):
	return a-b


class TestFun(unittest.TestCase):

	def setUp(self):
		print 'do before class....'

	def test_Add(self):
		'''This will be the description of the TestCase--test_Add.'''
		print 'test add................'
		self.assertEqual(1, addnum(1, 1),"stupid! 1+1=2")

	def test_Del(self):
		'''This will be the description of the TestCase--test_Del.'''
		print 'test del................'

		try:
			self.assertEqual(0, delnum(1, 1))
		except AssertionError,e:
			print e
			now = time.strftime("%Y-%m-%d_%H_%M_%S")
			print 'delnum error'
			self.driver.get_screenshot_as_file("log\\"+now+'delnum.png')


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
