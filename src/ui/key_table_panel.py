import dearpygui.dearpygui as dpg
import util
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


    def onKeyTableRowMoveUpBtnClicked(self):
        if self.selectableId != 0:
            rowId, device, key = self.__getSelectedRowData()
            self.controller.moveKeyUp(device, key)
            
            tableChildren = dpg.get_item_children(TMng.KeyTableTags.KeyTable)
            rowIdIndex = util.getIndexInList(tableChildren[1], lambda row: row == rowId)
            if rowIdIndex != 0:
                reorderedRow: list[int] = tableChildren[1]
                util.moveListItemIndex(reorderedRow, rowIdIndex, rowIdIndex - 1)
                dpg.reorder_items(TMng.KeyTableTags.KeyTable, 1, reorderedRow)


    def onKeyTableRowMoveDownBtnClicked(self):
        if self.selectableId != 0:
            rowId, device, key = self.__getSelectedRowData()
            self.controller.moveKeyDown(device, key)
            
            tableChildren = dpg.get_item_children(TMng.KeyTableTags.KeyTable)
            rowIdIndex = util.getIndexInList(tableChildren[1], lambda row: row == rowId)
            if rowIdIndex != len(tableChildren[1]) - 1:
                reorderedRow: list[int] = tableChildren[1]
                util.moveListItemIndex(reorderedRow, rowIdIndex, rowIdIndex + 1)
                dpg.reorder_items(TMng.KeyTableTags.KeyTable, 1, reorderedRow)
    

    def onKeyTableRowRemoveBtnClicked(self):
        if self.selectableId != 0:
            rowId, device, key = self.__getSelectedRowData()
            self.controller.removeKey(device, key)
            dpg.delete_item(rowId)
            self.selectableId = 0

    
    def render(self):
        with dpg.group(horizontal=True, tag=TMng.KeyTablePanelTags.KeyTablePanel):
            dpg.add_image_button(TMng.TextureTags.Up, label='Move up', width=16, height=16, tag=TMng.KeyTablePanelTags.MoveRowUpBtn, callback=self.onKeyTableRowMoveUpBtnClicked)
            dpg.add_image_button(TMng.TextureTags.Down, label='Move down', width=16, height=16, tag=TMng.KeyTablePanelTags.MoveRowDownBtn, callback=self.onKeyTableRowMoveDownBtnClicked)
            dpg.add_image_button(TMng.TextureTags.Delete, label='Delete', width=16, height=16, tag=TMng.KeyTablePanelTags.DeleteRowBtn, callback=self.onKeyTableRowRemoveBtnClicked)

    
    def __getSelectedRowData(self) -> tuple[int, str, str]:
        rowId = dpg.get_item_parent(self.selectableId)
        device = dpg.get_item_configuration(dpg.get_item_children(rowId)[1][0])['label']
        key = dpg.get_item_configuration(dpg.get_item_children(rowId)[1][1])['label']
        return rowId, device, key
