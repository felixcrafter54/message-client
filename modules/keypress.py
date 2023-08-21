import pyautogui

key_mapping = {
    "RCTRL": "ctrlright",
    "RALT": "altright",
    "RSHIFT": "shiftright",
    "RWIN": "winright",
    "ENT": "enter",
    "DEL": "delete",
    "INS": "insert",
    "VOLUP": "volumeup",
    "VOLDN": "volumedown",
    "MUTE": "volumemute",
    "NEXT": "nexttrack",
    "PREV": "prevtrack",
    "PLAY": "playpause",
    "STOP": "stop",
    "BACK": "browserback",
    "NUMP": "numpad",
    "NUMS": "numlock",
    "NUMD": "numdivide",
    "NUM*": "nummultiply",
    "NUMM": "numminus",
    "NUML": "numlock",
    "CAPS": "capslock",
    "PGDN": "pagedown",
    "PGUP": "pageup",
    "SCRL": "scrolllock",
    "PRNTSCR": "printscreen"
}

# Funktion, um den Eingabestring in eine Liste von Tasten umzuwandeln
def convert_to_key_list(input_string):
    keys = input_string.split("+")
    converted_keys = []
    for key in keys:
        if key in key_mapping:
            converted_keys.append(key_mapping[key])
        else:
            converted_keys.append(key)
    return converted_keys

def press_hotkey(keys):
    key_list = convert_to_key_list(keys)
    pyautogui.hotkey(key_list)