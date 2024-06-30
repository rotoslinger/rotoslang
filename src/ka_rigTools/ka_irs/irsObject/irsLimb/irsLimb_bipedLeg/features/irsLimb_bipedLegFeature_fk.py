#====================================================================================
#====================================================================================
#
# irsLimb_bipedLegFeature_fk
#
# DESCRIPTION:
#   an fk feature for irsLimb_bipedLeg
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


import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel

import ka_rigTools.ka_python as ka_python
import ka_rigTools.ka_controls as ka_controls
import ka_rigTools.ka_transforms as ka_transforms
import ka_rigTools.ka_attr as ka_attr

import ka_rigTools.ka_irs.irsObject.irsFeature as irsFeature

class IrsLimb_bipedLegFeature_fk(irsFeature.IrsFeature):
    featureSlot = 0
    featureLabel = 'fk'

    def __init__(self, root=None, **kwargs):

        # set defaults
        kwargs['name'] = kwargs['name']+'_fk'

        # init superClass
        self.__init__IrsFeature__(root, **kwargs)

        self.irsLimb = kwargs['irsLimb']
        self.controls = []

        # wrap or create
        if root:
            self.wrap(root)

        else:
            self.create()



    def create(self):
        self.startIrsObject()
        try:
            self._create()
        except:
            ka_python.printError()

        self.finishIrsObject()


    def _create(self):
        limb = self.irsLimb

        lockAttrs = ('tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v')

        # make leg ---------------------------------------------------------------------------
        size = [limb.defaultXform_knee.tx.get(), limb.sizeDict['leg'], limb.sizeDict['leg']]
        self.leg_controlStack = ka_controls.createControlStack(self.baseName+'_leg',size=size, side=limb.side)
        self.leg_controlStack[0].setParent(self.root)
        ka_transforms.snap(self.leg_controlStack[0], limb.defaultXform_leg, t=1, r=1)
        for attr in lockAttrs: self.leg_controlStack[-1].attr(attr).set(lock=True, keyable=False)
        ka_attr.addSeparatorAttr(node=self.leg_controlStack[-1])
        self.leg_controlStack[-1].addAttr('length', softMinValue=0.01, softMaxValue=5.0, defaultValue=1.0, keyable=True)

        self.fkLegJoint = pymel.createNode('joint')
        self.setName(self.fkLegJoint, 'fkLegJoint')
        self.fkLegJoint.jointOrient.set([0,0,0], lock=True)
        self.fkLegJoint.setParent(self.root)
        ka_transforms.snap(self.fkLegJoint, limb.defaultXform_leg, t=1, r=1)

        # make knee ---------------------------------------------------------------------------
        size = [limb.defaultXform_ankle.tx.get(), limb.sizeDict['knee'], limb.sizeDict['knee']]
        self.knee_controlStack = ka_controls.createControlStack(self.baseName+'_knee', size=size, side=limb.side)
        self.knee_controlStack[0].setParent(self.leg_controlStack[-1])
        ka_transforms.snap(self.knee_controlStack[0], limb.defaultXform_knee, t=1, r=1)
        for attr in lockAttrs: self.knee_controlStack[-1].attr(attr).set(lock=True, keyable=False)
        ka_attr.addSeparatorAttr(node=self.knee_controlStack[-1])
        self.knee_controlStack[-1].addAttr('length', softMinValue=0.01, softMaxValue=5.0, defaultValue=1.0, keyable=True)

        self.fkKneeJoint = pymel.createNode('joint')
        self.setName(self.fkKneeJoint, 'fkKneeJoint')
        self.fkKneeJoint.jointOrient.set([0,0,0], lock=True)
        self.fkKneeJoint.setParent(self.fkLegJoint)
        ka_transforms.snap(self.fkKneeJoint, limb.defaultXform_knee, t=1, r=1)

        # make ankle ---------------------------------------------------------------------------
        size = [limb.defaultXform_ballOfFoot.tx.get(), limb.sizeDict['ankle'], limb.sizeDict['ankle']]
        self.ankle_controlStack = ka_controls.createControlStack(self.baseName+'_ankle', size=size, side=limb.side)
        self.ankle_controlStack[0].setParent(self.knee_controlStack[-1])
        ka_transforms.snap(self.ankle_controlStack[0], limb.defaultXform_ankle, t=1, r=1)
        for attr in lockAttrs: self.ankle_controlStack[-1].attr(attr).set(lock=True, keyable=False)
        ka_attr.addSeparatorAttr(node=self.ankle_controlStack[-1])
        self.ankle_controlStack[-1].addAttr('length', softMinValue=0.01, softMaxValue=5.0, defaultValue=1.0, keyable=True)

        self.fkAnkleJoint = pymel.createNode('joint')
        self.setName(self.fkAnkleJoint, 'fkAnkleJoint')
        self.fkAnkleJoint.jointOrient.set([0,0,0], lock=True)
        self.fkAnkleJoint.setParent(self.fkKneeJoint)
        ka_transforms.snap(self.fkAnkleJoint, limb.defaultXform_ankle, t=1, r=1)

        # make ballOfFoot ---------------------------------------------------------------------------
        size = [limb.defaultXform_toe.tx.get(), limb.sizeDict['ballOfFoot'], limb.sizeDict['ballOfFoot']]
        self.ballOfFoot_controlStack = ka_controls.createControlStack(self.baseName+'_ballOfFoot', size=size, side=limb.side)
        self.ballOfFoot_controlStack[0].setParent(self.ankle_controlStack[-1])
        ka_transforms.snap(self.ballOfFoot_controlStack[0], limb.defaultXform_ballOfFoot, t=1, r=1)
        for attr in lockAttrs: self.ballOfFoot_controlStack[-1].attr(attr).set(lock=True, keyable=False)
        ka_attr.addSeparatorAttr(node=self.ballOfFoot_controlStack[-1])
        self.ballOfFoot_controlStack[-1].addAttr('length', softMinValue=0.01, softMaxValue=5.0, defaultValue=1.0, keyable=True)

        self.fkBallOfFootJoint = pymel.createNode('joint')
        self.setName(self.fkBallOfFootJoint, 'fkBallOfFootJoint')
        self.fkBallOfFootJoint.jointOrient.set([0,0,0], lock=True)
        self.fkBallOfFootJoint.setParent(self.fkAnkleJoint)
        ka_transforms.snap(self.fkBallOfFootJoint, limb.defaultXform_ballOfFoot, t=1, r=1)

        # make toe ---------------------------------------------------------------------------
        size = [limb.defaultXform_toeEnd.tx.get(), limb.sizeDict['toe'], limb.sizeDict['toe']]
        self.toe_controlStack = ka_controls.createControlStack(self.baseName+'_toe', size=size, side=limb.side)
        self.toe_controlStack[0].setParent(self.ballOfFoot_controlStack[-1])
        ka_transforms.snap(self.toe_controlStack[0], limb.defaultXform_toe, t=1, r=1)
        for attr in lockAttrs: self.toe_controlStack[-1].attr(attr).set(lock=True, keyable=False)
        ka_attr.addSeparatorAttr(node=self.toe_controlStack[-1])
        self.toe_controlStack[-1].addAttr('length', softMinValue=0.01, softMaxValue=5.0, defaultValue=1.0, keyable=True)

        self.fkToeJoint = pymel.createNode('joint')
        self.setName(self.fkToeJoint, 'fkToeJoint')
        self.fkToeJoint.jointOrient.set([0,0,0], lock=True)
        self.fkToeJoint.setParent(self.fkBallOfFootJoint)
        ka_transforms.snap(self.fkToeJoint, limb.defaultXform_toe, t=1, r=1)

        self.fkToeJointEnd = pymel.createNode('joint')
        self.setName(self.fkToeJointEnd, 'fkToeJointEnd')
        self.fkToeJointEnd.jointOrient.set([0,0,0], lock=True)
        self.fkToeJointEnd.setParent(self.fkToeJoint)
        ka_transforms.snap(self.fkToeJointEnd, limb.defaultXform_toeEnd, t=1, r=1)

        # drive joints
        pymel.parentConstraint(self.leg_controlStack[-1], self.fkLegJoint)
        pymel.parentConstraint(self.knee_controlStack[-1], self.fkKneeJoint)
        pymel.parentConstraint(self.ankle_controlStack[-1], self.fkAnkleJoint)
        pymel.parentConstraint(self.ballOfFoot_controlStack[-1], self.fkBallOfFootJoint)
        pymel.parentConstraint(self.toe_controlStack[-1], self.fkToeJoint)

        # drive limb
        limb.driveJoint(self.fkLegJoint, limb.drivenXform_leg, self.featureLabel)
        limb.driveJoint(self.fkKneeJoint, limb.drivenXform_knee, self.featureLabel)
        limb.driveJoint(self.fkAnkleJoint, limb.drivenXform_ankle, self.featureLabel)
        limb.driveJoint(self.fkBallOfFootJoint, limb.drivenXform_ballOfFoot, self.featureLabel)
        limb.driveJoint(self.fkToeJoint, limb.drivenXform_toe, self.featureLabel)

        # flatten foot controls
        for control in (self.ankle_controlStack[-1], self.ballOfFoot_controlStack[-1], self.toe_controlStack[-1]):
            shape = control.getShape()
            for cv in shape.cv:
                cvPosition = cv.getPosition()
                cvPositionWorldSpace = cv.getPosition(space='world')
                if cvPosition[1]*self.sideInt > 0.0:
                    pymel.xform(cv, worldSpace=True, translation=[cvPositionWorldSpace[0], 0, cvPositionWorldSpace[2]])


        # visibility
        self.fkLegJoint.v.set(0)

        limb.driveVisibility(self.root, self.featureLabel)
