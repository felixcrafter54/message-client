import ctypes
import os
import threading

def execute_systemfunction(function):
    if function == "standby":
        run_thread_delayed(lambda: ctypes.windll.powrprof.SetSuspendState(False, False, False))
    elif function == "lock":
        run_thread_delayed(lambda: ctypes.windll.user32.LockWorkStation())
    elif function == "shutdown":
        run_thread_delayed(lambda: os.system("shutdown /s /t 0"))
    elif function == "reboot":
        run_thread_delayed(lambda: os.system("shutdown /r /t 0"))
    else:
        return "Unknown Systemfunction: " + function
    return "Systemfunction executing"

def run_thread_delayed(task, delay = 1):
    threading.Timer(delay, task).start()