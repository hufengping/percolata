import threading
import os
import sys
import time
import boto
import random
import shutil
import logging
import glob
import pexpect
import urllib
import httplib2
import re
import json

class PseudoDevice(threading.Thread):
    MAX_ERR_TOLERANCE = 10
    def __init__(self, pseudoPlacementName, configuration, repeat):
        threading.Thread.__init__(self)
        self.name = pseudoPlacementName
        self.config = configuration
        self.repeat = repeat
        self.prevDataTimestamp = None
        self.currDataTimestamp = int(time.time())
        self.prevExtDataTimestamp = None
        self.currExtDataTimestamp = int(time.time())
        self.zonecountIndex = 0
        self.isInitOK = True
        try:
            if not os.path.exists("./%s" % pseudoPlacementName):
                os.mkdir("./%s" % pseudoPlacementName)
                os.mkdir("./%s/data" % pseudoPlacementName)
                os.mkdir("./%s/config" % pseudoPlacementName)
                os.mkdir("./%s/log" % pseudoPlacementName)
                os.mkdir("./%s/data/install" % pseudoPlacementName)
                os.mkdir("./%s/data/video" % pseudoPlacementName)
                os.mkdir("./%s/data/tracking" % pseudoPlacementName)
                os.mkdir("./%s/data/loi" % pseudoPlacementName)
                os.mkdir("./%s/data/image" % pseudoPlacementName)
                os.mkdir("./%s/data/zone_count" % pseudoPlacementName)
                os.mkdir("./%s/data/audio" % pseudoPlacementName)
                os.mkdir("./%s/data/audio_db" % pseudoPlacementName)
                os.mkdir("./%s/data/wifi" % pseudoPlacementName)
                os.mkdir("./%s/data/backup_video" % pseudoPlacementName)
            self.logger = logging.getLogger()
            self.logger.addHandler(logging.FileHandler("./%s/log/device.log"%self.name))
            self.logger.setLevel(logging.DEBUG)
        except Exception as e:
            self.logger.error("===ERROR===: device exit with %s"%e)
            self.isInitOK = False

    def getDuration(self):
        if self.config["installation-mode"] == "yes":
            return 15
        elif self.config["capture-mode"] == "video":
            sTime = time.gmtime()
            return 900 - (sTime.tm_min % 15)*60 - sTime.tm_sec
        elif self.config["capture-mode"] == "tracking":
            sTime = time.gmtime()
            return 900 - (sTime.tm_min % 15)*60 - sTime.tm_sec
        elif self.config["capture-mode"] == "loi":
            return random.randint(55,155)
        elif self.config["capture-mode"] == "zone-count":
            ret = 10*pow(2, self.zonecountIndex)
            self.zonecountIndex += 1
            self.zonecountIndex %= 4
            return ret
        else:
            raise ValueError("PseudoDevice.getDuration: Unknown capture-mode: %s"%self.config["capture-mode"])

    def isInSamePeriod(self, time1, time2):
        if (time1 is None) or (time2 is None):
            return False

        return (time1 - time1%900) == (time2 - time2%900)

    def splitFile(self, srcFile, dstDir, prefix, suffix, splitNum):
        #pexpect.run("split %s -n %s"%(srcFile, splitNum))
        splitedList = glob.glob('templates/x??')
        splitedList.sort()
        for i in range(0,splitNum):
            shutil.copy(splitedList[i],"%s/%s_%s_%s_%s.%s"%
                        (dstDir,
                        prefix,
                        str(i+1),
                        str(self.isOverlapped),
                        str(splitNum),
                        suffix
                    ))

    def prepareLoiData(self):
        sys.path.append("./protobuf_messages")
        from loi_pb2 import LOIForegroundBlobData
        MSG = LOIForegroundBlobData()
        loiFileList = glob.glob('templates/loi_template_??.blobproto')
        loiFileList.sort()
        timeStr = time.strftime("%Y-%m-%d-%H-%M-%S",
                time.gmtime(self.prevDataTimestamp))
        nameStr = str(self.name)+"_es_loi_"+timeStr+"_0_%s_%s_%s.blobproto"\
                %(self.dataIndex, self.isOverlapped, self.isLastData)
        pathName = "%s/data/loi/%s"%(self.name, nameStr)
        with open(loiFileList[random.randint(0,2)], 'rb') as fp:
            MSG.ParseFromString(fp.read())
            MSG.placementName = self.name
            MSG.viewId = 0
            MSG.startTimestamp = self.prevDataTimestamp
            MSG.endTimestamp = self.currDataTimestamp
            with open(pathName, "wb") as outfile:
                outfile.write(MSG.SerializeToString())
                outfile.close()

    def prepareExtData(self):
        tag = (True if (int(time.time()) - self.currExtDataTimestamp > 900) else False)
        # backup_video
        if tag:
            self.extDataIndexScheduler()
        else:
            return
        if(not self.config.has_key('videoBackup')) or (self.config['videoBackup']=='enable'):
            self.logger.info("videoBackup enable")
            timeStr = time.strftime("%Y-%m-%d-%H-%M-%S",
                    time.gmtime(self.prevDataTimestamp))
            nameStr = str(self.name)+"_es_backup_video_"+timeStr+"_0_%s_%s_%s"\
                    %(1, self.isOverlapped, 1)
            shutil.copy("templates/backup_video_template.mp4", "%s/data/backup_video/%s.mp4"%\
                    (self.name, nameStr))
            self.logger.info("prepareExtData: generated a backup_video file: %s"%nameStr)
        else:
            self.logger.info("videoBackup disable")

        # wifi
        if self.config.has_key('wifi-sniff-enable') and (self.config['wifi-sniff-enable']=='true'):
            self.logger.info("wifi sniff enable")
            timeStr = time.strftime("%Y-%m-%d-%H-%M-%S",
                    time.gmtime(self.prevExtDataTimestamp))
            nameStr = str(self.name)+"_es_wifi_"+timeStr+"_0_%s_%s_%s"\
                    %(1, self.isOverlappedExtData, 1)
            shutil.copy("templates/wifi_template.csv.gz", "%s/data/wifi/%s.csv.gz"%\
                    (self.name, nameStr))
            self.logger.info("prepareExtData: generated a wifi csv file: %s"%nameStr)
        else:
            self.logger.info("wifi sniff disabled")

        # audio
        # audio_db
        if self.config.has_key('audio') and (self.config['audio']=='true'):
            self.logger.info("audio enable")
            timeStr = time.strftime("%Y-%m-%d-%H-%M-%S",
                    time.gmtime(self.prevDataTimestamp))
            nameStr1 = str(self.name)+"_es_audio_"+timeStr+"_0_%s_%s_%s"\
                    %(1, self.isOverlapped, 1)
            nameStr2 = str(self.name)+"_es_audio_db_"+timeStr+"_0_%s_%s_%s"\
                    %(1, self.isOverlapped, 1)
            shutil.copy("templates/audio_template.3gp", "%s/data/audio/%s.3gp"%\
                        (self.name, nameStr1))
            self.logger.info("prepareExtData: generated a audio db file: %s"%nameStr1)
            shutil.copy("templates/audio_template.blobproto", "%s/data/audio/%s.blobproto"%\
                    (self.name, nameStr2))
            self.logger.info("prepareExtData: generated a audio proto file: %s"%nameStr2)
        else:
            self.logger.info("audio disable")

    def prepareData(self):
        if self.config["installation-mode"] == "yes":
            timeStr = time.strftime("%Y-%m-%d-%H-%M-%S",
                    time.gmtime(self.prevDataTimestamp))
            nameStr = str(self.name)+"_es_install_video_"+timeStr+"_0_%s_%s_%s.3gp"\
                    %(self.dataIndex, self.isOverlapped, self.isLastData)
            shutil.copy("templates/install_template.3gp", "%s/data/install/%s"%\
                    (self.name, nameStr))

        elif self.config["capture-mode"] == "video":
            timeStr = time.strftime("%Y-%m-%d-%H-%M-%S",
                    time.gmtime(self.prevDataTimestamp))
            nameStr = "%s_es_video_"%self.name+timeStr+"_0"
            self.splitFile("templates/video_template.3gp",
                    "%s/data/video/"%self.name, nameStr, "3gp", 10)
        elif self.config["capture-mode"] == "tracking":
            timeStr = time.strftime("%Y-%m-%d-%H-%M-%S",
                    time.gmtime(self.prevDataTimestamp))
            nameStr = "%s_es_tracking_"%self.name+timeStr
            shutil.copy("templates/tracking_template_01.frameproto",
                        "%s/data/tracking/%s_0_01_0_0.frameproto"%(self.name, nameStr))
            shutil.copy("templates/tracking_template_02.frameproto",
                        "%s/data/tracking/%s_0_02_0_1.frameproto"%(self.name, nameStr))
        elif self.config["capture-mode"] == "loi":
            self.prepareLoiData()
        elif self.config["capture-mode"] == "zone-count":
            timeStr = time.strftime("%Y-%m-%d-%H-%M-%S",
                    time.gmtime(self.prevDataTimestamp))
            nameStr1 = str(self.name)+"_es_image_"+timeStr+"_0_%s_%s_%s"\
                    %(self.dataIndex, self.isOverlapped, self.isLastData)
            nameStr2 = str(self.name)+"_es_zone_count_"+timeStr+"_0_%s_%s_%s"\
                    %(self.dataIndex, self.isOverlapped, self.isLastData)
            zcFileList1 = glob.glob('templates/zc_template_??.jpg')
            zcFileList1.sort()
            shutil.copy(zcFileList1[self.zonecountIndex],
                        "%s/data/image/%s.jpg"\
                                %(self.name, nameStr1)
                    )
            zcFileList2 = glob.glob('templates/zc_template_??.zoneCountproto')
            zcFileList2.sort()
            shutil.copy(zcFileList2[self.zonecountIndex],
                        "%s/data/zone_count/%s.zoneCountproto"\
                                %(self.name, nameStr2)
                    )
        else:
            self.logger.error('Unknown capture-mode: %s'%self.config['capture-mode'])
            raise ValueError("Unknown capture-mode: %s"%self.config["capture-mode"])

    def sendMsg(self, filename, dst_uri):
        url = 'https://ci-api.percolata.com/upload_data'
        headers = {'host':'ci-api.percolata.com'}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
        h.add_credentials('phone','11222011')
        regex = re.compile(r'(?P<placement_name>\d{8})_es_(?P<data_type>\w+)_(?P<timeStr>\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})_(?P<viewId>\d)_(?P<index>\d+)_(?P<isOverlapped>0|1)_(?P<isLast>\d+)\.(?P<suffix>\w+)')
        m = regex.match(filename)
        #currently audio have 2 types of datafiles: *.3gp & *.blobproto
        if m.group(2) != 'audio':
            dataType =  m.group(2)
        else:
            if m.group(8) == '3gp':
                dataType = 'audio'
            else:
                dataType = 'audio_db'
        _time1 = int(time.mktime(time.strptime(m.group(3),"%Y-%m-%d-%H-%M-%S")))
        _time2 = _time1 - _time1%900
        data = {
                'version': '0.1.0',
                'placement_name': m.group(1),
                'data_path': dst_uri,
                'data_type': dataType,
                'timestamp': str(_time1),
                'start_timestamp_of_zone': str(_time2),
                'view': m.group(4),
                'fragment_index': m.group(5),
                'is_overlapped_fragment': 'True' if m.group(6)=='1' else 'False'
                }
        if m.group(2) == 'video':
            data['total_fragment'] = m.group(7)
        else:
            data['is_last_fragment'] = 'True' if m.group(7)=='1' else 'False'

        body = urllib.urlencode(data)
        headers['Content-Length'] = str(len(body))

        resp, content = h.request(url, 'POST', headers=headers, body=body)
        if resp['status'] == '200':
            return True
        else:
            self.logger.error('PseudoDevice.sendMsg: %s send msg to api server failed with: \n%s'%
                    (self.name, str(resp)))
            return False

    def uploadConfigToGS(self):
        localConfigFile = "%s/config/%s.json"%(self.name, self.name)
        dst_uri = boto.storage_uri('percolata-test/config/%s.json'%self.name, 'gs')
        with open(localConfigFile, 'w+') as ofile:
            json.dump(self.config, ofile, sort_keys=True)
            ofile.seek(0)
            dst_uri.new_key().set_contents_from_file(ofile)


    def uploadDataToGS(self):
        #don't continuously upload over 10mins a time
        startTime = time.time()
        for each in glob.glob("%s/data/*"%self.name):
            if os.path.isdir(each):
                for dataFile in glob.glob("%s/*"%each):
                    with open(dataFile, 'r') as localFile:
                        dst_uri = boto.storage_uri('percolata-test/pseudo_data/'+dataFile, 'gs')
                        dst_uri.new_key().set_contents_from_file(localFile)
                        #TODO:send kafka msg for this file
                        if self.sendMsg(os.path.split(dataFile)[1],
                                'percolata-test/pseudo_data/'+dataFile
                                ):
                            shutil.os.remove(dataFile)

                        #don't continuously upload over 10mins a time
                        if (time.time() - startTime) > 600:
                            self.logger.info('upload data procedure beyond 10 min,\
                                    terminate uploading procedure to producing new data')
                            return

    def dataIndexScheduler(self):
        if self.isInSamePeriod(self.prevDataTimestamp, self.currDataTimestamp):
            self.dataIndex += 1
        elif self.prevDataTimestamp is None or self.currDataTimestamp%900 == 0:
            self.dataIndex = 1
        else:
            self.dataIndex = 2
        self.prevDataTimestamp,self.currDataTimestamp = self.currDataTimestamp,int(time.time())
        if self.isInSamePeriod(self.prevDataTimestamp, self.currDataTimestamp):
            self.isLastData = 0
            self.isOverlapped = 0
        else:
            self.isLastData = 1
            if not self.currDataTimestamp%900 == 0:
                self.isOverlapped = 1
            else:
                self.isOverlapped = 0

    def extDataIndexScheduler(self):
        if self.isInSamePeriod(self.prevExtDataTimestamp, self.currExtDataTimestamp):
            self.extDataIndex += 1
        elif self.prevExtDataTimestamp is None or self.currExtDataTimestamp%900 == 0:
            self.extDataIndex = 1
        else:
            self.extDataIndex= 2
        self.prevExtDataTimestamp,self.currExtDataTimestamp = self.currExtDataTimestamp,int(time.time())
        if self.isInSamePeriod(self.prevExtDataTimestamp, self.currExtDataTimestamp):
            self.isLastExtData = 0
            self.isOverlappedExtData = 0
        else:
            self.isLastExtData = 1
            if not self.currExtDataTimestamp%900 == 0:
                self.isOverlappedExtData = 1
            else:
                self.isOverlappedExtData = 0

    def run(self):
        count = 0
        err_count = 0
        if not self.isInitOK:
            print("device %s initializer failed" % self.name)
            return
        while count < self.repeat:
            try:
                _dur = self.getDuration()
                time.sleep(_dur)

                self.dataIndexScheduler()

                if self.config["capture-mode"] == "video" and _dur < 450:
                    continue

                #prepare data(generate & split)
                self.prepareData()
                self.prepareExtData()
                #upload config file to gs
                try:
                    err_count -= 1 if err_count > 0 else 0
                    self.uploadConfigToGS()
                except Exception as e:
                    self.logger.error("===ERROR===: %s upload config to GS failure with error: %s"%(self.name, e))
                    err_count += 2
                    if err_count > (PseudoDevice.MAX_ERR_TOLERANCE * 2):
                        self.logger.error("===ERROR===: upload config failed with too many times(>10): %s"%e)
                        self.logger.info("===INFO===: force quit thread of %s"%self.name)
                        return
                    continue
                #upload data files to gs
                #send kafka msg to pipeline-api server
                try:
                    err_count -= 1 if err_count > 0 else 0
                    self.uploadDataToGS()
                except Exception as e:
                    self.logger.error("===ERROR===: %s upload data failed with error: %s"%(self.name, e))
                    err_count += 2
                    if err_count > (PseudoDevice.MAX_ERR_TOLERANCE * 2):
                        self.logger.error("===ERROR===: upload data failed with too many times(>10): %s"%e)
                        self.logger.info("===INFO===: force quit thread of %s"%self.name)
                        return
                    continue

                #end
            except Exception as e:
                print("device %s crashed for exception: %s" %\
                        (self.name, e))
                return
            count += 1

