import weightmap
from maya import cmds

def get_attr(node, attr, attrType=None, enumName="this=is:an=example", k=False, weightmap=False, defaultVal=0.0, nice_name=""):
    if not node:
        return
    fullName = node + "." + attr
    # If it exists, get it
    if cmds.objExists(fullName):
        retAttrs.append(fullName)
        # update dv
        if not weightmap:
            cmds.addAttr(fullName, e=True, dv=defaultVal)
            cmds.setAttr(fullName, defaultVal)
        return fullName

    # If it doesn't exist, add it
    if weightmap:
        weightmap.createWeightMapOnSingleObject(node, attr)
    else:
        if attrType == "enum":
            cmds.addAttr(node, at=attrType, ln=attr, enumName=enumName, k=k, dv=defaultVal, niceName=nice_name)
        else:
            cmds.addAttr(node, at=attrType, ln=attr, k=k, dv=defaultVal, niceName=nice_name)

    return fullName

def get_attrs(node, attrs, attrType=None, enumName=None, k=False, weightmap=False, defaultVals=[]):
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
                                 defaultVal=dv))
    return retAttrs











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
