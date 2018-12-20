from maya import cmds

PREFIX = "LH"

def getCleanShape(mayaObject=None):
    if not mayaObject: mayaObject = cmds.ls(sl=True)
    if not mayaObject:
        return
    objType = cmds.objectType(mayaObject)
    if objType != "mesh" and objType != "transform":
        return
    if objType == "transform":
        mayaObject = cmds.listRelatives(mayaObject, shapes=True)
    if type(mayaObject) != list:
        mayaObject = [mayaObject]
    return mayaObject



def createWeightMapOnObject(mayaObject=None,
                            weightName=PREFIX+"WeightMap",
                            dataType="doubleArray"):
    mayaObject = getCleanShape(mayaObject)
    if not mayaObject:
        return
    # Single
    for i in mayaObject:
        cmds.addAttr(i, ln=weightName, dataType=dataType)
        cmds.makePaintable("mesh", weightName)


def removeWeightMapOnObject(mayaObject=None,
                            weightName=PREFIX+"WeightMap",
                            deleteAttr=False):
    if deleteAttr:
        mayaObject = getCleanShape(mayaObject)
        if not mayaObject:
            return
        for i in mayaObject:
            if cmds.attributeQuery(weightName, n= i, e=True):
                cmds.deleteAttr(i + "." + weightName)
    cmds.makePaintable("mesh", weightName, remove=True)

