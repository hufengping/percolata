'''
Created on 30 Aug 2015

@author: fengpinghu
'''
#coding=utf-8
from count import Count
import unittest
import HTMLTestRunner

class TestCount(unittest.TestCase):

    def setUp(self):
        self.j = Count(2, 3)


    def test_add(self):
        '''This will be the description of the TestCase--test_add.'''

        self.add = self.j.add()
        self.assertEqual(self.add,5)
        print "Test is OK !"

    def test_add2(self):
        '''This will be the description of the TestCase--test_add2.'''
        self.add = self.j.add()
        self.assertEqual(self.add,2)
        print "Test is ERROR !"

    @unittest.skip("skip")
    def test_add3(self):
        '''This will be the description of the TestCase--test_add3.'''
        self.add = self.j.add()
        self.assertEqual(self.add,2)
        print "Test is ERROR !"


    def tearDown(self):

        pass


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestCount("test_add"))
    suite.addTest(TestCount("test_add2"))
    suite.addTest(TestCount("test_add3"))

    
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                                           stream=fp,
                                           title='Percolata Test Report',
                                           description='Fusion Sensor 2.0 TestCase-0210'
                                           )
    runner.run(suite)
