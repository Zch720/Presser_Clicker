import dearpygui.dearpygui as dpg
from matplotlib import font_manager
from presser_clicker import PresserClicker

DefaultFontName = 'arial.ttf'
DefaultBoldFontName = 'arialbd.ttf'

DefaultFont = None
DefaultBoldFont = None

controller = PresserClicker()


def setDefaultFonts():
    global DefaultFont, DefaultBoldFont
    
    with dpg.font_registry():
        for font in font_manager.findSystemFonts(fontpaths=None, fontext='ttc'):
            if font.endswith(DefaultFontName):
                DefaultFont = dpg.add_font(font, 16)
            elif font.endswith(DefaultBoldFontName):
                DefaultBoldFont = dpg.add_font(font, 16)
    
    if DefaultFont == None or DefaultBoldFont == None:
        print(f"Can't find default font '{DefaultFontName}' or '{DefaultBoldFontName}'")
        exit()
    
    dpg.bind_font(DefaultFont)


def toggleKeyCallback():
    dpg.configure_item('toggle_key', label='press the key')
    controller.readToggleKey()
    updateToggleKeyText()


def startListenBtnCallback():
    if controller.listening:
        dpg.configure_item('start_listen_btn', label='Start Listen')
        dpg.configure_item('toggle_key', enabled=True)
        dpg.configure_item('add_key_btn', enabled=True)
        for row in dpg.get_item_children('key_table')[1]:
            dpg.configure_item(dpg.get_item_children(row)[1][4], enabled=True)
        controller.stopListening()
    else:
        dpg.configure_item('start_listen_btn', label='Stop Listen')
        dpg.configure_item('toggle_key', enabled=False)
        dpg.configure_item('add_key_btn', enabled=False)
        for row in dpg.get_item_children('key_table')[1]:
            dpg.configure_item(dpg.get_item_children(row)[1][4], enabled=False)
        controller.startListening()


def addKeyComboCallback(sender, value):
    if value == 'keyboard':
        dpg.hide_item('mouse_btn_combo')
        dpg.show_item('added_key')

        dpg.configure_item('added_key', label='not set')
    else:
        dpg.show_item('mouse_btn_combo')
        dpg.hide_item('added_key')
        
        dpg.set_value('mouse_btn_combo', '')


def addedKeyCallback():
    dpg.configure_item('added_key', label='press the key')
    key = controller.getKey()
    dpg.configure_item('added_key', label=key)


def keyActionComboCallback(sender, value):
    if value == 'click':
        dpg.show_item('key_click_interval')
    else:
        dpg.hide_item('key_click_interval')


def addKeyBtnCallback():
    device = dpg.get_value('added_key_device')
    key = ''
    if device == 'keyboard':
        key = dpg.get_item_configuration('added_key')['label']
    else:
        key = dpg.get_value('mouse_btn_combo')

    if dpg.get_value('added_key_action_combo') == 'hold':
        controller.addHoldKey(device, key)
    else:
        interval = dpg.get_value('key_click_interval')
        controller.addClickKey(device, key, interval)

    addLastKeyDataToTable()


def removeKeyTableRowBtnCallback(sender):
    parent = dpg.get_item_parent(sender)
    device = dpg.get_value(dpg.get_item_children(parent)[1][0])
    key = dpg.get_value(dpg.get_item_children(parent)[1][1])
    controller.removeKey(device, key)
    dpg.delete_item(parent)


def toggleStateEventListener(toggled: bool):
    if toggled:
        dpg.set_value('toggle_state', 'toggled')
    else:
        dpg.set_value('toggle_state', 'untoggled')


def updateToggleKeyText():
    if controller.toggleKey == None:
        dpg.configure_item('toggle_key', label='not set')
    else:
        dpg.configure_item('toggle_key', label=controller.toggleKey)


def addLastKeyDataToTable():
    lastKeyData = controller.keys[-1]
    with dpg.table_row(parent='key_table'):
        dpg.add_text(lastKeyData.device)
        dpg.add_text(lastKeyData.key)
        dpg.add_text(lastKeyData.type)
        if (lastKeyData.interval == -1):
            dpg.add_text('-')
        else:
            dpg.add_text(f"{lastKeyData.interval:.2f}")
        dpg.add_button(label='-', width=22, callback=removeKeyTableRowBtnCallback)


def initTexts():
    updateToggleKeyText()


def main():
    dpg.create_context()
    dpg.create_viewport(title='Presser, Clicker', width=500, height=350)
    
    setDefaultFonts()

    with dpg.window(label='Presser, Clicker', tag='Primary window'):
        with dpg.group(horizontal=True):
            dpg.add_text('Toggle key:', tag='toggle_key_label')
            dpg.bind_item_font('toggle_key_label', DefaultBoldFont)
            
            dpg.add_button(tag='toggle_key', width=100, callback=toggleKeyCallback)

            dpg.add_button(label='Start Listen', tag='start_listen_btn', width=90, callback=startListenBtnCallback)
            dpg.add_text('untoggled', tag='toggle_state')

        dpg.add_separator()

        with dpg.group():
            dpg.add_text('Keys', tag='add_key_label')
            dpg.bind_item_font('add_key_label', DefaultBoldFont)

            with dpg.table(tag="key_table", width=455, indent=3, header_row=False, borders_outerH=True, borders_innerH=True):
                dpg.add_table_column(width_fixed=True, init_width_or_weight=100)
                dpg.add_table_column(width_fixed=True, init_width_or_weight=100)
                dpg.add_table_column(width_fixed=True, init_width_or_weight=100)
                dpg.add_table_column(width_fixed=True, init_width_or_weight=100)
                dpg.add_table_column(width_fixed=True, init_width_or_weight=22)

            with dpg.group(horizontal=True):
                dpg.add_combo(default_value='keyboard', items=['keyboard', 'mouse'], tag='added_key_device', width=100, callback=addKeyComboCallback)
                
                # mouse btn setting
                dpg.add_combo(items=['left', 'right'], tag='mouse_btn_combo', width=100)
                dpg.hide_item('mouse_btn_combo')

                #keyboard key setting
                dpg.add_button(label='not set', tag='added_key', width=100, callback=addedKeyCallback)

                dpg.add_combo(default_value='hold', items=['hold', 'click'], tag='added_key_action_combo', width=100, callback=keyActionComboCallback)

                dpg.add_input_double(default_value=0.01, tag='key_click_interval', width=100, min_value=0.01, min_clamped=True, step=0.01, format='%.2f')
                dpg.hide_item('key_click_interval')

                dpg.add_button(label='Add', indent=430, tag='add_key_btn', callback=addKeyBtnCallback)

    initTexts()
    controller.toggleEventListener = toggleStateEventListener
    
    dpg.set_primary_window('Primary window', True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
