import dearpygui.dearpygui as dpg
from presser_clicker import PresserClicker
from ui.font_manager import FontManager
from ui.tag_manager import TagManager as TMng
from ui.dpg_component import DpgComponent

class KeyTable(DpgComponent):
    def __init__(self, fontManager: FontManager, controller: PresserClicker):
        self.fontManager: FontManager = fontManager
        self.controller: PresserClicker = controller
        

    def onKeyTableRowRemoveBtnClicked(self, sender):
        parent = dpg.get_item_parent(sender)
        device = dpg.get_value(dpg.get_item_children(parent)[1][0])
        key = dpg.get_value(dpg.get_item_children(parent)[1][1])
        self.controller.removeKey(device, key)
        dpg.delete_item(parent)


    def addLastKeyDataToTable(self):
        lastKeyData = self.controller.keys[-1]
        with dpg.table_row(parent=TMng.KeyTableTags.KeyTable):
            dpg.add_text(lastKeyData.device)
            dpg.add_text(lastKeyData.key)
            dpg.add_text(lastKeyData.type)
            if (lastKeyData.interval == -1):
                dpg.add_text('-')
            else:
                dpg.add_text(f"{lastKeyData.interval:.2f}")
            dpg.add_button(label='-', width=22, callback=self.onKeyTableRowRemoveBtnClicked)

    
    def render(self):
        with dpg.table(tag=TMng.KeyTableTags.KeyTable, width=455, indent=3, header_row=False, borders_outerH=True, borders_innerH=True):
            dpg.add_table_column(width_fixed=True, init_width_or_weight=100)
            dpg.add_table_column(width_fixed=True, init_width_or_weight=100)
            dpg.add_table_column(width_fixed=True, init_width_or_weight=100)
            dpg.add_table_column(width_fixed=True, init_width_or_weight=100)
            dpg.add_table_column(width_fixed=True, init_width_or_weight=22)
