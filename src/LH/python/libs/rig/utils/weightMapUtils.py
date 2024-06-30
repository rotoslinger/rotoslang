from maya import cmds
from rig.utils import misc

# for testing purposes AA will put the test map at the top of the connections if they are listed alphabetically
PREFIX = "AA"

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

def createWeightMapOnSingleObject(mayaObject=None,
                            weightName=PREFIX+"WeightMap",
                            dataType="doubleArray",
                            defaultValue=1.0, addAttr=True,
                            makePaintable=True,
                            geoType = "mesh"):
    mayaObject = misc.getShape(mayaObject)
    if addAttr:
        cmds.addAttr(mayaObject, ln=weightName, dataType=dataType)
        setDefaultWeights(mayaObject, weightName, dataType=dataType, defaultValue=defaultValue)
    if makePaintable:
        cmds.makePaintable(geoType, weightName)
    returnAttrs = mayaObject + "." + weightName
    return returnAttrs

def createWeightMapOnObject(mayaObject=None,
                            weightName=PREFIX+"WeightMap",
                            dataType="doubleArray",
                            defaultValue=1.0, addAttr=True,
                            makePaintable=True):
    mayaObject = getCleanShape(mayaObject)
    if not mayaObject:
        return
    # Single
    returnAttrs = []
    for i in mayaObject:
        if addAttr:
            cmds.addAttr(i, ln=weightName, dataType=dataType)
            setDefaultWeights(i, weightName, dataType=dataType, defaultValue=defaultValue)
        if makePaintable:
            cmds.makePaintable("mesh", weightName)
        returnAttrs.append(i + "." + weightName)
    return returnAttrs

def createWeightMapOnDeformer(deformer=None,
                              mesh = None,
                              weightName=PREFIX+"WeightMap",
                              dataType="doubleArray",
                              defaultValue=1.0, addAttr=True,
                              makePaintable=True):
    mesh = getCleanShape(mesh)
    if not mesh:
        return
    deformerType = cmds.objectType(deformer)
    # Single
    returnAttrs = []
    if addAttr:
        cmds.addAttr(deformer, ln=weightName, dataType=dataType)
        setDefaultWeightsWithDeformer(mesh, deformer, weightName, dataType=dataType, defaultValue=defaultValue)
    if makePaintable:
        cmds.makePaintable(deformerType, weightName)
    returnAttrs.append(deformer + "." + weightName)
    return returnAttrs

def createMultiWeightMapOnDeformer(deformer=None,
                              mesh = None,
                              weightName=None,
                              dataType="doubleArray",
                              defaultValue=1.0, addAttr=True,
                              makePaintable=True):
    mesh = getCleanShape(mesh)
    if not mesh or not weightName:
        return
    deformerType = cmds.objectType(deformer)
    # Single
    returnAttrs = []
    compoundName = weightName + 'Weights'
    weightMapName = weightName + 'Weight'
    if addAttr and not cmds.objExists(deformer + "." + compoundName):
        cmds.addAttr(deformer,
                        longName = compoundName,
                        numberOfChildren = 1, 
                        attributeType = 'compound',
                        multi = True, 
                        indexMatters=True)
        cmds.addAttr(deformer, 
                        longName = weightMapName,
                        dataType = 'doubleArray',
                        parent = compoundName)
        setDefaultMultiWeightsWithDeformer(mesh, deformer, weightMapName, compoundName , dataType=dataType, defaultValue=defaultValue)
    if makePaintable:
        cmds.makePaintable(deformerType, weightMapName, attrType='doubleArray', shapeMode='deformer')
    returnAttrs.append(deformer + "." + weightMapName)
    return returnAttrs

def setDefaultWeights(name, attrName, dataType, defaultValue=1.0):
    iterGeo = misc.getOMItergeo(name)
    count = iterGeo.count()
    defaultVals = [defaultValue for x in range(count)]
    cmds.setAttr(name + "." + attrName, defaultVals, type=dataType)

def setDefaultWeightsWithDeformer(meshName, deformerName, attrName, dataType, defaultValue=1.0):
    iterGeo = misc.getOMItergeo(name)
    polyCount = iterGeo.count()
    defaultVals = [defaultValue for x in range(polyCount)]
    cmds.setAttr(deformerName + "." + attrName, defaultVals, type=dataType)

def setDefaultMultiWeightsWithDeformer(meshName, deformerName, attrName, multiAttrName, dataType, defaultValue=1.0):
    iterGeo = misc.getOMItergeo(name)
    polyCount = iterGeo.count()
    defaultVals = [defaultValue for x in range(polyCount)]
    finalAttrName = "{0}.{1}[0].{2}".format(deformerName, multiAttrName, attrName)
    cmds.setAttr(finalAttrName, defaultVals, type=dataType)


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

