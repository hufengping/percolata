
import test_unittest
import globals
from globals import reboot_time_list
from unit_test_exception import RebootException

# test case class
class RebootTestCase(test_unittest.TestCase):
    REBOOT_COUNT_THRESHOLD = 1
    
    def setUp(self):
        self.reboot_count = 0
    
    def tearDown(self):
        pass
    
    def testReboot(self):
        print
        print "****Reboot Test Begin****"
        
        global reboot_time_list
        
        self.reboot_count = len(reboot_time_list)

        # add test result
        globals.test_result += """
Reboot:
REBOOT_COUNT_THRESHOLD: %s
reboot_count: %s
""" % (RebootTestCase.REBOOT_COUNT_THRESHOLD, self.reboot_count)

        print "Reboot count: ", self.reboot_count
        print "Reboot time:", reboot_time_list
        
        print "****Reboot Test End****"
        
        if self.reboot_count > RebootTestCase.REBOOT_COUNT_THRESHOLD:
            raise RebootException(self.reboot_count)