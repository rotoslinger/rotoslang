import inspect
from . import weightmap as _weightmap
from maya import cmds
import ast
from rig_2.attr import constants as attr_constants

def get_attr(node, attr, attrType=None, dataType=None, enumName="this=is:an=example", k=False, weightmap=False, defaultVal=0.0, nice_name="", parent=None):
    if not node:
        return
    fullName = node + "." + attr
    retAttrs = []
    # If it exists, get it
    if cmds.objExists(fullName):
        retAttrs.append(fullName)
        # update dv
        if not weightmap and not dataType and not attrType=="message":
            cmds.addAttr(fullName, e=True, dv=defaultVal)
            cmds.setAttr(fullName, defaultVal)
        return fullName

    # If it doesn't exist, add it
    if weightmap:
        _weightmap.createWeightMapOnSingleObject(node, attr)
    else:
        # These are arguments that may error out if they are use with a None value
        kwargs={}
        # If a parent isn't specified, but the parent flag is used, addAttr() will fail
        if parent:
            kwargs["parent"] = parent
        # If attr type isn't enum, but the enumName flag is used, addAttr() will fail
        if attrType == "enum":
            kwargs["enumName"] = enumName
        # If we are setting a datatype we may not want to use the attrType arg at all
        if attrType:
            kwargs["at"] = attrType
        # Data type is more rarely used
        if dataType:
            kwargs["dt"] = dataType
        # Using the defaultVal arg with the dataType arg will cause addAttr() to fail
        if defaultVal:
            kwargs["dv"] = defaultVal
        cmds.addAttr(node, ln=attr, k=k, niceName=nice_name, **kwargs)

    return fullName

def get_attrs(node, attrs, attrType=None, dataType=None, enumName=None, k=False, weightmap=False, defaultVals=[], parent=None):
    if not node:
        return
    retAttrs = []
    for idx, attr in enumerate(attrs):
        dv = 0.0
        if defaultVals:
            dv = defaultVals[idx]
        fullName = node + "." + attr
        retAttrs.append(get_attr(node=node,
                                 attr=attr,
                                 attrType=attrType,
                                 enumName=enumName,
                                 k=k,
                                 weightmap=weightmap,
                                 defaultVal=dv,
                                 parent=None))
    return retAttrs

def get_attr_from_arg(node, attr_name, attr_type, attr_default):   
    
    
    if type(attr_default) not in attr_constants.ARG_SUPPORTED_TYPES:
        attr_default = get_relative_path(attr_default)
        dataType = "string"
        attr_type=str
        attrType=False
        defaultVal=None
    elif attr_constants.ARG_ATTR_TYPE_DICT[attr_type] == "string":
        dataType = "string"
        attrType=False
        defaultVal=None
    else:
        attrType = attr_constants.ARG_ATTR_TYPE_DICT[attr_type]
        dataType = False
        defaultVal=attr_default
        
    new_attr = get_attr(node=node, attr=attr_name, dataType=dataType, attrType=attrType, defaultVal=defaultVal,  k=True)
    if attr_constants.ARG_ATTR_TYPE_DICT[attr_type] == "string":
        cmds.setAttr(node + "." + attr_name, str(attr_default), type="string")
    return new_attr

def get_relative_path(class_obj):
        module = class_obj.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return class_obj.__class__.__name__  # Avoid reporting __builtin__
        else:
            return module + '.' + class_obj.__class__.__name__

def create_string_array(node, attr_name, default_string_list=None):
    full_attr_name = node + "." + attr_name
    get_attr(node, attr_name, dataType="stringArray")
    if default_string_list and type(default_string_list) == list:
        set_string_array_attr(full_attr_name, default_string_list)
    return full_attr_name

def set_string_array_attr(string_array_attr, string_list):
    cmds.setAttr(string_array_attr,
                 len(string_list),
                 *string_list,
                 type='stringArray')

def add_string_to_string_array(string_array_attr, string_to_add):
    string_list = cmds.getAttr(string_array_attr)
    if string_list:
        string_list.append(string_to_add)
    else:
        string_list = [string_to_add]
    set_string_array_attr(string_array_attr, string_list)
    return string_list

def add_to_string_array_dict_at_index(string_array_attr, index, dictionary_key, dictionary_value):
    string_list = cmds.getAttr(string_array_attr)
    string_dict = ast.literal_eval(str(string_list[index]))
    string_dict[dictionary_key] = dictionary_value
    string_list[index] = str(string_dict)
    set_string_array_attr(string_array_attr, string_list)
    return string_list


# def set_string_attr(string_attr, string_to_set):
#     cmds.setAttr(string_array_attr,
#                  string_to_set,
#                  type='string')




# def create_compound_attr(node, compound_attr_name, num_children):
#     full_attr_name = node + "." + compound_attr_name
#     cmds.addAttr(node,
#                 longName = compound_attr_name,
#                 numberOfChildren = num_children, 
#                 attributeType = 'compound',
#                 multi = False, 
#                 # indexMatters=True
#                 )
#     return full_attr_name

# def add_child_to_compound_attr(node, compound_attr, child):
#     children = cmds.attributeQuery(compound_attr,  node=node, listChildren=True)
#     num_children = len(children)
#     cmds.deleteAttr(node + "." + compound_attr)
#     create_compound_attr(node, compound_attr, num_children = num_children + 1)





# def get_attrs(node, attrs, attrType=None, enumName=None, k=False, weightmap=False, defaultVals=[]):
#     if not node:
#         return
#     retAttrs = []
#     for idx, attr in enumerate(attrs):
#         dv = 0.0
#         if defaultVals:
#             dv = defaultVals[idx]
#         fullName = node + "." + attr
#         if cmds.objExists(fullName):
#             retAttrs.append(fullName)
#             # update dv
#             if defaultVals:
#                 cmds.addAttr(fullName, e=True, dv=dv)
#                 cmds.setAttr(fullName, dv)
#             continue
#         if weightmap:
#             weightmap.createWeightMapOnSingleObject(node, attr)
#         else:
#             if attrType == "enum":
#                 cmds.addAttr(node, at=attrType, ln=attr, enumName=enumName, k=k, dv=dv)
#             else:
#                 cmds.addAttr(node, at=attrType, ln=attr, k=k, dv=dv)

#         retAttrs.append(fullName)
#     return retAttrs
