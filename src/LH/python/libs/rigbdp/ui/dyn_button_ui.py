import maya.cmds as cmds

def create_dynamic_button_ui(button_dict, row_len=3, col_len=3, row_title=["row 1","row 2"], col_title=["column 1", "column 2", "column 3"]):
    """
    Creates a UI that dynamically generates buttons based on a given dictionary.
    
    Args:
        button_dict (dict): A dictionary where keys are button names (str), and values are the functions to call (func).
        row_len (int): The number of buttons allowed in each row.
        col_len (int): The number of buttons allowed in each column.
        row_title (str): Title for the row section.
        col_title (str): Title for the column section.
    """
    # Create a new window
    if cmds.window("dynamicButtonWindow", exists=True):
        cmds.deleteUI("dynamicButtonWindow", window=True)

    window = cmds.window("dynamicButtonWindow", title="Dynamic Button UI", widthHeight=(400, 300))
    cmds.scrollLayout()  # Create a scrollable layout in case there are too many buttons
    main_layout = cmds.gridLayout(numberOfColumns=row_len+1, cellWidthHeight=(100, 50))

    # Add column titles
    cmds.text(label="")
    for i in range(row_len):
        cmds.text(label=f"{col_title[i]}")

    # Add row titles and buttons dynamically
    for row in range(col_len):
        # Add row title
        cmds.text(label=f"{row_title[row]}")
        
        # Add buttons in each row
        for button_name, button_func in list(button_dict.items())[row * row_len : (row + 1) * row_len]:
            cmds.button(label=button_name, command=lambda x, func=button_func: func())

    cmds.showWindow(window)
####################################################################################################################################
# Example usage
def example_function1():
    print("Button 1 Pressed!")
def example_function2():
    print("Button 2 Pressed!")
def example_function3():
    print("Button 3 Pressed!")
def example_function4():
    print("Button 4 Pressed!")
def example_function5():
    print("Button 5 Pressed!")
def example_function6():
    print("Button 6 Pressed!")

button_dict = {
    "Button 1": example_function1,
    "Button 2": example_function2,
    "Button 3": example_function3,
    "Button 4": example_function4,
    "Button 5": example_function5,
    "Button 6": example_function6,
}
create_dynamic_button_ui(button_dict, row_len=3, col_len=2, row_title=["row 1","row 2"], col_title=["column 1", "column 2", "column 3"])
####################################################################################################################################
