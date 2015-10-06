import unittest
import globals
from globals import disk_remained_list
from unit_test_exception import DataHoleException

# test case class
class DiskRemainTestCase(unittest.TestCase):
    DISK_REMAIN_THRESHOLD = 128
    DISK_REMAIN_STEP = 10
        
    def setUp(self):
        self.disk_remain_exception_count = 0
    
    def tearDown(self):
        pass
    
    def testDiskRemain(self):
        print
        print "****Disk Remain Test Begin****"
        
        global disk_remained_list
        
        # disk remain item format: (placement_id, log_time, disk_remained)
        DISK_REMAIN_INDEX = -1
        
        cpu_load_sum = 0
        average = 0
        for index in range(0, len(disk_remained_list)):
            if index < DiskRemainTestCase.DISK_REMAIN_STEP:
                cpu_load_sum += disk_remained_list[index][DISK_REMAIN_INDEX]
            else:
                cpu_load_sum +=  (disk_remained_list[index][DISK_REMAIN_INDEX] - 
                         disk_remained_list[index - DiskRemainTestCase.DISK_REMAIN_STEP][DISK_REMAIN_INDEX])                
                average = cpu_load_sum / DiskRemainTestCase.DISK_REMAIN_STEP
                # notice, should less than DISK_REMAIN_THRESHOLD
                if average < DiskRemainTestCase.DISK_REMAIN_THRESHOLD:                    
                    self.disk_remain_exception_count += 1
                    print "Disk Remain Exception:", disk_remained_list[index]

        globals.test_result +="""
Disk:
DISK_REMAIN_THRESHOLD: %s
disk_remain_exception_count: %s
""" % (DiskRemainTestCase.DISK_REMAIN_THRESHOLD, self.disk_remain_exception_count)
                    
        print "disk_remain_exception_count is: " , self.disk_remain_exception_count
        
        print "****Disk Remain Test End****"
        
        if self.disk_remain_exception_count > 0:
            raise DataHoleException(self.disk_remain_exception_count)