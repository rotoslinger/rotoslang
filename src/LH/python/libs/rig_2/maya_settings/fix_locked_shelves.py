import maya.cmds as cmds

def enable_shelf_buttons():
    shelf_id = "ShelfLayout"
    # Query the shelf tabs
    tabs = cmds.tabLayout(shelf_id, query=True, childArray=True)
    
    if not tabs:
        return  # Exit if there are no tabs
    
    for tab in tabs:
        # Query the buttons in each tab
        buttons = cmds.layout("{0}|{1}".format(shelf_id, tab), query=True, childArray=True)

        if not buttons:
            continue  # Skip if no buttons in the tab

        for button in buttons:
            button_id = "{0}|{1}|{2}".format(shelf_id, tab, button)
            # Check if the button exists and enable it
            if cmds.shelfButton(button_id, exists=True):
                cmds.shelfButton(button_id, edit=True, enable=True)

# Run the function
enable_shelf_buttons()