# def refreshPaintableWeightOnMesh(mayaMesh="pSphereShape1"):
#     """
#     Because maya is only able to make attributes paintable per object type ("mesh", "nurbsSurface", "nurbsCurve")
#     and not per object, if you make an attribute paintable for one mesh, it will make it paintable for all other meshes
#     reguardless of whether or not they actually have the attribute.
#     This function will find out if these paintable attributes actually exist on the object, if they do not, it will clear
#     them from the paintable attributes.
#     Finds all paintable attributes on a mesh, clear all, except the ones that actually exists
#     :param mayaMesh: this needs to be the shape of a polygon mesh
#     :return:
#     """
#     # First get all userDefined attributes of type kDoubleArray
#     attrs = cmds.listAttr(mayaMesh, ud=True, a=True)
#     for attr in attrs:
#         fullAttrName = mayaMesh + "." + attr
#         type = cmds.getAttr(mayaMesh + "." + attr, typ=True)
#         if not type == "doubleArray":
#             continue
#         # print cmds.setToolTo("artAttrContext")
#         # print cmds.artAttrCtx()
#         #print cmds.makePaintable(mayaMesh, aca=True,q=True)
#         #cmds.artUserPaintCtx('artUserPaintCtx')
#         # cmds.currentCtx()
#         #print cmds.artUserPaintCtx("artAttrContext", objattrArray=True,q=True)
#         # ctx = cmds.artAttrCtx('artAttrCtx3')
#         # print "CONTEXT NAME ", ctx
#         # cmds.setToolTo('artAttrCtx3')
#         #
#         # print cmds.artAttrCtx('artAttrCtx3', q=True, objattrArray=True)
#         #
#         # cmds.deleteUI(ctx)

def connectWeightMapToWeightNode(sourceMap=None, destWeightNode=None, sourceFactor=None, sourceOperationEnum=None, force=False):
    """
    The weightNode takes up to 3 inputs:
    1. A weightmap of kDoubleArray
    2. A scalar attribute called "factor" that is a double
    3. An enum attribute called "product" that is an enum with names 0 "add", 1 "subtract", 2 "multiply", 3 "divide"

    To use this function you at least need to provide a source weightmap, from a geo shape that is type kDoubleArray,
    and a destination weightNode.

    You can also provide other source and destination attributes for connections, but you don't have to.

    :param sourceMap: a string of an attribute of type kDoubleArray
    :param destWeightNode: the weightMap where you want to connect this weightMap
    :param sourceFactor: a string of an attribute of type double
    :param sourceOperationEnum: a string of an attribute of type enum (needs to have a length of 4 cases preferably with
            "add", "subtract", "multiply", "divide" as the names of the cases)
    :return:
    """
    if not sourceMap and not destWeightNode:
        return
    size = cmds.getAttr(destWeightNode + ".Inputs", s=True)
    # Connect to next available item

    # ----Connect weightMap
    weightMapCheck = connectionCheck(destWeightNode, sourceMap)
    safeConnectWeightAttrs(weightMapCheck, destWeightNode, force, size, sourceMap, "inputWeights")
    if sourceFactor:
        # ----Connect sourceFactor
        sourceFactorCheck = connectionCheck(destWeightNode, sourceFactor)
        safeConnectWeightAttrs(sourceFactorCheck, destWeightNode, force, size, sourceFactor, "factor")
    if sourceOperationEnum:
        # ----Connect sourceProductEnum
        sourceOperationEnumCheck = connectionCheck(destWeightNode, sourceOperationEnum)
        safeConnectWeightAttrs(sourceOperationEnumCheck, destWeightNode, force, size, sourceOperationEnum, "operation")


def safeConnectWeightAttrs(isConnected, destNode, forceConnection, size, attrToConnect, attrName="inputWeights"):
    if isConnected:
        print(attrToConnect + "  has already been connected to " + destNode)
        if forceConnection:
            cmds.connectAttr(attrToConnect, destNode + ".Inputs[{0}].{1}".format(size, attrName))
    else:
        cmds.connectAttr(attrToConnect, destNode + ".Inputs[{0}].{1}".format(size, attrName))


def connectionCheck(destNode, attr):
    connections = cmds.listConnections(destNode, plugs=True)
    if not connections:
        return False
    for con in connections:
        print(con)
        if str(con) == attr:
            return True
    return False



def connectWeightNodeToWeightList(sourceWeightNode=None, destAttr=None, convertToFloat=False, convertName="LHKDoubleArrayToKFloatArray1"):
    """Connects the output weights from the weight node to the weightlist that will be driven.
    The weightNode outputs kDoubleArray because it is much faster to process and set.
    There are many maya deformers that do not accept kDoubleArray weights.
    To name a few, cluster, lattice, and the nonlinear deformers
    If the destWeightList is type kFloat Array (within a compound like the maya cluster and lattice)
    a conversion node will be created and connected.
    """
    if not sourceWeightNode and not destAttr:
        return
    if not convertToFloat:
        sourceAttr = sourceWeightNode + ".outWeights"
        cmds.connectAttr(sourceAttr, destAttr)
        return
    createAndConnectFloatConvertNode(sourceWeightNode + ".outWeights", destAttr, convertName)



