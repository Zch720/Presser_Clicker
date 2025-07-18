import pyautogui
import keyboard
import time
import threading
import util
from typing import Callable

class KeyDataInvalid(Exception):
    pass


class KeyAdded(Exception):
    pass


class KeyData:
    HOLD_TYPE = 'hold'
    CLICK_TYPE = 'click'

    def __init__(self, device, key, type, interval = -1):
        self.device = device
        self.key = key
        self.type = type
        self.interval = interval


class PresserClicker:
    def __init__(self):
        self.toggleKey = None
        self.keys: list[KeyData] = []
        self.listening = False
        self.toggled = False
        self.toggleEventListener: Callable[[bool], None] = None

    
    def getKey(self) -> str:
        key = ''
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name
                break
        return key

    
    def readToggleKey(self):
        key = self.getKey()
        if key == 'esc':
            self.toggleKey = None
        else:
            self.toggleKey = key

    
    def addHoldKey(self, device, key):
        data = KeyData(device, key, KeyData.HOLD_TYPE)
        self.__checkKeyDataValid(data)
        self.keys.append(data)
    

    def addClickKey(self, device, key, interval):
        data = KeyData(device, key, KeyData.CLICK_TYPE, interval)
        self.__checkKeyDataValid(data)
        self.keys.append(data)
    
    
    def getLastedKeyData(self) -> KeyData:
        return self.keys[-1]
    

    def moveKeyUp(self, device, key):
        index = util.getIndexInList(self.keys, lambda data: data.device == device and data.key == key)
        if index == 0:
            return
        util.moveListItemIndex(self.keys, index, index - 1)
    

    def moveKeyDown(self, device, key):
        index = util.getIndexInList(self.keys, lambda data: data.device == device and data.key == key)
        if index == len(self.keys) - 1:
            return
        util.moveListItemIndex(self.keys, index, index + 1)

    
    def removeKey(self, device, key):
        self.keys = [x for x in self.keys if x.device != device or x.key != key]

    
    def readyToListen(self) -> bool:
        return self.toggleKey != None

    
    def startListening(self):
        self.listening = True
        threading.Thread(target=self.__listenToggleKey, daemon=True).start()

    
    def stopListening(self):
        self.listening = False
        self.toggled = False

    
    def __checkKeyDataValid(self, keyData: KeyData):
        if keyData.key == '':
            raise KeyDataInvalid()
        if keyData.type == KeyData.CLICK_TYPE and keyData.interval < 0.01:
            raise KeyDataInvalid()

        for key in self.keys:
            if key.device == keyData.device and key.key == keyData.key:
                raise KeyAdded()

    
    def __listenToggleKey(self):
        while self.listening:
            if keyboard.is_pressed(self.toggleKey):
                self.__toggle()

                while keyboard.is_pressed(self.toggleKey):
                    time.sleep(0.05)
            time.sleep(0.01)
    

    def __toggle(self):
        if self.toggled:
            for key in self.keys:
                if key.type == KeyData.HOLD_TYPE:
                    if key.device == 'keyboard':
                        keyboard.release(key.key)
                    else:
                        pyautogui.mouseUp(button=key.key)
            self.toggled = False
        else:
            self.toggled = True
            for key in self.keys:
                if key.type == KeyData.HOLD_TYPE:
                    if key.device == 'keyboard':
                        keyboard.press(key.key)
                    else:
                        pyautogui.mouseDown(button=key.key)
                else:
                    threading.Thread(target=self.__click, args=[key], daemon=True).start()
                    
        if self.toggleEventListener != None:
            self.toggleEventListener(self.toggled)


    def __click(self, key: KeyData):
        if key.device == 'keyboard':
            while self.toggled:
                keyboard.press_and_release(key.key)
                time.sleep(key.interval)
        else:
            while self.toggled:
                pyautogui.click(button=key.key)
                time.sleep(key.interval)
