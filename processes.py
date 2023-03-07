import psutil

def alreadyRunning(self):
    pid = None
    process_name = self.config.getName()

    for proc in psutil.process_iter():
        if process_name in proc.name():
            pid = proc.pid
            break

    if pid == None:
        return False
    else:
        return True

if __name__ == "__main__":
    alreadyRunning()