def createAndConnectFloatConvertNode(inComingAttr, weightAttrToConnectTo, name="LHKDoubleArrayToKFloatArray1"):
    node = cmds.createNode("LHKDoubleArrayToKFloatArray", name=name)
    # ---Create outputArray
    cmds.getAttr(node + ".outFloatWeightList[0]", typ=True)
    cmds.connectAttr(inComingAttr, node + ".inWeights")
    cmds.connectAttr(node + ".outFloatWeightList[0]", weightAttrToConnectTo)


# def connectWeightNodeToWeightListCOMPLEX(sourceWeightNode=None, destNode=None, destAttr=None, destWeightListIdx=None):
#     """Connects the output weights from the weight node to the weightlist that will be driven.
#     The weightNode outputs kDoubleArray because it is much faster to process and set.
#     There are many maya deformers that do not accept kDoubleArray weights.
#     To name a few, cluster, lattice, and the nonlinear deformers
#     If the destWeightList is type kFloat Array (within a compound like the maya cluster and lattice)
#     a conversion node will be created and connected.
#     """
#     fullDestAttrName = destNode + "." + destAttr
#     if not sourceWeightNode and not destNode:
#         return
#     size = cmds.getAttr(fullDestAttrName, s=True)
#
#     type = cmds.getAttr(fullDestAttrName, type=True)
#
#
#     if type == "TdataCompound":
#         # Should have only 1 child type, and at least 1 element so this should be safe
#         childWeights = cmds.attributeQuery(destAttr, node=destNode, listChildren=True)[0]
#         childAttrName = destNode + "." + destAttr + "[0]." + childWeights +"[0]"
#         type = cmds.getAttr(childAttrName, type=True)
#         if type == "double":
#             attrToConnect = destNode + "." + destAttr + "[0]." + childWeights
#             print "DOUBLE"
#         if type == "doubleArray":
#             attrToConnect = destNode + "." + destAttr + "[0]." + childWeights
#             print "doubleArray"
#         if type == "float":
#             attrToConnect = destNode + "." + destAttr + "[0]." + childWeights
#             print "float"

                # for i in range(size):
    #     print babyWeights

    # cmds.createNode("LHKDoubleArrayToKFloatArray")
    # # To get new array item
    # cmds.getAttr("LHKDoubleArrayToKFloatArray1.outFloatWeightList[0]", typ=True)

def addCapsuleWeightsToLHCollisionDeformer(meshIdx=0, addAttr=True, updatePaintableWeights=True):
    """Select collision deformer and run.  Will add capsule weights for any capsule array that doesn't have weights attached already
    meshIdx refers to the idx of the selected mesh in the deformer.  If 3 meshes are being deformed, and the selected mesh is the 2nd in the mIndex, the idx will be 1
    
    
    """
    deformer = cmds.ls(sl=True)[0]
    mesh = cmds.ls(sl=True)[1]
    # Get attr
    collisionInput = cmds.getAttr(deformer + ".primitiveCollisionInputs", mi=True)
    inputCount = len(collisionInput)


#   MGlobal::executeCommand("makePaintable -attrType multiDouble -shapeMode deformer LHCollisionDeformer pCollisionWeights;");
#   MGlobal::executeCommand("makePaintable -attrType multiDouble -shapeMode deformer LHCollisionDeformer pBulgeWeights;");




    for i in range(inputCount):
        for attr in ("pCollisionWeights", "pBulgeWeights"):

            colConnection = cmds.listConnections(deformer + ".primitiveCollisionInputs[{0}].pWeightsParent[{1}].{2}".format(i, meshIdx, attr))
            if not colConnection:
                attrName = deformer + ".primitiveCollisionInputs[{0}].pWeightsParent[{1}].{2}".format(i, meshIdx, attr)
                addCapsuleWeightMap(name = mesh + "{0}{1:03}".format(attr, i), deformer=deformer, attr=attrName, idx=i, mesh=mesh, addAttr=addAttr)
            elif updatePaintableWeights:
                attrName = deformer + ".primitiveCollisionInputs[{0}].pWeightsParent[{1}].{2}".format(i, meshIdx, attr)
                addCapsuleWeightMap(name = mesh + "{0}{1:03}".format(attr, i), deformer=deformer, attr=attrName, idx=i, mesh=mesh, addAttr=False)


        # bulgeConnection = cmds.listConnections(deformer + ".primitiveCollisionInputs[{0}].pWeightsParent[{1}].pBulgeWeights".format(i, meshIdx))
        #     attrName = deformer + ".primitiveCollisionInputs[{0}].pWeightsParent[{1}].pBulgeWeights".format(i, meshIdx)
        #     addCapsuleWeightMap(name = mesh + "pBulgeWeights{0:03}".format(i), deformer=deformer, attr=attrName, idx=i, mesh=mesh)






def addCapsuleWeightMap(name=None, deformer=None, attr=None, idx=None, mesh=None, addAttr=True):
    if not name or not deformer or not attr or not mesh:
        return
    print("ACTUALLY CREATING ", idx)
    createWeightMapOnDeformer(deformer=deformer, mesh=mesh, weightName=name, dataType="doubleArray",
                            defaultValue=1.0, addAttr=addAttr,
                            makePaintable=True)
    if addAttr:
        cmds.connectAttr(deformer + "." + name, attr)
    
    
