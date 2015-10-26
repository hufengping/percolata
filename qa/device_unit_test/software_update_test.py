import test_unittest
import json
import os

from unit_test_exception import SoftwareUpdateException
import globals


class SoftwareUpdateTestCase(test_unittest.TestCase):
    """Test Software Update
    
    including fusion-sensor and FusionAdmin
    """
        
    def setUp(self):
        self.server_version = ""
    
    def tearDown(self):
        pass
    
    def testSoftwareUpdate(self):
        print
        print "****Software Update Test Begin****"
                
        print "device version is:", globals.device_version
        
        self.getServerVersion()

        # add test result
        globals.test_result += """
Update:
server_version: %s
device_version: %s
""" % (self.server_version, globals.device_version)

        print "server version is:", self.server_version
        
        print "****Software Update Test End****"
        
        if self.server_version != globals.device_version:
            globals.test_result += "update_condition: Failed\n\n"
            raise SoftwareUpdateException(self.server_version, globals.device_version)
        else:
            globals.test_result += "update_condition: Successful\n\n"
        
    def getServerVersion(self):
        """get fusion-sensor apk version from server"""
        
        # constants.should consist with server config
        # For software update
        SOFTWARE_UPDATE_CONFIG_PATH = "/data/software/"
        ADMIN_UPDATE_CONFIG_FILE = "update-moto-fusion-sensor.json"
        SENSOR_UPDATE_CONFIG_FILE = "update-moto-fusion-admin.json"
        SOFTWARE_UPDATE_LIST = "softwareList"
        VERSION_TAG = "version"
        VERSION_PREFIX = ".v"
        
        # make local directory to consist with server
        local_dir = os.curdir + SOFTWARE_UPDATE_CONFIG_PATH
        if not os.path.exists(local_dir):
            # use makedirs command can create parent directory  
            os.makedirs(local_dir)
        
        local_sensor_file_path = (local_dir + SENSOR_UPDATE_CONFIG_FILE)
        server_sensor_file_path = (SOFTWARE_UPDATE_CONFIG_PATH + 
                                   SENSOR_UPDATE_CONFIG_FILE)
        
        # download command format "scp {user_name}@{server_name}:{file_path} {local_path}"
        download_command = ("scp %s@%s:%s %s" % 
                            (globals.USER_NAME,
                             globals.SERVER_NAME,
                             server_sensor_file_path, 
                             local_sensor_file_path))
        os.system(download_command)     # download config file from remote server
        
        if os.path.exists(local_sensor_file_path):
            # parse json file  
            sensor_file = file(local_sensor_file_path)
            json_obj = json.load(sensor_file)
            #print json_obj
            
            # get version from json object
            # server version format: "version": "08-11-2014.v1.0.0"
            software_name = json_obj[SOFTWARE_UPDATE_LIST][0]
            server_version = json_obj[software_name][VERSION_TAG]
            index = server_version.find(VERSION_PREFIX)
            if index > 0:
                self.server_version = server_version[index+len(VERSION_PREFIX):]
            else:
                self.server_version = server_version
        # else: Can raise a io exception