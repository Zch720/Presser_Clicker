import dearpygui.dearpygui as dpg
from presser_clicker import PresserClicker
from ui.font_manager import FontManager
from ui.tag_manager import TagManager as TMng
from ui.dpg_component import DpgComponent
from ui.message_box import MessageBox
from ui.key_table import KeyTable
from ui.add_key_panel import AddKeyPanel

class KeysPanel(DpgComponent):
    def __init__(self, fontManager: FontManager, messageBoxComp: MessageBox, controller: PresserClicker):
        self.fontManager: FontManager = fontManager
        self.messageBoxComp: MessageBox = messageBoxComp
        self.controller: PresserClicker = controller
    
    def render(self):
        with dpg.group():
            keyTableComp = KeyTable(self.fontManager, self.messageBoxComp, self.controller)

            with dpg.group(horizontal=True):
                dpg.add_text('Keys', tag=TMng.KeysPanelTags.AddKeyLabel)
                keyTableComp.panel.render()
            dpg.bind_item_font(TMng.KeysPanelTags.AddKeyLabel, self.fontManager.DefaultBoldFont)

            keyTableComp.render()

            AddKeyPanel(self.fontManager, self.messageBoxComp, self.controller, keyTableComp).render()
