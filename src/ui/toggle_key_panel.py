import dearpygui.dearpygui as dpg
from presser_clicker import PresserClicker
from ui.font_manager import FontManager
from ui.tag_manager import TagManager as TMng
from ui.dpg_component import DpgComponent

class ToggleKeyPanel(DpgComponent):
    def __init__(self, fontManager: FontManager, controller: PresserClicker):
        self.fontManager: FontManager = fontManager
        self.controller: PresserClicker = controller

        controller.toggleEventListener = self.toggleStateChangeEventListener


    def onToggleKeySetting(self):
        dpg.configure_item(TMng.ToggleKeyPanelTags.ToggleKey, label='press the key')
        self.controller.readToggleKey()
        self.updateToggleKeyText()


    def onStartListenBtnClicked(self):
        if self.controller.listening:
            dpg.configure_item(TMng.ToggleKeyPanelTags.StartListenBtn, label='Start Listen')
            dpg.configure_item(TMng.ToggleKeyPanelTags.ToggleKey, enabled=True)
            dpg.configure_item(TMng.AddKeyPanelTags.AddKeyBtn, enabled=True)
            for row in dpg.get_item_children(TMng.KeyTableTags.KeyTable)[1]:
                dpg.configure_item(dpg.get_item_children(row)[1][4], enabled=True)
            self.controller.stopListening()
        else:
            dpg.configure_item(TMng.ToggleKeyPanelTags.StartListenBtn, label='Stop Listen')
            dpg.configure_item(TMng.ToggleKeyPanelTags.ToggleKey, enabled=False)
            dpg.configure_item(TMng.AddKeyPanelTags.AddKeyBtn, enabled=False)
            for row in dpg.get_item_children(TMng.KeyTableTags.KeyTable)[1]:
                dpg.configure_item(dpg.get_item_children(row)[1][4], enabled=False)
            self.controller.startListening()


    def updateToggleKeyText(self):
        if self.controller.toggleKey == None:
            dpg.configure_item(TMng.ToggleKeyPanelTags.ToggleKey, label='not set')
        else:
            dpg.configure_item(TMng.ToggleKeyPanelTags.ToggleKey, label=self.controller.toggleKey)
    

    def toggleStateChangeEventListener(self, toggled: bool):
        if toggled:
            dpg.set_value(TMng.ToggleKeyPanelTags.ToggleState, 'toggled')
        else:
            dpg.set_value(TMng.ToggleKeyPanelTags.ToggleState, 'untoggled')


    def render(self):
        with dpg.group(horizontal=True):
            dpg.add_text('Toggle key:', tag=TMng.ToggleKeyPanelTags.ToggleKeyLabel)
            dpg.bind_item_font(TMng.ToggleKeyPanelTags.ToggleKeyLabel, self.fontManager.DefaultBoldFont)
            
            dpg.add_button(label='not set', tag=TMng.ToggleKeyPanelTags.ToggleKey, width=100, callback=self.onToggleKeySetting)

            dpg.add_button(label='Start Listen', tag=TMng.ToggleKeyPanelTags.StartListenBtn, width=90, callback=self.onStartListenBtnClicked)
            dpg.add_text('untoggled', tag=TMng.ToggleKeyPanelTags.ToggleState)
