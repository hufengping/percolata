#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test whether the loi file can be generated.
"""

import unittest
import sys
import time

sys.path.append('../TestLibs/')
from device import Device
from gs import GSMonitor
from config import ConfigManager

TEST_DEVICE = "8600176"

class TC_LOI_FUNC(unittest.TestCase):
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

    def test_loi_generating(self):
        self.assertEqual(self.dev.isFSRunning(), True, "Fusion Sensor is not running.")
        self.mCfg.setLoiMode()
        time.sleep(8*60)
        self.assertTrue(self.dev.isNewDataOnDevice("loi") or self.mGS.isNewLoiUploaded(),
                    "Failed to find new loi data"
                )
        print("Loi generating is approved")
