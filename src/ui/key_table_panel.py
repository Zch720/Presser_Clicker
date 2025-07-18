import dearpygui.dearpygui as dpg
from presser_clicker import PresserClicker
from ui.font_manager import FontManager
from ui.tag_manager import TagManager as TMng
from ui.dpg_component import DpgComponent
from ui.message_box import MessageBox

class KeyTablePanel(DpgComponent):
    def __init__(self, fontManager: FontManager, messageBoxComp: MessageBox, controller: PresserClicker):
        self.fontManager: FontManager = fontManager
        self.messageBoxComp: MessageBox = messageBoxComp
        self.controller: PresserClicker = controller
        self.selectableId = 0
    

    def onKeyTableRowRemoveBtnClicked(self):
        if self.selectableId != 0:
            rowId = dpg.get_item_parent(self.selectableId)
            device = dpg.get_item_configuration(dpg.get_item_children(rowId)[1][0])['label']
            key = dpg.get_item_configuration(dpg.get_item_children(rowId)[1][1])['label']
            self.controller.removeKey(device, key)
            dpg.delete_item(rowId)
            self.selectableId = 0

    
    def render(self):
        dpg.add_image_button(TMng.TextureTags.Delete, label='Delete', width=18, height=18, tag=TMng.KeyTablePanelTags.DeleteRowBtn, callback=self.onKeyTableRowRemoveBtnClicked)
