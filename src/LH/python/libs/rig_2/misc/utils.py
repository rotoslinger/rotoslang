from maya import cmds
def lock_attrs(mayaObject,
               attrs=["sx","sy","sz"],
               unhide = False,
               lock = True,
               keyable = False,
               channelBox = False):
    if unhide == True:
        lock = False
        keyable = True
        channelBox = True
    if attrs == ["all"]:
        attrs = ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]
    for i in range(len(attrs)):
        cmds.setAttr(mayaObject + "." + attrs[i], 
                        lock = lock, 
                        keyable = keyable, 
                        channelBox = channelBox)

def get_parent(mayaObject):
    parent = cmds.listRelatives( mayaObject, parent=True)
    if parent:
        return parent[0]

def get_shape(mayaObject):
    # double check it isn't already a mesh, just in case a transform is passed in...
    objectType = cmds.objectType(mayaObject)
    if objectType == "mesh" or objectType == "nurbsCurve" or objectType == "nurbsSurface" or objectType == "lattice":
        return mayaObject
    relatives = cmds.listRelatives(mayaObject, shapes=True, fullPath=True)
    if relatives:
        return relatives

def get_var_litteral(var, namespace):
    # all_vars = locals()
    # print "ALLVARS", namespace
    return [name for name in namespace if namespace[name] is var]
    
    
