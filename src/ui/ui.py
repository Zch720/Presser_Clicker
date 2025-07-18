import dearpygui.dearpygui as dpg
import util
from presser_clicker import PresserClicker
from ui.font_manager import FontManager
from ui.tag_manager import TagManager as TMng
from ui.message_box import MessageBox
from ui.toggle_key_panel import ToggleKeyPanel
from ui.keys_panel import KeysPanel

class ParserClickerUI:
    def __init__(self, controller: PresserClicker):
        self.controller: PresserClicker = controller
        self.fontManager: FontManager = FontManager()

    
    def loadTexture(self, imagePath, tag):
        width, height, channels, data = dpg.load_image(imagePath)
        dpg.add_static_texture(width=width, height=height, default_value=data, tag=tag)

    
    def loadTextures(self):
        with dpg.texture_registry():
            self.loadTexture(util.resource_path('delete.png'), TMng.TextureTags.Delete)
            self.loadTexture(util.resource_path('up.png'), TMng.TextureTags.Up)
            self.loadTexture(util.resource_path('down.png'), TMng.TextureTags.Down)

    
    def setTheme(self):
        with dpg.theme() as globalTheme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 3, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 0, 2, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_SelectableTextAlign, 0, 0.5, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 60, 67), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (60, 60, 67), category=dpg.mvThemeCat_Core)
        with dpg.theme() as keyTableTheme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Header, (39, 39, 45), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (29, 151, 236, 130), category=dpg.mvThemeCat_Core)
        with dpg.theme() as keyTablePanelTheme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, category=dpg.mvThemeCat_Core)
        dpg.bind_theme(globalTheme)
        dpg.bind_item_theme(TMng.KeyTableTags.KeyTable, keyTableTheme)
        dpg.bind_item_theme(TMng.KeyTablePanelTags.KeyTablePanel, keyTablePanelTheme)


    def run(self):
        dpg.create_context()
        dpg.create_viewport(title='Presser, Clicker', width=500, height=350, small_icon=util.resource_path('icon_small.ico'), large_icon=util.resource_path('icon_large.ico'))
        self.fontManager.init()
        dpg.bind_font(self.fontManager.DefaultFont)
        self.loadTextures()

        with dpg.window(label='Presser, Clicker', tag='main/window'):
            messageBoxComp = MessageBox()
            ToggleKeyPanel(self.fontManager, messageBoxComp, self.controller).render()
            dpg.add_separator()
            KeysPanel(self.fontManager, messageBoxComp, self.controller).render()
            messageBoxComp.render()

        self.setTheme()
        # dpg.show_style_editor()

        dpg.set_primary_window('main/window', True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
