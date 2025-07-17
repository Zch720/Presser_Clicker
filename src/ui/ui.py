import dearpygui.dearpygui as dpg
from presser_clicker import PresserClicker
from ui.font_manager import FontManager
from ui.toggle_key_panel import ToggleKeyPanel
from ui.keys_panel import KeysPanel

class ParserClickerUI:
    def __init__(self, controller: PresserClicker):
        self.controller: PresserClicker = controller
        self.fontManager: FontManager = FontManager()


    def run(self):
        dpg.create_context()
        dpg.create_viewport(title='Presser, Clicker', width=500, height=350, small_icon="./resources/icon_small.ico", large_icon="./resources/icon_large.ico")
        self.fontManager.init()
        dpg.bind_font(self.fontManager.DefaultFont)

        with dpg.window(label='Presser, Clicker', tag='main/window'):
            ToggleKeyPanel(self.fontManager, self.controller).render()
            dpg.add_separator()
            KeysPanel(self.fontManager, self.controller).render()

        dpg.set_primary_window('main/window', True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
