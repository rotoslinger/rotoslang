import maya.cmds as cmds
import webbrowser

# Function to retrieve and display help information
def display_help(*args):
    module_name = cmds.textField('moduleField', query=True, text=True)
    flag_name = cmds.textField('flagField', query=True, text=True)
    
    if module_name:
        help_text = cmds.help(module_name, language="python")
        
        # If a flag is specified, search for the flag within the help text
        if flag_name:
            flag_info = [line for line in help_text.split('\n') if flag_name in line]
            if flag_info:
                help_text = '\n'.join(flag_info)
            else:
                help_text = f'Flag "{flag_name}" not found in {module_name}.'
                
        cmds.scrollField('helpField', edit=True, text=help_text)
    else:
        cmds.scrollField('helpField', edit=True, text='Please enter a module name.')

# Function to open Maya Python reference link for the entered command
def open_maya_reference(*args):
    module_name = cmds.textField('moduleField', query=True, text=True)
    if module_name:
        url = f"https://help.autodesk.com/cloudhelp/2024/ENU/Maya-Tech-Docs/CommandsPython/{module_name}.html"
        webbrowser.open(url)
    else:
        cmds.warning("Please enter a module name to view its reference.")

# Function to create the UI
def create_help_ui():
    if cmds.window('helpWindow', exists=True):
        cmds.deleteUI('helpWindow')
        
    window = cmds.window('helpWindow', title="Maya Module Help", widthHeight=(400, 400), sizeable=True)
    
    form = cmds.formLayout()
    
    # Text field for module input with changeCommand to fetch help as you type
    moduleField = cmds.textField('moduleField', placeholderText="Enter Maya module name...", changeCommand=display_help)
    
    # New text field to search for specific flags
    flagField = cmds.textField('flagField', placeholderText="Enter flag to search...", changeCommand=display_help)
    
    # Button to open the Maya Python command reference
    referenceButton = cmds.button(label="Open Maya Python Reference", command=open_maya_reference)
    
    # Scrollable field to display the help text
    helpField = cmds.scrollField('helpField', wordWrap=True, editable=False)
    
    # Define how UI elements should resize with the window
    cmds.formLayout(form, edit=True,
                    attachForm=[(moduleField, 'top', 5), (moduleField, 'left', 5), (moduleField, 'right', 5),
                                (flagField, 'left', 5), (flagField, 'right', 5),
                                (referenceButton, 'left', 5), (referenceButton, 'right', 5),
                                (helpField, 'left', 5), (helpField, 'bottom', 5), (helpField, 'right', 5)],
                    attachControl=[(flagField, 'top', 5, moduleField),
                                   (referenceButton, 'top', 5, flagField),
                                   (helpField, 'top', 5, referenceButton)])
    
    cmds.showWindow(window)

# Run the UI
# create_help_ui()
