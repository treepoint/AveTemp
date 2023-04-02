import sys
import traceback
import os.path

debug_file = 'debug.txt'
hardware_dump_file = 'hardware_dump.txt'

def setDebug(self):
    self.no_debug = False

    if '--no-debug' in sys.argv:
        self.no_debug = True

    self.hardware_dump = False

    if '--hardware-dump' in sys.argv:
        self.hardware_dump = True

def truncateHardwareDumpFile(self):
    if os.path.isfile(hardware_dump_file) and self.hardware_dump:
        with open(hardware_dump_file,'r+') as file:
            file.truncate(0)

def dumpHardwareToFile(self, content):
    if self.hardware_dump:
        with open(hardware_dump_file, 'a') as file:
            file.write(f'{ content }\n')

def writeToDebugFile(content):
    with open(debug_file, 'a') as file:
        file.write(content)

def log(input_func):    
    def output_func(*args):
        self = args[0]

        try:
            return input_func(*args)
        except: 
            if self.no_debug:
                traceback.print_exc()
            else:
                trace = traceback.format_exc()
                writeToDebugFile(trace)
    return output_func