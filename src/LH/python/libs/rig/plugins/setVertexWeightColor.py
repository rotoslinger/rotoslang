import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
 
class SetVertexWeightColor(OpenMayaMPx.MPxCommand):
    originalWeightValuesShort = "-owv"
    originalWeightValuesLong = "-originalWeightValues"
    newWeightValuesShort = "-nwv"
    newWeightValuesLong = "-newWeightValues"
    fnMeshShort = "-fnm"
    fnMeshLong = "-fnMesh"
    vertexColorListShort = "-vcl"
    vertexColorListLong = "-vertexColorList"
    vertexIndexListShort = "-vil"
    vertexIndexListLong = "-vertexIndexList"



    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self._dgmod = OpenMaya.MDGModifier()



    @classmethod
    def command_syntax(cls):
        syntax = OpenMaya.MSyntax()
        syntax.addFlag(cls.originalWeightValuesShort, cls.originalWeightValuesLong, OpenMaya.MSyntax.kNone)
        syntax.addFlag(cls.newWeightValuesShort, cls.newWeightValuesLong, OpenMaya.MSyntax.kNone)
        syntax.addFlag(cls.fnMeshShort, cls.fnMeshLong, OpenMaya.MSyntax.kNone)
        syntax.addFlag(cls.vertexColorListShort, cls.vertexColorListLong, OpenMaya.MSyntax.kNone)
        syntax.addFlag(cls.vertexIndexListShort, cls.vertexIndexListLong, OpenMaya.MSyntax.kNone)
        # syntax.setObjectType(OpenMaya.MSyntax.kSelectionList, 2, 2)
        syntax.useSelectionAsDefault(False)
        syntax.enableEdit(False)
        syntax.enableQuery(False)
        return syntax


    def doIt(self, args):
        arg_data = OpenMaya.MArgDatabase(self.syntax(), args)
        if arg_data.isFlagSet(self.originalWeightValuesShort):
            self.originalWeightValues = arg_data.flagArgumentString(self.originalWeightValuesShort, 0)
        if arg_data.isFlagSet(self.newWeightValuesShort):
            self.newWeightValues = arg_data.flagArgumentString(self.newWeightValuesShort, 0)
        if arg_data.isFlagSet(self.fnMeshShort):
            self.fnMesh = arg_data.flagArgumentString(self.fnMeshShort, 0)
        if arg_data.isFlagSet(self.vertexColorListShort):
            self.vertexColorList = arg_data.flagArgumentString(self.vertexColorListShort, 0)
        if arg_data.isFlagSet(self.vertexIndexListShort):
            self.vertexIndexList = arg_data.flagArgumentString(self.vertexIndexListShort, 0)
        setVertexColors(self.newWeightValues, self.fnMesh, self.vertexColorList, self.vertexIndexList)

    def undoIt(self, ):
        self._dgmod.undoIt()

    def redoIt(self):
        self._dgmod.doIt()

    def isUndoable(self):
        return True
 
def creator():
    return OpenMayaMPx.asMPxPtr(SetVertexWeightColor())
 
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Levi Harrison', '1.0', 'Any')
    try:
        plugin.registerCommand('setVertexWeightColor', creator)
    except:
        raise RuntimeError('Failed to register command')
 
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterCommand('setVertexWeightColor')
    except:
        raise RuntimeError('Failed to unregister command')


def setVertexColors(allWeightValues, fnMesh, vertexColorList, vertexIndexList):
    for c in range(vertexColorList.length()):
        # print c
        # print allWeightValues[c]
        vertexColorList[c].r = float(allWeightValues[0][c])
        vertexColorList[c].g = float(allWeightValues[0][c])
        vertexColorList[c].b = float(allWeightValues[0][c])
        vertexColorList[c].a = float(1.0)
    fnMesh.setVertexColors(vertexColorList, vertexIndexList, None)
