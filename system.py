import os
import psutil

def increase_current_process_priority():
    process = psutil.Process(os.getpid())
    process.nice(psutil.REALTIME_PRIORITY_CLASS)

if __name__ == "__main__":
    increase_current_process_priority()