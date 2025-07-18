import dearpygui.dearpygui as dpg
from ui.tag_manager import TagManager as TMng
from ui.dpg_component import DpgComponent

class MessageBox(DpgComponent):
    def show(self, message):
        dpg.set_value(TMng.MessageBoxTags.Message, message)
        dpg.configure_item(TMng.MessageBoxTags.Popup)
        dpg.show_item(TMng.MessageBoxTags.Popup)
        dpg.set_item_pos(TMng.MessageBoxTags.Popup, self.__calculatePopupPos())


    def hide(self):
        dpg.hide_item(TMng.MessageBoxTags.Popup)


    def render(self):
        with dpg.popup(dpg.last_item(), modal=True, min_size=(0, 0), tag=TMng.MessageBoxTags.Popup):
            dpg.add_text('', tag=TMng.MessageBoxTags.Message)

    
    def __calculatePopupPos(self) -> list[float]:
        dpg.split_frame()
        viewportWidth = dpg.get_viewport_client_width()
        viewportHeight = dpg.get_viewport_client_height()
        [popupWidth, popupHeight] = dpg.get_item_rect_size(TMng.MessageBoxTags.Popup)
        return [(viewportWidth - popupWidth) / 2, (viewportHeight - popupHeight) / 2]

