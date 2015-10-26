
import test_unittest
import globals
from globals import memory_used_list
from unit_test_exception import MemoryLeakException

# test case class
class MemoryLeakTestCase(test_unittest.TestCase):

    MEMORY_USED_THRESHOLD = 410     # 80% of 512M memory
    MEMORY_USED_STEP = 10
 
    def setUp(self):
        self.memory_used_exception_count = 0
        self.memory_used_average = 0
    
    def tearDown(self):
        pass
    
    def testMemoryLeak(self):
        print
        print "****Memory Leak Test End****"
        
        global memory_used_list
        
        # memory used item format:
        # (placement_id, log_time, memory_used, memory_remained) 
        MEMORY_USED_INDEX = -2
        
        memory_used_step_sum = 0
        memory_used_step_average = 0
        for index in range(0, len(memory_used_list)):
            self.memory_used_average += memory_used_list[index][MEMORY_USED_INDEX]
            if index < MemoryLeakTestCase.MEMORY_USED_STEP:
                memory_used_step_sum += memory_used_list[index][MEMORY_USED_INDEX]
            else:
                memory_used_step_sum += (memory_used_list[index][MEMORY_USED_INDEX] - 
                        memory_used_list[index - MemoryLeakTestCase.MEMORY_USED_STEP][MEMORY_USED_INDEX])                
                memory_used_step_average = memory_used_step_sum / MemoryLeakTestCase.MEMORY_USED_STEP
                if memory_used_step_average > MemoryLeakTestCase.MEMORY_USED_THRESHOLD:
                    self.memory_used_exception_count += 1
                    print "Memory Leak Exception:", memory_used_list[index]
        
        self.memory_used_average /= len(memory_used_list)

        globals.test_result +="""
Memory:
MEMORY_USED_THRESHOLD: %s
memory_used_average: %s
memory_used_exception_count %s
""" % (MemoryLeakTestCase.MEMORY_USED_THRESHOLD, self.memory_used_average, self.memory_used_exception_count)


        print "memory_used_average is : ", self.memory_used_average
                    
        print "memory_used_exception_count is : ", self.memory_used_exception_count
                        
        print "****Memory Leak Test End****"
        
        if self.memory_used_exception_count > 0:
            raise MemoryLeakException(self.memory_used_exception_count)        
