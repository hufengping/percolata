#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test whether the zone-count file can be generated.
"""

import unittest
import sys
import time

sys.path.append('../TestLibs/')
from device import Device
from gs import GSMonitor
from config import ConfigManager

TEST_DEVICE = "8600176"

class TC_ZC_FUNC(unittest.TestCase):
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

    def test_zc_generating(self):
        self.assertEqual(self.dev.isFSRunning(), True, "Fusion Sensor is not running.")
        self.mCfg.setZoneCountMode()
        time.sleep(5*60)
        self.assertTrue(self.dev.isNewDataOnDevice("zone-count") or self.mGS.isNewZoneCountUploaded(),
                    "Failed to find new zone-count data"
                )
        print("ZoneCount generating is approved")
