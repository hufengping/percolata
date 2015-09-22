import unittest
import paramiko
import sys
import time
import datetime
import re
#import matplotlib.pyplot as plt
import collections
from optparse import OptionParser
from unit_test_exception import DataHoleException
import globals
from globals import *


# test case class
class DataHolekTestCase(unittest.TestCase):
    delay_tolerrance = 1

    def __init__(self, name, start_time, end_time):
        super(DataHolekTestCase, self).__init__(name)
        self.start_time = start_time
        self.end_time = end_time
     
    def setUp(self):
        self.data_hole_count = 0  
    
    def tearDown(self):
        pass
    

    def parseWifiFileList(self, wfilelist, start_datetime, end_datetime):
        wdatalist={}
        f=iter(wfilelist)
        first = True
        try:
            while True:
                vfile = f.next()
                name=re.split('_|-|\.', vfile)
                if len(name) < 11:
                    continue
                if name[9] != "dat":
                    continue
                data_time = datetime.datetime(int(name[3]), int(name[4]), int(name[5]), int(name[6]), int(name[7]), int(name[8]))
                if first:
                    first = False
                    if data_time > start_datetime:
                        start_datetime = data_time
    
                if data_time < start_datetime:
                    continue
                if data_time > end_datetime:
                    continue    
    
                #if wdatalist.get(data_time.strftime("%d %H:%M:%S"), 0) == 1:
                #    continue
                if len(wdatalist) == 0:
                    prev_wtime = data_time
                    wdatalist[data_time.strftime("%m %d %H:%M:%S")] = 1
                t1 = time.mktime(data_time.timetuple())
                t2 = time.mktime(prev_wtime.timetuple())
                time_delta = (int)(round((t1-t2)/60))
                while time_delta > 15+int(DataHolekTestCase.delay_tolerrance):
                    next_time = prev_wtime + datetime.timedelta(seconds=15*60)
                    prev_wtime = next_time
                    time_delta -= 15
                    wdatalist[next_time.strftime("%m %d %H:%M:%S")] = 0
                if len(name) == 11:
                    wdatalist[data_time.strftime("%m %d %H:%M:%S")] = 1
                elif len(name) == 13:
                    if data_time.strftime("%m %d %H:%M:%S") not in wdatalist:
                        split_num = int(name[11])
                        for i in range(split_num):
                            chunk=list(vfile)
                            chunk[-6]=chr(ord('0')+i+1)
                            if "".join(chunk) not in wfilelist:
                                wdatalist[data_time.strftime("%m %d %H:%M:%S")] = 0
                                break
                        else:
                            wdatalist[data_time.strftime("%m %d %H:%M:%S")] = 1
                prev_wtime = data_time
        except StopIteration:
            pass
        return wdatalist

    def parseVideoFileList(self, vfilelist, start_datetime, end_datetime):
            
        vdatalist={}
        first = True
        for vfile in vfilelist:
            name=re.split('_|-|\.', vfile)
            if len(name) != 11:
                continue
            if name[10] != "3gp":
                continue
            data_time = datetime.datetime(int(name[2]), int(name[3]), int(name[4]), int(name[5]), int(name[6]), int(name[7]))
            if first:
                first = False
                if data_time > start_datetime:
                    start_datetime = data_time
    
            if data_time < start_datetime:
                continue
            if data_time > end_datetime:
                continue    
            #if vdatalist.get(data_time.strftime("%d %H:%M:%S"), 0) == 1:
            #    continue
            #print data_time
            if len(vdatalist) == 0:
                vdatalist[data_time.strftime("%m %d %H:%M:%S")] = 1
                prev_vtime = data_time
            else:
                t1 = time.mktime(data_time.timetuple())
                t2 = time.mktime(prev_vtime.timetuple())
                time_delta = (int)(round((t1-t2)/60))
                while time_delta > 15+int(DataHolekTestCase.delay_tolerrance):
                    next_time = prev_vtime + datetime.timedelta(seconds=15*60)
                    vdatalist[next_time.strftime("%m %d %H:%M:%S")] = 0
                    prev_vtime = next_time
                    time_delta -= 15
                vdatalist[data_time.strftime("%m %d %H:%M:%S")] = 1
                prev_vtime = data_time
        return vdatalist


    def testDataHole(self):
        print
        print "****Data Hole Test Begin****"
        
        # global constants
        global SERVER_NAME
        global USER_NAME
        
        # global variables
        global placement_id_list
                
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=SERVER_NAME, username=USER_NAME)
        
        for placementId in placement_id_list:
                #start_time = "1969:01:01:00:00:00"
                #end_time = time.strftime("%Y:%m:%d:%H:%M:%S")
                start_time = self.start_time
                end_time = self.end_time
                #We assume the script is running in a server with UTC timezone
                #so ignore the timezone setting now.
        
                start_datetime = datetime.datetime.strptime(start_time, "%Y:%m:%d:%H:%M:%S")
                end_datetime = datetime.datetime.strptime(end_time, "%Y:%m:%d:%H:%M:%S")
                print SERVER_NAME, placementId, DataHolekTestCase.delay_tolerrance, start_datetime, end_datetime
        
                vpath='/data/video/dump/'+placementId
                vpattern='"*.3gp"'
                wpath='/data/wifi_dumpcap/dump/'+placementId
                wpattern='"*.dat*.gz"'
                rawcommand='find {path} -name {pattern} | sort'
        
                vcommand = rawcommand.format(path=vpath,pattern=vpattern)
                stdin,stdout,stderr = ssh.exec_command(vcommand)
                vfilelist=stdout.read().splitlines()
        
                wcommand = rawcommand.format(path=wpath,pattern=wpattern)
                stdin,stdout,stderr = ssh.exec_command(wcommand)
                wfilelist=stdout.read().splitlines()
        
                vdatalist = collections.OrderedDict(sorted(self.parseVideoFileList(vfilelist, start_datetime, end_datetime).items()))
                wdatalist = collections.OrderedDict(sorted(self.parseWifiFileList(wfilelist, start_datetime, end_datetime).items()))
                #print vdatalist
        
                vdata_show={}
                wdata_show={}
        
                vdata_items = vdatalist.items()
                vdata_keys = vdatalist.keys()
                wdata_items = wdatalist.items()
                wdata_keys = wdatalist.keys()
        
                vdatahole = 0
                for d in vdatalist:
                    if vdatalist[d] == 0:
                        hole_index = vdata_keys.index(d)
                        #vdata_show[vdata_items[hole_index - 1][0]] = vdata_items[hole_index - 1][1]
                        vdata_show[vdata_items[hole_index][0]] = vdata_items[hole_index][1]
                        #vdata_show[vdata_items[hole_index + 1][0]] = vdata_items[hole_index + 1][1]
                        vdatahole += 1
        #        latest_range =  1
        #        if len(vdata_keys) > 1:
        #            latest_range += 1
        #            if len(vdata_keys) > 2:
        #                latest_range += 1
        #                if len(vdata_keys) > 3:
        #                    latest_range += 1
        
        #        for i in range(len(vdata_keys)-latest_range, len(vdata_keys)):
        #            vdata_show[vdata_items[i][0]] = vdata_items[i][1]
                wdatahole = 0
                for d in wdatalist:
                    if wdatalist[d] == 0:
                        hole_index = wdata_keys.index(d)
                        wdata_show[wdata_items[hole_index - 1][0]] = wdata_items[hole_index - 1][1]
                        wdata_show[wdata_items[hole_index][0]] = wdata_items[hole_index][1]
                        wdata_show[wdata_items[hole_index + 1][0]] = wdata_items[hole_index + 1][1]
                        wdatahole += 1
        #        latest_range =  1
        #        if len(wdata_keys) > 1:
        #            latest_range += 1
        #            if len(wdata_keys) > 2:
        #                latest_range += 1
        #                if len(wdata_keys) > 3:
        #                    latest_range += 1
        
        #        for i in range(len(wdata_keys)-latest_range, len(wdata_keys)):
        #            wdata_show[wdata_items[i][0]] = wdata_items[i][1]
        
                vdata_show = collections.OrderedDict(sorted(vdata_show.items()))
                wdata_show = collections.OrderedDict(sorted(wdata_show.items()))
        
                #calculate the duration
                vtotal_run_str = ""
                if vdatalist:
                    vstart = datetime.datetime.strptime(vdatalist.keys()[0], '%m %d %H:%M:%S')
                    vend = datetime.datetime.strptime(vdatalist.keys()[len(vdatalist.keys())-1], '%m %d %H:%M:%S')
                    velaps = vend-vstart
                    vtotal_run = divmod(velaps.total_seconds(), 86400)
                    vtotal_h = divmod(vtotal_run[1], 3600)
                    vtotal_m = divmod(vtotal_h[1], 60)
                    vtotal_run_str = "%d days %d hours %d mins" % (vtotal_run[0], vtotal_h[0], vtotal_m[0])
                
                wtotal_run_str = ""
                if wdatalist:
                    wstart = datetime.datetime.strptime(wdatalist.keys()[0], '%m %d %H:%M:%S')
                    wend = datetime.datetime.strptime(wdatalist.keys()[len(wdatalist.keys())-1], '%m %d %H:%M:%S')
                    welaps = wend-wstart
                    wtotal_run = divmod(welaps.total_seconds(), 86400)
                    wtotal_h = divmod(wtotal_run[1], 3600)
                    wtotal_m = divmod(wtotal_h[1], 60)
                    wtotal_run_str = "%d days %d hours %d mins" % (wtotal_run[0], wtotal_h[0], wtotal_m[0])
        
                print "Video module runs for "+vtotal_run_str
                print "Wifi module runs for "+wtotal_run_str
                print "From %s to %s: %d video data holes and %d wifi data holes"%(start_datetime.strftime("%Y:%m:%d:%H:%M:%S"), end_datetime.strftime("%Y:%m:%d:%H:%M:%S"), vdatahole, wdatahole)
                print "Video data holes: "
                print vdata_show
                print "Wifi data holes: "
                print wdata_show
            
                #plt.ion()
                #ax1.set_xticks(range(0,len(vdata_show)), minor=False)
                #ax1.set_xticklabels(vdata_show.keys(), fontdict=None, minor=False)
                #ax1.plot(vdata_show.values())
                #ax1.set_title('Video data with time (latest one hour, or data holes) ' + vtotal_run_str)
                #ax1.set_ylim([0,2])
        
                #ax2.set_xticks(range(0,len(wdata_show)), minor=False)
                #ax2.set_xticklabels(wdata_show.keys(), fontdict=None, minor=False)
                #ax2.plot(wdata_show.values())
                #ax2.set_title('Wifi data with time (latest one hour, or data holes)' + wtotal_run_str)
                #ax2.set_ylim([0,2])
        
                #mng = plt.get_current_fig_manager()
                #mng.window.wm_geometry("3600x800+20+40")
                #plt.draw()
                
                self.data_hole_count += vdatahole + wdatahole
        ssh.close()

        # add to test_result
        globals.test_result +="""
Data hole:
data_hole_count: %s
""" % (self.data_hole_count)
        
        print "****Data Hole Test End****"
            
        if self.data_hole_count > 0:
            raise DataHoleException(self.data_hole_count)
