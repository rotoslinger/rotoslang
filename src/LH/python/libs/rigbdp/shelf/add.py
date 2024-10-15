import importlib
from rigbdp.ui import lockui
from rigbdp.shelf import refresh
importlib.reload(lockui)
importlib.reload(refresh)

import maya.cmds as cmds
import inspect


def extract_module_code(module):
    module_code = inspect.getsource(module)

    # Find the first function in the module to use as the button title
    function_names = [name for name, obj in inspect.getmembers(module) if inspect.isfunction(obj)]
    button_title = function_names[0] if function_names else 'NoFunctionFound'

    # Construct the command to execute the module code
    button_command = f"""{module_code}\n{button_title}()"""
    return button_title, button_command

# TODO split the add shelf and add button to two functions
def create_shelf_tab_with_button(module, shelf_name, debug=False):
    """
    Creates a new shelf tab and adds a button that contains the code from the specified module.

    Args:
        module: The actual module object containing the function to be used.
        shelf_name (str): The name of the new shelf tab.
        debug (bool): If True, skips adding the button and prints outputs instead.
    """

    button_title, button_command = extract_module_code(module)
    refresh_button_title, refresh_button_command = extract_module_code(refresh)

    # Print outputs if in debug mode
    if debug:
        print(f"Debug Mode: ON")
        print(f"Shelf Name: {shelf_name}")
        print(f"Button Title: {button_title}")
        print(f"Button Command:\n{button_command}")
    else:
        # Replace spaces with underscores for the shelf layout name
        # Only used to check if the shelf exists, as spaces do not register in the query they instead format to BDP_Rigging
        conditional_shelf_name = shelf_name.replace(' ', '_')


        # Check if the shelf tab already exists, if not create it
        if not cmds.shelfLayout(conditional_shelf_name, exists=True):
            cmds.shelfLayout(shelf_name, parent='ShelfLayout')


        if cmds.control('buttonName', exists=True):
            print("The button exists!")
        else:
            print("The button does not exist.")

        # Create the button on the shelf
        cmds.shelfButton(parent=conditional_shelf_name, label=button_title, image1='commandButton.png', command=button_command, imageOverlayLabel=button_title)
        cmds.shelfButton(parent=conditional_shelf_name, label=refresh_button_title, image1='commandButton.png', command=refresh_button_command, imageOverlayLabel=refresh_button_title)


        print(button_title)

def refresh_shelf():
    pass

# Example usage
# import myModule  # Import your module here
# create_shelf_tab_with_button(lockui, 'BDP Rigging', debug=False)
