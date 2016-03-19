#!/usr/bin/env python

import collections
import datetime
import os
import re
import sys
import time
import unittest
from optparse import OptionParser
import pexpect

# import test cases
import cpu_load_test
import data_hole_test
import disk_remain
import memory_leak_test
import reboot_test
import software_update_test
import globals


def build_test_suit(start_time, end_time):
    # build test suite
    suite = unittest.TestSuite()
    suite.addTest(cpu_load_test.CpuLoadTestCase("testCpuLoad"))
    suite.addTest(data_hole_test.DataHolekTestCase("testDataHole", start_time, end_time))
    suite.addTest(disk_remain.DiskRemainTestCase("testDiskRemain"))
    suite.addTest(memory_leak_test.MemoryLeakTestCase("testMemoryLeak"))
    suite.addTest(reboot_test.RebootTestCase("testReboot"))
    suite.addTest(software_update_test.SoftwareUpdateTestCase("testSoftwareUpdate"))
    return suite

def get_log_time(log_line):
    """get the log_line print time

    Args:
        log_line: a line of the log file
    """

    begin_index = log_line.find("|")
    begin_index = log_line.find("|", begin_index + 1)    # find the second "|"
    end_index = log_line.find("|", begin_index + 1)

    return log_line[begin_index + 1:end_index]

def parse_log_file(file_name, start_time, end_time):
    """Parse log file
    Args:
        file_name: the file need to be parsed
    """

    # parse tag
    MONITOR_TAG = "BS-sysmon"
    REBOOT_TAG = "SD wait:"
    CPU_TAG = "C:"
    MEMORY_TAG = "M:"
    DISK_TAG = "F:"

    with open(file_name) as log_file:
        # parse log file by line
        for line in log_file:
            log_time = get_log_time(line)
            if (cmp(log_time, start_time) < 0 or
                cmp(log_time, end_time) >0):
                # not in the monitor time
                continue

            # parse reboot log
            index = line.find(REBOOT_TAG)
            if index != -1:
                # save reboot time
                globals.reboot_time_list.append((placement_id, log_time))
                #print (placement_id, reboot_time)

                # save local version
                begin_index = line.find("@")
                end_index = line.find(", ", begin_index)
                globals.device_version = line[begin_index + 1:end_index]

            # parse monitor log, including CPU, Memory, Disk
            index = line.find(MONITOR_TAG)
            if index != -1:
                monitor_str = line[index + len(MONITOR_TAG):]
                log_time = get_log_time(line)
                # save cpu load
                begin_index = monitor_str.find(CPU_TAG)
                end_index = monitor_str.find("|", begin_index + 1)
                cpu_load = int(monitor_str[begin_index + len(CPU_TAG):end_index])
                globals.cpu_load_list.append((placement_id, log_time, cpu_load))
                #print (placement_id, log_time, cpu_load)

                # save memory used
                begin_index = monitor_str.find(MEMORY_TAG)
                end_index = monitor_str.find("|", begin_index + 1)
                memory_used = monitor_str[begin_index + len(MEMORY_TAG):end_index].split("/")
                globals.memory_used_list.append((placement_id, log_time, int(memory_used[0]), int(memory_used[1])))
                #print (placement_id, log_time, int(memory_used[0]), int(memory_used[1]))

                # save disk remained
                begin_index = monitor_str.find(DISK_TAG)
                end_index = monitor_str.find("|", begin_index + 1)
                disk_remained = int(monitor_str[begin_index + len(DISK_TAG):end_index])
                globals.disk_remained_list.append((placement_id, log_time, disk_remained))
                #print (placement_id, log_time, disk_remained)

#         # for test
#         print reboot_time_list
#         print cpu_load_list
#         print memory_used_list
#         print disk_remained_list

def load_log_file(placement_id):
    # Notice: set local_dir, need the permission to create the directory
    local_dir = os.getcwd()

    # server log
    log_dir = "/log/"
    log_file_path = "/log/placement_%s.txt" % placement_id

    # make local directory to consist with server
    local_log_dir = local_dir + log_dir
    if not os.path.exists(local_log_dir):
       os.makedirs(local_log_dir)
    local_log_path = local_dir + log_file_path

    # download command format "scp {user_name}@{server_name}:{file_path} {local_path}"
    raw_command = "scp {user_name}@{server_name}:{file_path} {local_path}"
    download_command = raw_command.format(user_name=globals.USER_NAME,
                                          server_name=globals.SERVER_NAME,
                                          file_path=log_file_path,
                                          local_path=local_log_path)
    os.system(download_command)     # download log from remote server

    return local_log_path


