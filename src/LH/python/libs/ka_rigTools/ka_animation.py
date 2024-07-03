#====================================================================================
#====================================================================================
#
# ka_util
#
# DESCRIPTION:
#   collection of small utility scripts that do simple yet essential tasks within maya
#
# AUTHOR:
#   Kris Andrews (3dkris@3dkris.com)
#
#====================================================================================
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are
#met:

    #(1) Redistributions of source code must retain the above copyright
    #notice, this list of conditions and the following disclaimer.

    #(2) Redistributions in binary form must reproduce the above copyright
    #notice, this list of conditions and the following disclaimer in
    #the documentation and/or other materials provided with the
    #distribution.

    #(3)The name of the author may not be used to
    #endorse or promote products derived from this software without
    #specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
#INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#POSSIBILITY OF SUCH DAMAGE.
#====================================================================================

from traceback import print_exc as printError

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel

import ka_rigTools.ka_clipBoard as ka_clipBoard    #;reload(ka_clipBoard)
import ka_rigTools.ka_pymel as ka_pymel            #;reload(ka_pymel)

def advanceNFrames(numberOfFrames=20):
    currentTime = pymel.currentTime( query=True )
    currentTime += numberOfFrames
    pymel.currentTime( currentTime )


def storeAllControls(allControls=None):
    if not allControls:
        allControls = pymel.ls(selection=True)
    ka_clipBoard.add('allControls', allControls)


def getAllControls():
    allControls = ka_clipBoard.get('allControls', [])
    return allControls


def selectAllControls():
    return pymel.select(getAllControls())


def keyAllControls():
    allControls = ka_clipBoard.get('allControls', [])
    for control in allControls:
        pymel.setKeyframe(control, shape=False)


def deleteAnimationOnAllControls():
    allControls = ka_clipBoard.get('allControls', [])
    for control in allControls:
        for attr in control.listAttr(keyable=True):
            inputs = attr.inputs()
            for input in inputs:
                nodeType = input.nodeType()
                if nodeType[:-1] == 'animCurveT':
                    pymel.delete(input)


def storePose(poseName='default', space='local'):
    tPoseDict = {}

    for control in getAllControls():
        if 'transform' in control.nodeType(inherited=True):
            controlMatrix = pymel.xform(control, query=True, matrix=True, objectSpace=True)
            tPoseDict[control] = controlMatrix


    ka_clipBoard.add('tPoseData', tPoseDict)


def getTPose(space='local'):
    return ka_clipBoard.get('tPoseData', {})


def applyPose(poseName='default'):
    tPoseDict = ka_clipBoard.get('tPoseData', [])
    for control in tPoseDict:
        matrix = tPoseDict[control]
        pymel.xform(control, matrix=matrix, objectSpace=True)

