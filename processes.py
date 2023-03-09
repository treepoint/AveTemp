import psutil
import logger

@logger.log
def alreadyRunning(self):
    process_name = self.config.getName()
    count = 0

    for proc in psutil.process_iter():
        if process_name in proc.name():
            count += 1
        if count >= 3:
            return True

    return False

if __name__ == "__main__":
    alreadyRunning()