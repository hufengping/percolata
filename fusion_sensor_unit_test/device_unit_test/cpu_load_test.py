import unittest
from unit_test_exception import CpuLoadException
import globals
from globals import cpu_load_list


class CpuLoadTestCase(unittest.TestCase):

    """Test CPU Load"""

    # the max cpu load
    CPU_LOAD_THRESHOLD = 80     # 80%

    # use the average avoid temp exception
    CPU_LOAD_STEP = 10

    def setUp(self):
        self.cpu_load_exception_count = 0
        self.cpu_load_average = 0

    def tearDown(self):
        pass

    def testCpuLoad(self):
        print
        print "****CPU Load Test Begin****"
        global cpu_load_list

        # CPU load set format (placement_id, log_time, cpu_load)
        CPU_LOAD_INDEX = -1

        cpu_load_sum = 0
        average = 0
        for index in range(0, len(cpu_load_list)):
            self.cpu_load_average += cpu_load_list[index][CPU_LOAD_INDEX]
            if index < CpuLoadTestCase.CPU_LOAD_STEP:
                cpu_load_sum += cpu_load_list[index][CPU_LOAD_INDEX]
            else:
                cpu_load_sum += (cpu_load_list[index][CPU_LOAD_INDEX] -
                                 cpu_load_list[index - CpuLoadTestCase.CPU_LOAD_STEP][CPU_LOAD_INDEX])
                average = cpu_load_sum / CpuLoadTestCase.CPU_LOAD_STEP
                if average > CpuLoadTestCase.CPU_LOAD_THRESHOLD:
                    self.cpu_load_exception_count += 1
                    print "CPU Load Exception:", cpu_load_list[index]

        self.cpu_load_average /= len(cpu_load_list)

        # add test result
        globals.test_result += """
Cpu:
CPU_LOAD_THRESHOLD: %s
cpu_load_average: %s
cpu_load_exception_count: %s
""" % (CpuLoadTestCase.CPU_LOAD_THRESHOLD, self.cpu_load_average, self.cpu_load_exception_count)
        print "cpu_load_average is: ", self.cpu_load_average

        print "cpu_load_exception_count is: ", self.cpu_load_exception_count

        print "****CPU Load Test End****"

        if self.cpu_load_exception_count > 0:
            raise CpuLoadException(self.cpu_load_exception_count)
