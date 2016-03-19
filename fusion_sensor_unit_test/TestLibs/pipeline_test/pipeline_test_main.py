#!/usr/bin/env python

import os
import sys
from optparse import OptionParser
import json
import random
import logging
import inspect
import multiprocessing as mulp
from pseudo_device import PseudoDevice

CONFIG_TEMPLATE="./templates/config_template.json"
CURRENT_FRAME = inspect.currentframe()
logger = logging.getLogger()
logger.addHandler(logging.FileHandler("pipeline_test.log"))
logger.setLevel(logging.DEBUG)

class PseudoPlacementNameFactory:
    MAX_DEV_NUM = 2000
    BEGIN_NAME  = 59370001
    def __init__(self):
        self.nameList = list()
        for i in range(PseudoPlacementNameFactory.MAX_DEV_NUM):
            self.nameList.append(str(PseudoPlacementNameFactory.BEGIN_NAME + i))
    def getPlacementName(self):
        try:
            #return self.nameList.pop(random.randint(0, self.nameList.__len__()-1))
            return self.nameList.pop(0)
        except Exception as e:
            logger.error("===ERROR===: " + e.message + '''
                    raised by PseudoPlacementNameFactory.getPlacementName()
                    in file: %s
                    at line: %s'''%(
                        CURRENT_FRAME.f_code.co_filename,
                        CURRENT_FRAME.f_lineno))

def parse_option_args():
    parser = OptionParser()

    parser.add_option("-I","--install",help="number of simulate device in install mode.")
    parser.add_option("-V","--video",help="number of simulate device in video mode.")
    parser.add_option("-L","--loi",help="number of simulate device in loi mode.")
    parser.add_option("-T","--tracking",help="number of simulate device in tracking mode.")
    parser.add_option("-Z","--zonecount",help="number of simulate device in zone-count mode.")

    (options, args) = parser.parse_args()

    install = options.install
    if install is None:
        install = 0
    else:
        install = int(install)
    loi = options.loi
    if loi is None:
        loi = 0
    else:
        loi = int(loi)
    tracking = options.tracking
    if tracking is None:
        tracking = 0
    else:
        tracking = int(tracking)
    video = options.video
    if video is None:
        video = 0
    else:
        video = int(video)
    zonecount = options.zonecount
    if zonecount is None:
        zonecount = 0
    else:
        zonecount = int(zonecount)

    return (install, loi, tracking, video, zonecount)

def getConfig(srcFile, mode):
    with open(srcFile, 'r') as fp:
        _conf = json.load(fp)
        if "install" == mode:
            _conf["installation-mode"] = "yes"
        else:
            _conf["installation-mode"] = "no"
            _conf["capture-mode"] = mode
        return _conf

def runPseudoDevice(name, conf, repeat):
    try:
        PseudoDevice(name,
              conf,
              repeat
            ).run()
    except Exception as e:
        logger.error("===ERROR===: " + e.message + '''
            raised by PseudoDevice.__init__()
            in file: %s
            at line: %s'''%(
            CURRENT_FRAME.f_code.co_filename,
            CURRENT_FRAME.f_lineno))

def multiProcessMain(args):
    nameGenerator = PseudoPlacementNameFactory()
    pList = list()

    install_config = getConfig(CONFIG_TEMPLATE, "install")
    for i in range(args[0]):
        process = mulp.Process(target=runPseudoDevice,
            args=(nameGenerator.getPlacementName(),
                install_config,
                2000)
            )
        process.start()
        pList.append(process)

    loi_config = getConfig(CONFIG_TEMPLATE, "loi")
    for i in range(args[1]):
        process = mulp.Process(target=runPseudoDevice,
            args=(nameGenerator.getPlacementName(),
                loi_config,
                300)
            )
        process.start()
        pList.append(process)

    tracking_config = getConfig(CONFIG_TEMPLATE, "tracking")
    for i in range(args[2]):
        process = mulp.Process(target=runPseudoDevice,
            args=(nameGenerator.getPlacementName(),
                tracking_config,
                40)
            )
        process.start()
        pList.append(process)

    video_config = getConfig(CONFIG_TEMPLATE, "video")
    for i in range(args[3]):
        process = mulp.Process(target=runPseudoDevice,
            args=(nameGenerator.getPlacementName(),
                video_config,
                40)
            )
        process.start()
        pList.append(process)

    zonecount_config = getConfig(CONFIG_TEMPLATE, "zone-count")
    for i in range(args[4]):
        process = mulp.Process(target=runPseudoDevice,
            args=(nameGenerator.getPlacementName(),
                zonecount_config,
                900)
            )
        process.start()
        pList.append(process)

    for p in pList:
        p.join()


def multiThreadMain(args):
    nameGenerator = PseudoPlacementNameFactory()

    install_config = getConfig(CONFIG_TEMPLATE, "install")
    for i in range(args[0]):
        try:
            PseudoDevice(nameGenerator.getPlacementName(),
                      install_config,
                      2000
                    ).start()
        except Exception as e:
            logger.error("===ERROR===: " + e.message + '''
                    raised by PseudoDevice.__init__()
                    in file: %s
                    at line: %s'''%(
                        CURRENT_FRAME.f_code.co_filename,
                        CURRENT_FRAME.f_lineno))
    loi_config = getConfig(CONFIG_TEMPLATE, "loi")
    for i in range(args[1]):
        try:
            PseudoDevice(nameGenerator.getPlacementName(),
                  loi_config,
                  300
                ).start()
        except Exception as e:
            logger.error("===ERROR===: " + e.message + '''
                    raised by PseudoDevice.__init__()
                    in file: %s
                    at line: %s'''%(
                        CURRENT_FRAME.f_code.co_filename,
                        CURRENT_FRAME.f_lineno))
    tracking_config = getConfig(CONFIG_TEMPLATE, "tracking")
    for i in range(args[2]):
        try:
            PseudoDevice(nameGenerator.getPlacementName(),
                  tracking_config,
                  40
                ).start()
        except Exception as e:
            logger.error("===ERROR===: " + e.message + '''
                    raised by PseudoDevice.__init__()
                    in file: %s
                    at line: %s'''%(
                        CURRENT_FRAME.f_code.co_filename,
                        CURRENT_FRAME.f_lineno))
    video_config = getConfig(CONFIG_TEMPLATE, "video")
    for i in range(args[3]):
        try:
            PseudoDevice(nameGenerator.getPlacementName(),
                  video_config,
                  40
                ).start()
        except Exception as e:
            logger.error("===ERROR===: " + e.message + '''
                    raised by PseudoDevice.__init__()
                    in file: %s
                    at line: %s'''%(
                        CURRENT_FRAME.f_code.co_filename,
                        CURRENT_FRAME.f_lineno))
    zonecount_config = getConfig(CONFIG_TEMPLATE, "zone-count")
    for i in range(args[4]):
        try:
            PseudoDevice(nameGenerator.getPlacementName(),
                  zonecount_config,
                  1000
                ).start()
        except Exception as e:
            logger.error("===ERROR===: " + e.message + '''
                    raised by PseudoDevice.__init__()
                    in file: %s
                    at line: %s'''%(
                        CURRENT_FRAME.f_code.co_filename,
                        CURRENT_FRAME.f_lineno))

if __name__ == '__main__':
    args = parse_option_args()
    multiProcessMain(args)
