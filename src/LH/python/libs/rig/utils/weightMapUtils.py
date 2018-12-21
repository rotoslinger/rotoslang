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
                            dataType="doubleArray",
                            defaultValue=1.0, addAttr=True):
    mayaObject = getCleanShape(mayaObject)
    if not mayaObject:
        return
    # Single
    for i in mayaObject:
        if addAttr:
            cmds.addAttr(i, ln=weightName, dataType=dataType)
            setDefaultWeights(i, weightName, dataType=dataType, defaultValue=defaultValue)
        cmds.makePaintable("mesh", weightName)


def setDefaultWeights(name, attrName, dataType, defaultValue=1.0):
    polyCount = cmds.polyEvaluate(name, v=True)
    defaultVals = [defaultValue for x in range(polyCount)]
    cmds.setAttr(name + "." + attrName, defaultVals, type=dataType)


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

