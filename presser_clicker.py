import pyautogui
import keyboard
import time
import threading

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
        self.toggleEventListener: callable[[bool], None] = None

    
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
        self.keys.append(KeyData(device, key, KeyData.HOLD_TYPE))
    

    def addClickKey(self, device, key, interval):
        self.keys.append(KeyData(device, key, KeyData.CLICK_TYPE, interval))

    
    def removeKey(self, device, key):
        self.keys = [x for x in self.keys if x.device != device or x.key != key]

    
    def startListening(self):
        self.listening = True
        threading.Thread(target=self.__listenToggleKey, daemon=True).start()

    
    def stopListening(self):
        self.listening = False
        self.toggled = False

    
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
