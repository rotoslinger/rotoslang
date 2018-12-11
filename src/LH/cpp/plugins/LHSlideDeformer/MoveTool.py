
# ==========================================================================
#+

#
#       Creation Date:   2 October 2006
#
#       Description:
# 
#               moveTool.py
#
# Description:
#       Interactive tool for moving objects and components.
#
#       This plug-in will register the following two commands in Maya:
#               maya.cmds.spMoveToolCmd(x, y, z)
#       maya.cmds.spMoveToolContext()
#
#       Usage:
#       import maya
#       maya.cmds.loadPlugin("moveTool.py")
#       maya.cmds.spMoveToolContext("spMoveToolContext1")
#       shelfTopLevel = maya.mel.eval("global string $gShelfTopLevel;$temp = $gShelfTopLevel")
#       maya.cmds.setParent("%s|General" % shelfTopLevel)
#       maya.cmds.toolButton("spMoveTool1", cl="toolCluster", t="spMoveToolContext1", i1="moveTool.xpm") 
#
#       Remove UI objects with
#       maya.cmds.deleteUI("spMoveToolContext1")
#       maya.cmds.deleteUI("spMoveTool1")
#
import maya.cmds as cmds

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaUI as OpenMayaUI
import sys, math

kPluginCmdName="spMoveToolCmd"
kPluginCtxName="spMoveToolContext"
kVectorEpsilon = 1.0e-3

# keep track of instances of MoveToolCmd to get around script limitation
# with proxy classes of base pointers that actually point to derived
# classes
kTrackingDictionary = {}

# command
class MoveToolCmd(OpenMayaMPx.MPxToolCommand):
        kDoIt, kUndoIt, kRedoIt = 0, 1, 2

        def __init__(self):
                OpenMayaMPx.MPxToolCommand.__init__(self)
                self.setCommandString(kPluginCmdName)
                self.__delta = OpenMaya.MVector()
                kTrackingDictionary[OpenMayaMPx.asHashable(self)] = self

        def __del__(self):
                del kTrackingDictionary[OpenMayaMPx.asHashable(self)]

        def doIt(self, args):
                argData = OpenMaya.MArgDatabase(self.syntax(), args)
                self.__action(MoveToolCmd.kDoIt)

        def redoIt(self):
                self.__action(MoveToolCmd.kRedoIt)

        def undoIt(self):
                self.__action(MoveToolCmd.kUndoIt)

        def isUndoable(self):
                return True

        def finalize(self):
                """
                Command is finished, construct a string for the command
                for journalling.
                """
                self.finalWeight = self.__weight
                command = OpenMaya.MArgList()
                command.addArg(self.commandString())
                command.addArg(self.__weight)

                # This call adds the command to the undo queue and sets
                # the journal string for the command.
                #
                try:
                        OpenMayaMPx.MPxToolCommand._doFinalize(self, command)
                except:
                        pass

        def setVector(self, x, y, z):
                self.__delta.x = x
                self.__delta.y = y
                self.__delta.z = z
        def setWeight(self, w):
                self.__weight = w

#         def draw(self, view, path, style, status):
#             view.beginGL()
#             view.drawText("Text String", OpenMaya.MPoint())
#             view.endGL()

        def __action(self, flag):
                """
                set weights
                """
                
                wt = self.__weight
                if flag == MoveToolCmd.kUndoIt:
                        wt = -wt
                else:
                        pass
                
                if cmds.optionVar(exists='weightName') == 1:
                    weightAttr = cmds.optionVar(q='weightName')
                    weightAttrSplit = weightAttr.split(".")
                    #---get deformer
                    deformer = weightAttr.split(".")[1]
                    geo = cmds.deformer(deformer, q = True, g = True)
                    geoTransform = [cmds.listRelatives(i,parent = True)[0] for i in geo]
                    #---make sure selected are points, and are in the deformer
                    selected = cmds.ls(sl = True, fl = True)
                    vtx = [i for i in selected if ".vtx[" in i]
                    cv = [i for i in selected if ".cv[" in i]
                    points = vtx + cv
                    finalPoints = []
                    
                    weightAttrs = []
                    allWeightValues = []
                    for i in range(len(geoTransform)):
                        weightAttrs.append(weightAttrSplit[1]+"."+weightAttrSplit[2] + "s["+str(i)+"]." + weightAttrSplit[2])
                        allWeightValues.append(cmds.getAttr(weightAttrs[i]))
                    
                    final_points_indexes = []
                    initial_values = []
                    for i in range(len(geoTransform)):
                        tmp_final_idx = []
                        tmp_value = []
                        for j in range(len(points)):
                            if geoTransform[i] in points[j]:
                                finalPoints.append(points[j])
                                idx = points[j].split("[")[1]
                                idx = int(idx.split("]")[0])
                                tmp_final_idx.append(idx)
                                tmp_value.append(allWeightValues[i][idx])
                        final_points_indexes.append(tmp_final_idx)
                        initial_values.append(tmp_value)
                    for i in range(len(geoTransform)):
                        for j in range(len(final_points_indexes[i])):
                            allWeightValues[i][final_points_indexes[i][j]] = initial_values[i][j]+wt
                    for i in range(len(allWeightValues)):
                        cmds.setAttr(weightAttrs[i],allWeightValues[i], typ='doubleArray')# 






                    #determine whether or not these are in the deformer

