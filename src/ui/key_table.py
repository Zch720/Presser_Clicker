import dearpygui.dearpygui as dpg
from presser_clicker import PresserClicker
from ui.font_manager import FontManager
from ui.tag_manager import TagManager as TMng
from ui.dpg_component import DpgComponent
from ui.message_box import MessageBox
from ui.key_table_panel import KeyTablePanel

class KeyTable(DpgComponent):
    def __init__(self, fontManager: FontManager, messageBoxComp: MessageBox, controller: PresserClicker):
        self.fontManager: FontManager = fontManager
        self.messageBoxComp: MessageBox = messageBoxComp
        self.controller: PresserClicker = controller
        self.panel: KeyTablePanel = KeyTablePanel(fontManager, messageBoxComp, controller)

    
    def onKeyTableRowSelected(self, sender, app_data):
        if app_data:
            if self.panel.selectableId != 0:
                dpg.configure_item(self.panel.selectableId, default_value=False)
            self.panel.selectableId = sender
        else:
            self.panel.selectableId = 0


    def addLastKeyDataToTable(self):
        lastKeyData = self.controller.getLastedKeyData()
        with dpg.table_row(parent=TMng.KeyTableTags.KeyTable):
            dpg.add_selectable(label=lastKeyData.device, span_columns=True, callback=self.onKeyTableRowSelected)
            dpg.add_selectable(label=lastKeyData.key, span_columns=True, callback=self.onKeyTableRowSelected)
            dpg.add_selectable(label=lastKeyData.type, span_columns=True, callback=self.onKeyTableRowSelected)
            if lastKeyData.interval == -1:
                dpg.add_selectable(label='-', span_columns=True, callback=self.onKeyTableRowSelected)
            else:
                dpg.add_selectable(label=f"{lastKeyData.interval:.2f}", span_columns=True, callback=self.onKeyTableRowSelected)

    
    def render(self):
        with dpg.table(tag=TMng.KeyTableTags.KeyTable, width=424, indent=100, borders_outerH=True, borders_innerH=True):
            dpg.add_table_column(label='Device', width_fixed=True, init_width_or_weight=108)
            dpg.add_table_column(label='Key', width_fixed=True, init_width_or_weight=108)
            dpg.add_table_column(label='Action', width_fixed=True, init_width_or_weight=108)
            dpg.add_table_column(label='Interval', width_fixed=True, init_width_or_weight=100)
