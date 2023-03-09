import sys
import traceback

debug_file = 'debug.txt'

def setDebug(self):
    self.no_debug = False

    if '--no-debug' in sys.argv:
        self.no_debug = True

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