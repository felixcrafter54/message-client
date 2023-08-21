Message Client

The Message Client is a Windows application that provides a user-friendly graphical interface for receiving and displaying messages via Windows toast notifications and console logs. This client also serves as an HTTP server, allowing users to send messages, execute commands and press hotkeys remotely.

Installation
- Download the MessageClient.exe file from the releases section of this repository.
- Double-click on the MessageClient.exe file to run the application.

Usage
- The application will display a GUI where you can enter your login credentials (username and password).
- Optionally, check the "Autostart" box if you want the client to start automatically when your system boots.
- Click the "Save Credentials" button to save the entered credentials.
- The client will now set up an HTTP server on port 8080 and wait for incoming messages and commands.

Sending Messages and Commands
- To send messages, commands and hotkeys to the client, you can use HTTP POST requests with basic authentication. The username should match the one entered in the GUI, and the password should be the hashed version of the password (SHA-256).

Examples:

Sending a message:


POST http://localhost:8080/
Authorization: Basic BASE64_ENCODED_USERNAME_AND_PASSWORD

{
  "type": "message",
  "payload": "Hello, this is a test message!"
}

Sending a command:


POST http://localhost:8080/
Authorization: Basic BASE64_ENCODED_USERNAME_AND_PASSWORD

{
  "type": "command",
  "payload": "dir"
}

Sending a hotkey:


POST http://localhost:8080/
Authorization: Basic BASE64_ENCODED_USERNAME_AND_PASSWORD

{
  "type": "hotkey",
  "payload": "CTRL+SHIFT+P"
}

Possible Hotkeys: [
    'CTRL', 'RCTRL', 'ALT', 'RALT', 'SHIFT', 'RSHIFT', 'WIN', 'RWIN', 'ESC',
    'ENT', 'DEL', 'INS', 'VOLUP', 'VOLDN', 'MUTE', 'NEXT', 'PREV', 'PLAY',
    'STOP', 'BACK', 'SPACE', 'TAB', 'NUMP', 'NUMS', 'NUMD', 'NUM*', 'NUMM',
    'NUML', 'CAPS', 'END', 'HOME', 'PGDN', 'PGUP', 'SCRL', 'PRNTSCR', 'SLEEP',
    'DOWN', 'UP', 'LEFT', 'RIGHT', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7',
    'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18',
    'F19', 'F20', 'F21', 'F22', 'F23', 'F24', 'NUM0', 'NUM1', 'NUM2', 'NUM3',
    'NUM4', 'NUM5', 'NUM6', 'NUM7', 'NUM8', 'NUM9', '0', '1', '2', '3', '4',
    '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

Format: 'CTRL+RCTRL+ALT' or 'CTRL'

------------------------

System Tray Icon
- The application provides a system tray icon that allows you to hide/show the GUI. When hidden, the application will continue running in the background and display toast notifications for incoming messages.

Uninstall
- To uninstall the Message Client, simply delete the MessageClient.exe file from your system.

Acknowledgments
- The Message Client was inspired by the need for a simple messaging and command execution platform and is built on various Python libraries.

License
- This project is licensed under the MIT License.

Feel free to contribute or report issues if you find any improvements or bugs! Happy messaging!