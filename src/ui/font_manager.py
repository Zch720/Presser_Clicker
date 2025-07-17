import dearpygui.dearpygui as dpg
from matplotlib import font_manager

class FontManager:
    __DefaultFontName = 'arial.ttf'
    __DefaultBoldFontName = 'arialbd.ttf'

    DefaultFont = None
    DefaultBoldFont = None

    def init(self):
        with dpg.font_registry():
            for font in font_manager.findSystemFonts(fontpaths=None, fontext='ttc'):
                if font.endswith(self.__DefaultFontName):
                    self.DefaultFont = dpg.add_font(font, 16)
                elif font.endswith(self.__DefaultBoldFontName):
                    self.DefaultBoldFont = dpg.add_font(font, 16)
        
        if self.DefaultFont == None or self.DefaultBoldFont == None:
            print(f"Can't find default font '{self.__DefaultFontName}' or '{self.__DefaultBoldFontName}'")
            exit()
