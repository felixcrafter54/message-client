from tkinter import messagebox
import pythoncom
import win32com.client
import os
import sys

exe_path = sys.argv[0]
autostart_folder = os.path.join(os.getenv('APPDATA'),r'Microsoft\Windows\Start Menu\Programs\Startup')

def create_shortcut(target_path, shortcut_path, description="", icon_path="", working_directory=""):
    try:
        shortcut = win32com.client.Dispatch("WScript.Shell").CreateShortcut(shortcut_path)
        shortcut.TargetPath = target_path
        shortcut.Description = description
        shortcut.IconLocation = icon_path
        shortcut.WorkingDirectory = working_directory
        shortcut.Save()
        messagebox.showinfo("Success", f"Added '{target_path}' to Autostart")
    except pythoncom.com_error as e:
        messagebox.showinfo("Error", f"Can not add to Autostart: {str(e)}")
