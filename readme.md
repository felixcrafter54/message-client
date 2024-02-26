# Message Client

The Message Client is a Windows application that provides a user-friendly graphical interface for receiving and displaying messages via Windows toast notifications and console logs. This client also serves as an HTTP server, allowing users to send messages, execute commands, and press hotkeys remotely.

## Installation

1. Download the MessageClient.exe file from the [releases section](https://github.com/felixcrafter54/message-client/releases) of this repository.
2. Double-click on the MessageClient.exe file to run the application.

## Usage

1. The application will display a GUI where you can enter your login credentials (username and password).
2. Optionally, check the "Autostart" box if you want the client to start automatically when your system boots.
3. Click the "Save Credentials" button to save the entered credentials.
4. The client will now set up an HTTP server on port 8080 and wait for incoming messages and commands.

## Sending Messages and Commands

To send messages, commands, and hotkeys to the client, you can use HTTP POST requests with basic authentication. The username should match the one entered in the GUI, and the password should be the hashed version of the password (SHA-256).

### Examples

Sending a message:

```http
POST http://localhost:8080/
Authorization: Basic BASE64_ENCODED_USERNAME_AND_PASSWORD

{
  "type": "message",
  "payload": "Hello, this is a test message!"
}
```

---
Sending a command:

```http
POST http://localhost:8080/
Authorization: Basic BASE64_ENCODED_USERNAME_AND_PASSWORD

{
  "type": "command",
  "payload": "dir"
}
```

---
Sending a hotkey:

```http
POST http://localhost:8080/
Authorization: Basic BASE64_ENCODED_USERNAME_AND_PASSWORD

{
  "type": "hotkey",
  "payload": "CTRL+SHIFT+P"
}
```

Possible Hotkeys: [List of hotkeys](keylist.txt)

---
Retrieving Process Information:

```http
POST http://localhost:8080/
Authorization: Basic BASE64_ENCODED_USERNAME_AND_PASSWORD

{
  "type": "process",
  "payload": "chrome"
}
```

---
Execute a system function:

```http
POST http://localhost:8080/
Authorization: Basic BASE64_ENCODED_USERNAME_AND_PASSWORD

{
  "type": "systemfunction",
  "payload": "lock"
}
```

Possible functions: [standby, lock, shutdown, reboot]

## Responses from the client

* message, command and hotkey:
    ```http
    HTTP/1.1 200 OK
    Content-Type: text/plain
    
    Message Received
    ```

* process:
    ```http
    HTTP/1.1 200 OK
    Content-Type: application/json
    
    {"process": "opera", "status": false}
    ```

* systemfunction:
    ```http
    HTTP/1.1 200 OK
    Content-Type: text/plain
    
    Systemfunction executing
    ```    

## System Tray Icon

The application provides a system tray icon that allows you to hide/show the GUI. When hidden, the application will continue running in the background and display toast notifications for incoming messages.

## Uninstall
To uninstall the Message Client, simply delete the MessageClient.exe file from your system.

## Acknowledgments
The Message Client was inspired by the need for a simple messaging and command execution platform and is built on various Python libraries.

## License
This project is licensed under the GPL-3.0 License.

Feel free to contribute or report issues if you find any improvements or bugs! Happy messaging!
