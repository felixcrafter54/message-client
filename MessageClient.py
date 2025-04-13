import tkinter as tk
from tkinter import messagebox, BooleanVar
from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import json
import threading
from typing import Any
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import sys
import os
from modules.keypress import press_hotkey
from modules.functions import resource_path, hash_password
from modules.toast_messages import show_toast
from modules.autostart import create_shortcut
from modules.command import execute_command, execute_command_detached
from modules.processes import check_process_running
from modules.systemfunction import execute_systemfunction

version = "v2.0"

config = None

# load hashed config
def load_config():
    global config
    if config == None:
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
            return config
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    else:
        return config

# save hasched config
def save_config(new_config):
    global config
    if isinstance(new_config, str):
        new_config = json.loads(new_config)
    config = new_config
    with open("config.json", "w") as file:
        json.dump(config, file)

# list for massages
last_messages = []

console_output = None

username_entry = None
password_entry = None

window = None

autostart_var = None

tray_icon = None

isshown = False

config_loaded = load_config()

exe_path = sys.argv[0]
autostart_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')

def autostart(Flag):
    data = load_config()
    shortcut_name = "MessageClient.lnk"
    shortcut_path = os.path.join(autostart_folder, shortcut_name)
    if Flag:
        data['autostart'] = True
        current_directory = os.getcwd()
        description = "Start Message-Client on Startup"
        icon_path = resource_path("app_icon.ico")
        working_directory = current_directory
        create_shortcut(exe_path, shortcut_path, description, icon_path, working_directory)
    else:
        data['autostart'] = False
        try:
            # delete shortcut
            os.remove(shortcut_path)
            messagebox.showinfo("Success", f"Removed'{exe_path}' from Autostart")
        except FileNotFoundError:
            messagebox.showinfo("Error", "Shortcut not found")
        except PermissionError:
            messagebox.showinfo("Error", "No Permission to delete Autostart Shortcut")
        except Exception as e:
            messagebox.showinfo("Error", f"Error: {str(e)}")
    save_config(data)

#add incomming messages in list
def redirect_stdout(text):
    global last_messages, console_output, isshown  # Use the global keyword to access the global variable
    last_messages.append(text)
    # only last 10 messages
    last_messages = last_messages[-10:]
    
    if isshown:
        console_output.delete(1.0, tk.END)
        console_output.insert(tk.END, "\n".join(last_messages))
        console_output.see(tk.END)

# Class for the HTTP-Server
class RequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format: str, *args: Any) -> None:
        return None

    def do_AUTHHEAD(self,response):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Auth required"')
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

    def do_RESPONSE(self,response,option = 0):
        if option == 1:
            ct = 'application/json'
        else:
            ct = 'text/plain'    
        self.send_response(200)
        self.send_header("Content-type", ct)
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response) 

    def do_POST(self):
        auth_header = self.headers.get("Authorization")
        if not auth_header or "Basic" not in auth_header:
            response = b"Unauthorized"
            self.do_AUTHHEAD(response)
            self.wfile.write(response)
        else:
            # extract user and password from auth-header
            auth_decoded = auth_header.split(" ")[-1].strip()
            auth_decoded = base64.b64decode(auth_decoded).decode()
            username, password = auth_decoded.split(":")
            loaded_config = load_config()
            if loaded_config and username == loaded_config["username"] and hash_password(password) == loaded_config["hashed_password"]:
                # authorized
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length).decode("utf-8")
                payload = json.loads(post_data).get("payload")
                type = json.loads(post_data).get("type")
                if type == "message":
                    show_toast(payload)
                    redirect_stdout("message: " + payload)
                    response = b"Message received"
                    self.do_RESPONSE(response)
                elif type == "command":
                    output = execute_command(payload)
                    redirect_stdout("command: " + payload)
                    response = bytes(output, "utf-8")
                    self.do_RESPONSE(response)
                elif type == "command_detached":
                    output = execute_command_detached(payload)
                    redirect_stdout("command_detached: " + payload)
                    response = bytes(output, "utf-8")
                    self.do_RESPONSE(response)
                elif type == "hotkey":
                    press_hotkey(payload)
                    redirect_stdout("hotkey: " + payload)
                    response = b"Hotkey pressed"
                    self.do_RESPONSE(response)
                elif type == "process":
                    output = check_process_running(payload)
                    redirect_stdout("process: " + payload)
                    response = bytes(output, "utf-8")
                    self.do_RESPONSE(response,1) # e.g. {"process": "opera", "status": false}
                elif type == "systemfunction":
                    output = execute_systemfunction(payload)
                    redirect_stdout("Systemfunction: " + payload)
                    response = bytes(output, "utf-8")
                    self.do_RESPONSE(response)
                else:
                    response = b"incorrect Message type"
                    self.do_RESPONSE(response)    
            else:
                response = b"Unauthorized"
                self.do_AUTHHEAD(response)
                self.wfile.write(response)


