import dearpygui.dearpygui as dpg
from presser_clicker import PresserClicker, KeyDataInvalid, KeyAdded
from ui.font_manager import FontManager
from ui.tag_manager import TagManager as TMng
from ui.dpg_component import DpgComponent
from ui.message_box import MessageBox
from ui.key_table import KeyTable

class AddKeyPanel(DpgComponent):
    def __init__(self, fontManager: FontManager, messageBoxComp: MessageBox, controller: PresserClicker, keyTableComp: KeyTable):
        self.fontManager: FontManager = fontManager
        self.messageBoxComp: MessageBox = messageBoxComp
        self.controller: PresserClicker = controller
        self.keyTableComp: KeyTable = keyTableComp


    def onAddKeyComboChanged(self, sender, value):
        if value == 'keyboard':
            dpg.hide_item(TMng.AddKeyPanelTags.MouseBtnCombo)
            dpg.show_item(TMng.AddKeyPanelTags.AddedKey)

            dpg.configure_item(TMng.AddKeyPanelTags.AddedKey, label='not set')
        else:
            dpg.show_item(TMng.AddKeyPanelTags.MouseBtnCombo)
            dpg.hide_item(TMng.AddKeyPanelTags.AddedKey)
            
            dpg.set_value(TMng.AddKeyPanelTags.MouseBtnCombo, '')


    def onAddedKeySetting(self):
        dpg.configure_item(TMng.AddKeyPanelTags.AddedKey, label='press the key')
        key = self.controller.getKey()
        dpg.configure_item(TMng.AddKeyPanelTags.AddedKey, label=key)


    def onKeyActionComboChanged(self, sender, value):
        if value == 'click':
            dpg.show_item(TMng.AddKeyPanelTags.KeyClickInterval)
            dpg.hide_item(TMng.AddKeyPanelTags.AddBtnSpacer)
        else:
            dpg.hide_item(TMng.AddKeyPanelTags.KeyClickInterval)
            dpg.show_item(TMng.AddKeyPanelTags.AddBtnSpacer)


    def onAddKeyBtnClicked(self):
        try:
            device = dpg.get_value(TMng.AddKeyPanelTags.AddedKeyDeviceCombo)
            key = ''
            if device == 'keyboard':
                key = dpg.get_item_configuration(TMng.AddKeyPanelTags.AddedKey)['label']
                key = '' if key == 'not set' else key
            else:
                key = dpg.get_value(TMng.AddKeyPanelTags.MouseBtnCombo)

            if dpg.get_value(TMng.AddKeyPanelTags.AddedKeyActionCombo) == 'hold':
                self.controller.addHoldKey(device, key)
            else:
                interval = dpg.get_value(TMng.AddKeyPanelTags.KeyClickInterval)
                self.controller.addClickKey(device, key, interval)

            self.keyTableComp.addLastKeyDataToTable()
        except KeyDataInvalid:
            self.messageBoxComp.show('Key data is invalid')
        except KeyAdded:
            self.messageBoxComp.show('This key is already added')

    def render(self):
        with dpg.group(horizontal=True):
            dpg.add_combo(default_value='keyboard', items=['keyboard', 'mouse'], tag=TMng.AddKeyPanelTags.AddedKeyDeviceCombo, width=100, callback=self.onAddKeyComboChanged)
            
            # mouse btn setting
            dpg.add_combo(items=['left', 'right'], tag=TMng.AddKeyPanelTags.MouseBtnCombo, width=100)
            dpg.hide_item(TMng.AddKeyPanelTags.MouseBtnCombo)

            #keyboard key setting
            dpg.add_button(label='not set', tag=TMng.AddKeyPanelTags.AddedKey, width=100, callback=self.onAddedKeySetting)

            dpg.add_combo(default_value='hold', items=['hold', 'click'], tag=TMng.AddKeyPanelTags.AddedKeyActionCombo, width=100, callback=self.onKeyActionComboChanged)

            dpg.add_input_double(default_value=0.01, tag=TMng.AddKeyPanelTags.KeyClickInterval, width=100, min_value=0.01, min_clamped=True, step=0.01, format='%.2f')
            dpg.hide_item(TMng.AddKeyPanelTags.KeyClickInterval)

            dpg.add_spacer(tag=TMng.AddKeyPanelTags.AddBtnSpacer, width=100)

            dpg.add_button(label='Add', tag=TMng.AddKeyPanelTags.AddKeyBtn, callback=self.onAddKeyBtnClicked)
