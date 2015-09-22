#!/usr/bin/env python
'''
Created on 30 Aug 2015

@author: fengpinghu
'''
#coding=utf-8
import unittest

@unittest.skip("skip")
def addNum(a,b):
	return a+b

def delNum(a,b):
	return a-b

class TestFun(unittest.TestCase):
	def setUp(self):
		print 'do before class....'
	def tearDown(self):
		print 'do after class....'

	def test_Add(self):
		print 'test add................'
		self.assertEqual(1,addNum(1,1))

	def test_Del(self):
		print 'test del................'
		self.assertEqual(0,delNum(1,1))

if __name__ == '__main__':

	suite1 = unittest.TestLoader().loadTestsFromTestCase(TestFun)
	suite2 = unittest.TestLoader().loadTestsFromTestCase(TestFun)
	allTests = unittest.TestSuite([suite1, suite2])
	unittest.TextTestRunner(verbosity=2).run(allTests)
	