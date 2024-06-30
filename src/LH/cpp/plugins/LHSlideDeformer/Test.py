import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaUI as OpenMayaUI

class MoveContext(OpenMayaMPx.MPxSelectionContext):
        kTop, kFront, kSide, kPersp = 0, 1, 2, 3
        
        def __init__(self):
                OpenMayaMPx.MPxSelectionContext.__init__(self)
#                 self._setTitleString("moveTool")
#                 self.setImage("moveTool.xpm", OpenMayaMPx.MPxContext.kImage1)
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
#                         fnCamera = OpenMaya.MFnCamera(camera)
#                         upDir = fnCamera.upDirection(spc)
#                         rightDir = fnCamera.rightDirection(spc)

                        # Determine the camera used in the current view
                        #
#                         if fnCamera.isOrtho():
#                                 if upDir.isEquivalent(OpenMaya.MVector.zNegAxis, kVectorEpsilon):
#                                         self.__currWin = MoveContext.kTop
#                                 elif rightDir.isEquivalent(OpenMaya.MVector.xAxis, kVectorEpsilon):
#                                         self.__currWin = MoveContext.kFront
#                                 else:
#                                         self.__currWin = MoveContext.kSide
#                         else:
#                                 self.__currWin = MoveContext.kPersp

                        # Create an instance of the move tool command.
                        #
                        newCmd = self._newToolCommand()
                        self.__cmd = kTrackingDictionary.get(OpenMayaMPx.asHashable(newCmd), None)
                        self.__cmd.setVector(0.0, 0.0, 0.0)
                        
                        newWeightCmd = self._newToolCommand()
                        self.__weightCmd = kTrackingDictionary.get(OpenMayaMPx.asHashable(newWeightCmd), None)
                        self.__weightCmd.setWeight(0.0)
                        
                        

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
                        self.__view.viewToWorld(self.__endPos_x, self.__endPos_y, endW, vec)
                        downButton = event.mouseButton()
                        shiftButton = event.modifiers()

                        # We reset the the move vector each time a drag event occurs
                        # and then recalculate it based on the start position.
                        #
                        self.__cmd.undoIt()
                        if downButton == OpenMayaUI.MEvent.kMiddleMouse and shiftButton != OpenMayaUI.MEvent.shiftKey and shiftButton != OpenMayaUI.MEvent.controlKey:
                                self.__cmd.setWeight(endW.x - startW.x)
                        elif downButton == OpenMayaUI.MEvent.kMiddleMouse and shiftButton == OpenMayaUI.MEvent.shiftKey and shiftButton != OpenMayaUI.MEvent.controlKey:
                                self.__cmd.setWeight((endW.x - startW.x)*20)
                        elif downButton == OpenMayaUI.MEvent.kMiddleMouse and shiftButton == OpenMayaUI.MEvent.controlKey and shiftButton != OpenMayaUI.MEvent.shiftKey:
                                self.__cmd.setWeight((endW.x - startW.x)*.1)
                        else:
                                self.__cmd.setWeight(endW.x - startW.x)

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
MoveContext
print("stuff")