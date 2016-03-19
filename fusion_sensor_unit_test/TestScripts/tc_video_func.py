#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test whether the video file can be generated.
"""

import unittest
import sys
import time

sys.path.append('../TestLibs/')
from device import Device
from gs import GSMonitor
from config import ConfigManager

TEST_DEVICE = "8600176"

class TC_VIDEO_FUNC(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.dev = Device(TEST_DEVICE)
        self.mGS = GSMonitor(self.dev)
        self.mCfg = ConfigManager(self.dev)

    @classmethod
    def tearDownClass(self):
        self.mCfg.close()
        self.mGS.close()
        self.dev.close()

    def test_video_generating(self):
        self.assertEqual(self.dev.isFSRunning(), True, "Fusion Sensor is not running.")
        self.mCfg.setVideoMode()
        time.sleep(20*60)
        self.assertTrue(self.dev.isNewDataOnDevice("video") or self.mGS.isNewVideoUploaded(),
                    "Failed to find new video data"
                )
        print("Video generating is approved")
