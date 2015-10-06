
class CpuLoadException(Exception):
    '''A user-defined exception class.'''
    def __init__(self, cpu_load_exception_count):
        Exception.__init__(self)
        self.cpu_load_exception_count = cpu_load_exception_count
        
class RebootException(Exception):
    '''A user-defined exception class.'''
    def __init__(self, reboot_count):
        Exception.__init__(self)
        self.reboot_count = reboot_count
        
class MemoryLeakException(Exception):
    '''A user-defined exception class.'''
    def __init__(self, memory_used_exception_count):
        Exception.__init__(self)
        self.memory_used_exception_count = memory_used_exception_count
        
class DataHoleException(Exception):
    '''A user-defined exception class.'''
    def __init__(self, data_hole_count):
        Exception.__init__(self)
        self.data_hole_count = data_hole_count

class DiskRemainException(Exception):
    '''A user-defined exception class.'''
    def __init__(self, disk_remain_exception_count):
        Exception.__init__(self)
        self.disk_remain_exception_count = disk_remain_exception_count

class SoftwareUpdateException(Exception):
    '''A user-defined exception class.'''
    def __init__(self, server_version, device_version):
        Exception.__init__(self)
        self.server_version = server_version
        self.device_version = device_version         
                

                        