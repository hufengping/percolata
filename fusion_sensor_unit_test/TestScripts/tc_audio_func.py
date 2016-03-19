#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test whether the audio file can be generated.
"""

import unittest
import sys
import time

sys.path.append('../TestLibs/')
from device import Device
from gs import GSMonitor
from config import ConfigManager

TEST_DEVICE = "8600176"

class TC_AUDIO_FUNC_001(unittest.TestCase):
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

    def test_audio_generating(self):
        self.assertEqual(self.dev.isFSRunning(), True, "Fusion Sensor is not running.")
        self.mCfg.setTrackingMode()
        self.mCfg.setAudio(True)
        time.sleep(6*60)
        self.assertTrue(self.dev.isNewDataOnDevice("audio") or self.mGS.isNewAudioUploaded(),
                    "Failed to find new audio data"
                )
        print("Audio generating is approved")
