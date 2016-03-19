#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
_____________________________________________________________________________
Update Record:
    2015-12-16: Adjust the test framework for FusionSensor2.0 with new data
                pipeline.

_____________________________________________________________________________
 * BAY SENSORS INC CONFIDENTIAL
 *
 *
 *  Copyright [2012] - [2014] Bay Sensors Inc
 *  All Rights Reserved.
 *
 * NOTICE:  All information contained herein is, and remains
 * the property of Bay Sensors Inc.
 * The intellectual and technical concepts contained herein are proprietary
 * to Bay Sensors Inc., and may be covered by U.S. and Foreign Patents,
 * or disclosed and claimed in pending patent applications, and are protected
 * by trade secret or copyright law.
 * Dissemination of this information or reproduction of this material is
 * strictly forbidden unless prior written permission is obtained from
 * Bay Sensors Inc.
_____________________________________________________________________________
 * @author:  yifei.fu@baysensors.com
 * @version: 2015年 12月 28日 星期四 10:03:32 CST

"""

class ConfigManager(object):
    """Afford method for config modification."""
    def __init__(self, dev):
        self.dev = dev

    def close(self):
        pass

    def setInstallMode(self):
        newCfg = {'installation-mode': "yes"}
        self.dev.setDevCfg(newCfg)

    def setVideoMode(self):
        newCfg = {'capture-mode': "video", 'installation-mode': "no"}
        self.dev.setDevCfg(newCfg)

    def setLoiMode(self):
        newCfg = {'capture-mode': "loi", 'installation-mode': "no"}
        self.dev.setDevCfg(newCfg)

    def setZoneCountMode(self):
        newCfg = {'capture-mode': "zone-count", 'installation-mode': "no"}
        self.dev.setDevCfg(newCfg)

    def setTrackingMode(self):
        newCfg = {'capture-mode': "tracking", 'installation-mode': "no"}
        self.dev.setDevCfg(newCfg)

    def setAudio(self, signal):
        newCfg = dict(
                    audio = "true" if signal else "false"
                )
        self.dev.setDevCfg(newCfg)

    def setWifiSniff(self, signal):
        newCfg = {
                    'wifi-sniff-enable': "true" if signal else "false"
                }
        self.dev.setDevCfg(newCfg)

    def setVideoBkp(self, signal):
        newCfg = dict(
                   videoBackup = "true" if signal else "false"
                )
        self.dev.setDevCfg(newCfg)

    def setWifiAccess(self, seqNO, SSID, KEY):
        newCfg = {"WifiAccess":{
                        seqNO: {
                                "SSID": SSID,
                                "key": KEY,
                                "hiddenSSID": "no"
                            },
                        "AccessList":[
                                "1",
                                "2",
                                "3",
                                "4"
                            ]
                    }
                }
        self.dev.setDevCfg(newCfg)



