import ctypes
import os

def execute_systemfunction(function):
    if function == "standby":
        ctypes.windll.powrprof.SetSuspendState(False, False, False)
    elif function == "lock":
        ctypes.windll.user32.LockWorkStation()
    elif function == "shutdown":
        os.system("shutdown /s /t 0")
    elif function == "reboot":
        os.system("shutdown /r /t 0")
    else:
        return "Unknown Systemfunction: " + function
    return "Systemfunction executed"