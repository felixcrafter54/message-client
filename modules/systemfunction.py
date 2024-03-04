import ctypes
import os
import threading
import win32api, win32con

def move_cursor():
    x, y = (0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)

def screen_on():
    move_cursor()

def execute_systemfunction(function):
    if function == "standby":
        run_thread_delayed(lambda: ctypes.windll.powrprof.SetSuspendState(False, False, False))
    elif function == "lock":
        run_thread_delayed(lambda: ctypes.windll.user32.LockWorkStation())
    elif function == "shutdown":
        run_thread_delayed(lambda: os.system("shutdown /s /t 0"))
    elif function == "reboot":
        run_thread_delayed(lambda: os.system("shutdown /r /t 0"))
    elif function == "screen_on":
        #run_thread_delayed(lambda: screen_on())
        screen_on()
    elif function == "screen_off":
        run_thread_delayed(lambda: ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2))
    else:
        return "Unknown Systemfunction: " + function
    return "Systemfunction executing"

def run_thread_delayed(task, delay = 1):
    threading.Timer(delay, task).start()