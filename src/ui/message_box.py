import dearpygui.dearpygui as dpg
from ui.dpg_component import DpgComponent

class MessageBox(DpgComponent):
    def __init__(self, message):
        self.message = message

    def render(self):
        with dpg.popup(dpg.last_item(), modal=True, min_size=(0, 0)) as popup:
            dpg.add_text(self.message)
        dpg.show_item(popup)
