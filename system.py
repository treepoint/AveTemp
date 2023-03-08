import os
import psutil
import logger

@logger.log
def increase_current_process_priority(self):
    process = psutil.Process(os.getpid())
    process.nice(psutil.REALTIME_PRIORITY_CLASS)

if __name__ == "__main__":
    increase_current_process_priority()