class MoveContext(OpenMayaMPx.MPxSelectionContext):
        kTop, kFront, kSide, kPersp = 0, 1, 2, 3
        
        def __init__(self):
                OpenMayaMPx.MPxSelectionContext.__init__(self)
                self._setTitleString("moveTool")
                self.setImage("moveTool.xpm", OpenMayaMPx.MPxContext.kImage1)
                self.__currWin = 0
                self.__view = OpenMayaUI.M3dView()
                self.__startPos_x = 0
                self.__endPos_x = 0
                self.__startPos_y = 0
                self.__endPos_y = 0
                self.__cmd = None

        def toolOnSetup(self, event):
                self._setHelpString("drag to move selected object")

        def doPress(self, event):
                OpenMayaMPx.MPxSelectionContext.doPress(self, event)
                spc = OpenMaya.MSpace.kWorld
                
                # If we are not in selecting mode (i.e. an object has been selected)
                # then set up for the translation.
                #
                if not self._isSelecting():
                        argX = OpenMaya.MScriptUtil()
                        argX.createFromInt(0)
                        argXPtr = argX.asShortPtr()
                        argY = OpenMaya.MScriptUtil()
                        argY.createFromInt(0)
                        argYPtr = argY.asShortPtr()
                        event.getPosition(argXPtr, argYPtr)
                        self.__startPos_x = OpenMaya.MScriptUtil(argXPtr).asShort()
                        self.__startPos_y = OpenMaya.MScriptUtil(argYPtr).asShort()
                        self.__view = OpenMayaUI.M3dView.active3dView()

                        camera = OpenMaya.MDagPath()
                        self.__view.getCamera(camera)
                        fnCamera = OpenMaya.MFnCamera(camera)
                        upDir = fnCamera.upDirection(spc)
                        rightDir = fnCamera.rightDirection(spc)

                        # Determine the camera used in the current view
                        #
                        if fnCamera.isOrtho():
                                if upDir.isEquivalent(OpenMaya.MVector.zNegAxis, kVectorEpsilon):
                                        self.__currWin = MoveContext.kTop
                                elif rightDir.isEquivalent(OpenMaya.MVector.xAxis, kVectorEpsilon):
                                        self.__currWin = MoveContext.kFront
                                else:
                                        self.__currWin = MoveContext.kSide
                        else:
                                self.__currWin = MoveContext.kPersp
                        # Create an instance of the move tool command.
                        #
                        newCmd = self._newToolCommand()
                        self.__cmd = kTrackingDictionary.get(OpenMayaMPx.asHashable(newCmd), None)
                        self.__cmd.setWeight(0.0)

        def doDrag(self, event):
                OpenMayaMPx.MPxSelectionContext.doDrag(self, event)

                # If we are not in selecting mode (i.e. an object has been selected)
                # then do the translation.
                #

                if not self._isSelecting():
                        argX = OpenMaya.MScriptUtil()
                        argX.createFromInt(0)
                        argXPtr = argX.asShortPtr()
                        argY = OpenMaya.MScriptUtil()
                        argY.createFromInt(0)
                        argYPtr = argY.asShortPtr()
                        event.getPosition(argXPtr, argYPtr)
                        self.__endPos_x = OpenMaya.MScriptUtil(argXPtr).asShort()
                        self.__endPos_y = OpenMaya.MScriptUtil(argYPtr).asShort()

                        startW = OpenMaya.MPoint()
                        endW = OpenMaya.MPoint()
                        vec = OpenMaya.MVector()
                        self.__view.viewToWorld(self.__startPos_x, self.__startPos_y, startW, vec)
