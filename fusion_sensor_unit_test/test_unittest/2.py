#!/usr/bin/env python
'''setUp teardown'''
import unittest


def addnum(a, b):
	return a+b


def delnum(a, b):
	return a-b


class TestFun(unittest.TestCase):

	def setUp(self):
		print 'do before class....'

	def test_Add(self):
		print 'test add................'
		self.assertEqual(1, addnum(1, 1))

	def test_Del(self):
		print 'test del................'
		self.assertEqual(0, delnum(1, 1))

	def tearDown(self):
		print 'do after class....'

if __name__ == "__main__":
	unittest.main()