def start_http_server():
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    #print("HTTP server is running...")
    httpd.serve_forever()

# Main function for GUI
def create_gui():
    global console_output, username_entry, password_entry, window, config_loaded, autostart_var, isshown

    def quit_all():
        window.destroy()

    def quit_window(icon):
        icon.stop()
        window.destroy()

    def show_window(icon):
        global isshown
        icon.stop()
        window.after(0, window.deiconify)
        # delete Textbox and show last messages
        console_output.delete(1.0, tk.END)
        console_output.insert(tk.END, "\n".join(last_messages))
        console_output.see(tk.END)
        isshown = True

    # Hide the window and show on the system taskbar
    def hide_window():
        global isshown, tray_icon
        isshown = False
        window.withdraw()
        image = Image.open(resource_path("app_icon.ico"))
        menu = (
            item('Quit', quit_window),
            item('Show', show_window)
        )
        tray_icon = pystray.Icon("name", image, "Message-Client", menu)
        tray_icon.run()

    def save_credentials():
        new_config = {
            "username": username_entry.get(),
            "hashed_password": hash_password(password_entry.get()),
            "autostart": load_config()['autostart'] if load_config() and 'autostart' in load_config() else False
        }
        save_config(new_config)
        messagebox.showinfo("Success", "Credentials saved successfully.")

    window = tk.Tk()

    window.title("Message-Client")
    icon_image = Image.open(resource_path("app_icon.ico"))
    photo = ImageTk.PhotoImage(icon_image)
    window.wm_iconphoto(False, photo)

    # GUI-Elements
    tk.Label(window, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(window, name = "username")
    username_entry.grid(row=1, column=0)

    autostart_var = BooleanVar(window, value=False)
    if config_loaded is not None and "autostart" in config_loaded:
        autostart_var.set(config_loaded["autostart"])

    tk.Label(window, text=version).grid(row=0, column=2)

    tk.Checkbutton(window, text="Autostart", variable=autostart_var, onvalue=True, offvalue=False, command=lambda: autostart(autostart_var.get())).grid(row=2, column=2)

    tk.Label(window, text="Password:").grid(row=2, column=0)
    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=3, column=0)

    tk.Button(window, text="Save Credentials", command=save_credentials).grid(row=4, column=0, pady=5)

    tk.Button(window, text="Quit", command=quit_all).grid(row=4, column=2)

    console_output = tk.Text(window, wrap=tk.WORD, width=50, height=10)
    console_output.grid(row=5, column=0, columnspan=3)

    # Start HTTP-Server in seperate Tread
    http_server_thread = threading.Thread(target=start_http_server, daemon=True)
    http_server_thread.start()

    window.protocol('WM_DELETE_WINDOW', hide_window)

    if config_loaded != None:
        hide_window()
    else:
        messagebox.showinfo("Info", "Please enter credentials.")
        isshown = True

    window.mainloop()


if __name__ == "__main__":
    create_gui()