#                         help(self.__view)
                        self.__view.viewToWorld(self.__endPos_x, self.__endPos_y, endW, vec)
                        downButton = event.mouseButton()
                        shiftButton = event.modifiers()
                        # We reset the the move vector each time a drag event occurs
                        # and then recalculate it based on the start position.
                        #
                        
                        self.__cmd.undoIt()
                        if self.__currWin == MoveContext.kPersp:
                            if downButton == OpenMayaUI.MEvent.kMiddleMouse and shiftButton != OpenMayaUI.MEvent.shiftKey and shiftButton != OpenMayaUI.MEvent.controlKey:
                                    all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z
                                    if all != 0:
                                        all = all/3
                                    self.__cmd.setWeight(all*40)
    #                                 length = (startW-endW).length()
    #                                 self.__cmd.setWeight((length)*20)
                            elif downButton == OpenMayaUI.MEvent.kMiddleMouse and shiftButton == OpenMayaUI.MEvent.shiftKey and shiftButton != OpenMayaUI.MEvent.controlKey:
                                    all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z
                                    if all != 0:
                                        all = all/3
                                    self.__cmd.setWeight(all*60)
                            elif downButton == OpenMayaUI.MEvent.kMiddleMouse and shiftButton == OpenMayaUI.MEvent.controlKey and shiftButton != OpenMayaUI.MEvent.shiftKey:
                                    all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z
                                    if all != 0:
                                        all = all/3
                                    self.__cmd.setWeight(all)
                            else:
                                    all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z
                                    if all != 0:
                                        all = all/3
                                    self.__cmd.setWeight(all)
                        else:
                            if downButton == OpenMayaUI.MEvent.kMiddleMouse and shiftButton != OpenMayaUI.MEvent.shiftKey and shiftButton != OpenMayaUI.MEvent.controlKey:
                                    all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z
                                    if all != 0:
                                        all = all/3
                                    self.__cmd.setWeight(all*.1)
    #                                 length = (startW-endW).length()
    #                                 self.__cmd.setWeight((length)*20)
                            elif downButton == OpenMayaUI.MEvent.kMiddleMouse and shiftButton == OpenMayaUI.MEvent.shiftKey and shiftButton != OpenMayaUI.MEvent.controlKey:
                                    all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z
                                    if all != 0:
                                        all = all/3
                                    self.__cmd.setWeight(all)
                            elif downButton == OpenMayaUI.MEvent.kMiddleMouse and shiftButton == OpenMayaUI.MEvent.controlKey and shiftButton != OpenMayaUI.MEvent.shiftKey:
                                    all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z
                                    if all != 0:
                                        all = all/3
                                    self.__cmd.setWeight(all*.01)
                            else:
                                    all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z
                                    if all != 0:
                                        all = all/3
                                    self.__cmd.setWeight(all)
                                    
                                    
                        self.__cmd.redoIt()
                        self.__view.refresh(True)

        def doRelease(self, event):
                OpenMayaMPx.MPxSelectionContext.doRelease(self, event)
                if not self._isSelecting():
                        argX = OpenMaya.MScriptUtil()
                        argX.createFromInt(0)
                        argXPtr = argX.asShortPtr()
                        argY = OpenMaya.MScriptUtil()
                        argY.createFromInt(0)
                        argYPtr = argY.asShortPtr()
                        event.getPosition(argXPtr, argYPtr)
                        self.__endPos_x = OpenMaya.MScriptUtil(argXPtr).asShort()
                        self.__endPos_y = OpenMaya.MScriptUtil(argYPtr).asShort()

                        # Delete the move command if we have moved less then 2 pixels
                        # otherwise call finalize to set up the journal and add the
                        # command to the undo queue.

                        #
                        if (math.fabs(self.__startPos_x - self.__endPos_x) < 2 and 
                                        math.fabs(self.__startPos_y - self.__endPos_y) < 2):
                                self.__cmd = None
                                self.__view.refresh(True)
                        else:
                                self.__cmd.finalize()
                                self.__view.refresh(True)

        def doEnterRegion(self, event):
                """
                Print the tool description in the help line.
                """
                self._setHelpString("drag to move selected object")


#############################################################################


class MoveContextCommand(OpenMayaMPx.MPxContextCommand):
        def __init__(self):
                OpenMayaMPx.MPxContextCommand.__init__(self)

        def makeObj(self):
                return OpenMayaMPx.asMPxPtr(MoveContext())

def cmdCreator():
        return OpenMayaMPx.asMPxPtr(MoveToolCmd())

def ctxCmdCreator():
        return OpenMayaMPx.asMPxPtr(MoveContextCommand())

def syntaxCreator():
        syntax = OpenMaya.MSyntax()
        syntax.addArg(OpenMaya.MSyntax.kDouble)
        syntax.addArg(OpenMaya.MSyntax.kDouble)
        syntax.addArg(OpenMaya.MSyntax.kDouble)
        return syntax

# Initialize the script plug-in

def initializePlugin(mobject):
        mplugin = OpenMayaMPx.MFnPlugin(mobject, "Autodesk", "1.0", "Any")
        try:
                mplugin.registerContextCommand(kPluginCtxName, ctxCmdCreator, kPluginCmdName, cmdCreator, syntaxCreator)
        except:
                sys.stderr.write("Failed to register context command: %s\n" % kPluginCtxName)
                raise

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
        mplugin = OpenMayaMPx.MFnPlugin(mobject)
        try:
                mplugin.deregisterContextCommand(kPluginCtxName, kPluginCmdName)
        except:
                sys.stderr.write("Failed to deregister context command: %s\n" % kPluginCtxName)
                raise