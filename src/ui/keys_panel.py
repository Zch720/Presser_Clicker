import dearpygui.dearpygui as dpg
from presser_clicker import PresserClicker
from ui.font_manager import FontManager
from ui.tag_manager import TagManager as TMng
from ui.dpg_component import DpgComponent
from ui.key_table import KeyTable
from ui.add_key_panel import AddKeyPanel

class KeysPanel(DpgComponent):
    def __init__(self, fontManager: FontManager, controller: PresserClicker):
        self.fontManager: FontManager = fontManager
        self.controller: PresserClicker = controller
    
    def render(self):
        with dpg.group():
            dpg.add_text('Keys', tag=TMng.KeysPanelTags.AddKeyLabel)
            dpg.bind_item_font(TMng.KeysPanelTags.AddKeyLabel, self.fontManager.DefaultBoldFont)

            keyTableComp = KeyTable(self.fontManager, self.controller)
            keyTableComp.render()

            AddKeyPanel(self.fontManager, self.controller, keyTableComp).render()
