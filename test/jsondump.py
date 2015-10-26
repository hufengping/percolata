'''
Created on 30 Aug 2015

@author: fengpinghu

'''
import test_unittest.HTMLTestRunner as HTMLTestRunner

print "test"
if __name__ == '__main__':
    
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                                           stream=fp,
                                           title='My unit test',
                                           description='This demonstrates the report output by HTMLTestRunner.'
                                           )