def parse_option_args():
    # parse the options
    parser = OptionParser()
    parser.add_option("-s", "--start", help="The starting time, in format of YYYY:MM:DD:hh:mm:ss. By default it is the time when the device is deployed")
    parser.add_option("-e", "--end", help="The end time, in format of YYYY:MM:DD:hh:mm:ss. By default it is the current time")
    (options, args) = parser.parse_args()
    start_time = options.start
    end_time = options.end

    # We assume the script is running in a server with UTC timezone
    # so ignore the timezone setting now.
    if start_time is None:
        start_time = "1969:01:01:00:00:00"
    if end_time is None:
        end_time = time.strftime("%Y:%m:%d:%H:%M:%S")

    return (start_time, end_time)

def init_globals():
    # initiator globals args
    del globals.placement_id_list[:]
    del globals.cpu_load_list[:]
    del globals.memory_used_list[:]
    del globals.disk_remained_list[:]
    del globals.reboot_time_list[:]
    #globals.device_version = ""

def timeout_handler(d):
    pass


# test script
if __name__ == "__main__":
    usage_str = """
    Usage:
    unit_test_main.py {[ID_LIST] OR ID_FILE}
        {[ID_LIST] OR ID_FILE}:
            [id_list]: [placement_id1,placement_id2,placement_id3...]
            id_file:   input file contains placement ids, one row one id
    """

    if len(sys.argv) < 2:
        print(usage_str)
        raise Exception("undefined exception.")

    # parse placement id
    id_source = sys.argv[1]
    id_list = list()
    if os.path.isfile(id_source):
        # id input file
        with open(id_source) as input_file:
            for line in input_file.readlines():
                line = line.strip() # remove empty char
                if not len(line) or line.startswith('#'):
                    # skip the empty line or comment line
                    continue
                id_list.append(line)
    elif id_source.startswith("[") and id_source.endswith("]"):
        id_list = id_source.lstrip("[").rstrip("]").split(",")
    else:
        print("Id source has error, please check it: ", id_source)
        raise Exception("undefined exception.")

    # parse start and end time of log
    (start_time, end_time) = parse_option_args()
    print start_time, end_time
    print("****Unit Test Begin****")
    globals.test_result = "TEST_RESULT="
    for placement_id in id_list:
        globals.test_result += "placement_id[%s]:\n" % placement_id
        init_globals()
        log_file = load_log_file(placement_id)
        print("begin load log file: ", log_file)
        if os.path.exists(log_file):
            # the file path format is like "./log/placement_8100005.txt"
            print("begin parse log file: ", log_file)
            parse_log_file(log_file, start_time, end_time)
            globals.placement_id_list.append(placement_id)

            # remove log file to save disk
            os.remove(log_file)

            # implement test
            print("begin test log file: ", log_file)
            suite = build_test_suit(start_time, end_time)
            runner = unittest.TextTestRunner()
            runner.run(suite)

    globals.test_result = globals.test_result.replace('\n', '<br/>')
    #print "+"*50
    if globals.test_result.endswith('<br/><br/>'):
        globals.test_result = globals.test_result[:-10]
    #print globals.test_result

    # write tht test result to the file which store the environment variables of jenkins
    with open('./propsfile', 'w') as f:
        f.write(globals.test_result)

        print("****AUTOMATED TEST BEGIN****")
        pexpect.run('python ../test_main.py ',events={pexpect.TIMEOUT:timeout_handler})
        pexpect.run('mv -f ../test_log .')
        with open('test_log','r') as log:
            f.write('<br/><br/>')
            f.write('TestCases Error List: <br/>')
            for ln in log:
                if not(ln.find('ERROR') == -1):
                    print("="*30)
                    print(ln)
                    f.write(ln.replace('\n', '<br/>'))
                    print("-"*30)

    timestr = time.strftime("_%Y-%m-%d-%H")
    pexpect.run('mv test_log test_log%s'%(timestr),events={pexpect.TIMEOUT:timeout_handler})
    #print("****Unit Test End****")
