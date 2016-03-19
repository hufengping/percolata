#!/usr/bin/env python
'''unittest, assert'''
import unittest


def addnum(a, b):
	return a+b


def delnum(a, b):
	return a-b


class TestFun(unittest.TestCase):

	def test_Add(self):
		print 'test add................'
		self.assertEqual(1, addnum(1, 1))

if __name__ == "__main__":
	unittest.main()



