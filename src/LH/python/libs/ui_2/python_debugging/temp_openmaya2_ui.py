import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaUI as omui
import webbrowser
import sys
import io
import re

# Function to get help for OpenMaya classes
def get_openmaya_help(library, module_name):
    try:
        # Create a buffer to capture the help output
        buffer = io.StringIO()
        sys.stdout = buffer

        # Import the OpenMaya class dynamically
        class_obj = getattr(library, module_name, None)
        
        if class_obj:
            help(class_obj)
        else:
            sys.stdout = sys.__stdout__
            return f'Error: "{module_name}" not found in {library.__name__}.'
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        return buffer.getvalue()
    except Exception as e:
        sys.stdout = sys.__stdout__  # Reset stdout on error
        return f'Error: {str(e)}'

# Function to find similar classes/modules in a given library
def find_similar_classes(library, query):
    available_classes = [attr for attr in dir(library) if not attr.startswith("__")]
    query_lower = query.lower()
    similar_classes = [cls for cls in available_classes if query_lower in cls.lower()]
    return similar_classes

# Function to display help information, searching across libraries
def display_help(*args):
    module_name = cmds.textField('openMayaModuleField', query=True, text=True)
    flag_name = cmds.textField('openMayaFlagField', query=True, text=True)

    if module_name:
        libraries = [
            ("OpenMaya", om),
            ("OpenMayaAnim", oma),
            ("OpenMayaRender", omr),
            ("OpenMayaUI", omui)
        ]
        
        exact_match_found = False
        result_text = ""

        # Check each library for an exact or partial match
        for lib_name, lib in libraries:
            similar_classes = find_similar_classes(lib, module_name)
            exact_match = next((cls for cls in similar_classes if cls.lower() == module_name.lower()), None)
            
            if exact_match:
                # Display exact match and its library
                exact_match_found = True
                result_text += f'This class was found in {lib_name}:\n\n'
                result_text += get_openmaya_help(lib, exact_match)
                break  # No need to search other libraries once we find an exact match
            elif similar_classes:
                # Add similar classes under each library category
                result_text += f'Classes found in {lib_name}:\n'
                result_text += '\n'.join(similar_classes) + '\n\n'

        if not exact_match_found and result_text == "":
            result_text = f'No similar classes found for "{module_name}".'

        # If a flag is specified, search for the flag within the help text
        if flag_name and exact_match_found:
            flag_info = [line for line in result_text.split('\n') if flag_name in line]
            if flag_info:
                result_text = '\n'.join(flag_info)
            else:
                result_text = f'Flag "{flag_name}" not found in {module_name}.'

        cmds.scrollField('openMayaHelpField', edit=True, text=result_text)
    else:
        cmds.scrollField('openMayaHelpField', edit=True, text='Please enter a class/module name.')

# Generate the correct URL based on library and module name
def get_documentation_url(library, class_name):
    base_url = "https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid="
    
    formatted_name = format_class_name(class_name)
    
    if library == "OpenMaya":
        return f"{base_url}MAYA_API_REF_py_ref_class_open_maya_1_1_{formatted_name}_html"
    elif library == "OpenMayaAnim":
        return f"{base_url}MAYA_API_REF_py_ref_class_open_maya_anim_1_1_{formatted_name}_html"
    elif library == "OpenMayaRender":
        return f"{base_url}MAYA_API_REF_py_ref_class_open_maya_render_1_1_{formatted_name}_html"
    elif library == "OpenMayaUI":
        return f"{base_url}MAYA_API_REF_py_ref_class_open_maya_u_i_1_1_{formatted_name}_html"
    else:
        return None

# Format class names according to the patterns
def format_class_name(class_name):
    if class_name.startswith("MFn"):
        return f"m_fn_{'_'.join(split_camel_case(class_name[3:]))}"
    elif class_name.startswith("MIt"):
        return f"m_it_{'_'.join(split_camel_case(class_name[3:]))}"
    elif class_name.startswith("MPx"):
        return f"m_px_{'_'.join(split_camel_case(class_name[3:]))}"
    elif class_name == "M3dView":
        return "m3d_view"
    elif class_name == "MHWShaderSwatchGenerator":
        return "m_h_w_shader_swatch_generator"
    elif class_name == "MUiMessage":
        return "m_ui_message"
    else:
        return f"m_{'_'.join(split_camel_case(class_name[1:]))}"

# Split camel case names into components for URL formatting
def split_camel_case(name):
    return [x.lower() for x in re.findall(r'[A-Z][^A-Z]*', name)]

# Function to open the Maya Python command reference for the module
def open_maya_reference(*args):
    module_name = cmds.textField('openMayaModuleField', query=True, text=True)
    
    if module_name:
        libraries = [
            ("OpenMaya", om),
            ("OpenMayaAnim", oma),
            ("OpenMayaRender", omr),
            ("OpenMayaUI", omui)
        ]
        
        # Check for the specific class in each library and build the correct URL
        for lib_name, lib in libraries:
            if getattr(lib, module_name, None):
                url = get_documentation_url(lib_name, module_name)
                if url:
                    webbrowser.open(url)
                    return

        # Default if no class is found
        webbrowser.open("https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=MAYA_API_REF_py_ref_class_open_maya_1_1_maya_sdk_py_ref_annotated_html")
    else:
        webbrowser.open("https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=MAYA_API_REF_py_ref_class_open_maya_1_1_maya_sdk_py_ref_annotated_html")

# Create the UI function
def create_openmaya_help_ui():
    if cmds.window('openMayaHelpWindow', exists=True):
        cmds.deleteUI('openMayaHelpWindow')

    window = cmds.window('openMayaHelpWindow', title="OpenMaya API Help", widthHeight=(400, 400), sizeable=True)

    form = cmds.formLayout()
    
    moduleField = cmds.textField('openMayaModuleField', placeholderText="Enter OpenMaya class/module name...", changeCommand=display_help)
    flagField = cmds.textField('openMayaFlagField', placeholderText="Enter flag to search...", changeCommand=display_help)

    referenceButton = cmds.button(label="Open Maya Python Reference", command=open_maya_reference)

    helpField = cmds.scrollField('openMayaHelpField', wordWrap=True, editable=False)

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
create_openmaya_help_ui()

