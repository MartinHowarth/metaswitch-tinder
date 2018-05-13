import time


def wait_for(condition, timeout):
    start_time = time.time()
    while time.time() < start_time + timeout:
        if condition():
            return True
        time.sleep(0.1)
