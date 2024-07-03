#====================================================================================
#====================================================================================
#
# irsLimb_spineFeature_fk
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

class IrsLimb_spineFeature_fk(irsFeature.IrsFeature):
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

        lockAttrs = ('sx', 'sy', 'sz', 'v')

        # make root ---------------------------------------------------------------------------
        self.fkRootJoint = pymel.createNode('joint')
        self.setName(self.fkRootJoint, 'fkRootJoint')
        self.fkRootJoint.jointOrient.set([0,0,0], lock=True)
        self.fkRootJoint.setParent(self.root)
        ka_transforms.snap(self.fkRootJoint, limb.defaultXform_root, t=1, r=1)


        # make pelvis ---------------------------------------------------------------------------
        size = [limb.defaultXform_pelvisEnd.tx.get(), limb.sizeDict['pelvis'], limb.sizeDict['pelvis']]

        self.pelvis_controlStack = ka_controls.createControlStack(self.baseName+'_pelvis', sizeOfStack=3, size=size, side=limb.side)
        self.pelvis_controlStack[0].setParent(self.root)
        ka_transforms.snap(self.pelvis_controlStack[0], limb.defaultXform_pelvis, t=1, r=1)
        for attr in lockAttrs: self.pelvis_controlStack[-1].attr(attr).set(lock=True, keyable=False)
        ka_attr.addSeparatorAttr(node=self.pelvis_controlStack[-1])
        self.pelvis_controlStack[-1].addAttr('length', softMinValue=0.01, softMaxValue=5.0, defaultValue=1.0, keyable=True)

        self.fkPelvisJoint = pymel.createNode('joint')
        self.setName(self.fkPelvisJoint, 'fkPelvisJoint')
        self.fkPelvisJoint.jointOrient.set([0,0,0], lock=True)
        self.fkPelvisJoint.setParent(self.fkRootJoint)
        ka_transforms.snap(self.fkPelvisJoint, limb.defaultXform_pelvis, t=1, r=1)

        self.fkPelvisEndJoint = pymel.createNode('joint')
        self.setName(self.fkPelvisEndJoint, 'fkPelvisEndJoint')
        self.fkPelvisEndJoint.jointOrient.set([0,0,0], lock=True)
        self.fkPelvisEndJoint.setParent(self.fkPelvisJoint)
        ka_transforms.snap(self.fkPelvisEndJoint, limb.defaultXform_pelvisEnd, t=1, r=1)

        # make lowerSpines ---------------------------------------------------------------------------
        parent = self.root
        parentJoint = self.fkRootJoint
        self.lowerSpine_controlStacks = []
        self.lowerSpine_joints = []
        lockAttrs = ('tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v')

        for i in range(limb.lenLowerSpine):
            if i != limb.lenLowerSpine-1:
                nextDefaultXform = limb.defaultXform_lowerSpines[i+1]
            else:
                nextDefaultXform = limb.defaultXform_upperSpine

            size = [nextDefaultXform.tx.get(), limb.sizeDict['lowerSpines'][i], limb.sizeDict['lowerSpines'][i]]

            lowerSpine_controlStack = ka_controls.createControlStack(self.baseName+'_lowerSpine', sizeOfStack=3, size=size, side=limb.side, index=i)
            lowerSpine_controlStack[0].setParent(parent)
            ka_transforms.snap(lowerSpine_controlStack[0], limb.defaultXform_lowerSpines[i], t=1, r=1)
            if i == 0:
                pymel.pointConstraint(self.pelvis_controlStack[-1], lowerSpine_controlStack[-1])

            for attr in lockAttrs: lowerSpine_controlStack[-1].attr(attr).set(lock=True, keyable=False)
            ka_attr.addSeparatorAttr(node=lowerSpine_controlStack[-1])
            lowerSpine_controlStack[-1].addAttr('length', softMinValue=0.01, softMaxValue=5.0, defaultValue=1.0, keyable=True)
            self.lowerSpine_controlStacks.append(lowerSpine_controlStack)

            shadowJoint = pymel.createNode('joint')
            self.setName(shadowJoint, 'lowerSpaceShadowJoint', index=i)
            shadowJoint.setParent(lowerSpine_controlStack[-2])
            shadowJoint.jointOrient.set(0,0,0)
            ka_transforms.snap(shadowJoint, limb.defaultXform_lowerSpines[i], t=1, r=1)
            lowerSpine_controlStack[-1].rx >> shadowJoint.rx
            lowerSpine_controlStack[-1].ry >> shadowJoint.ry
            lowerSpine_controlStack[-1].rz >> shadowJoint.rz

            fkLowerSpineJoint = pymel.createNode('joint')
            self.setName(fkLowerSpineJoint, 'fkLowerSpineJoint', index=i)
            fkLowerSpineJoint.jointOrient.set([0,0,0], lock=True)
            fkLowerSpineJoint.setParent(parentJoint)
            ka_transforms.snap(fkLowerSpineJoint, limb.defaultXform_lowerSpines[i], t=1, r=1)
            self.lowerSpine_joints.append(fkLowerSpineJoint)

            parent = shadowJoint
            parentJoint = fkLowerSpineJoint
            lockAttrs = ('sx', 'sy', 'sz', 'v')

        # make upperSpine ---------------------------------------------------------------------------
        size = [limb.defaultXform_upperSpineEnd.tx.get(), limb.sizeDict['upperSpine'], limb.sizeDict['upperSpine']]

        self.upperSpine_controlStack = ka_controls.createControlStack(self.baseName+'_upperSpine', sizeOfStack=3, size=size, side=limb.side)
        self.upperSpine_controlStack[0].setParent(parent)
        ka_transforms.snap(self.upperSpine_controlStack[0], limb.defaultXform_upperSpine, t=1, r=1)
        for attr in lockAttrs: self.upperSpine_controlStack[-1].attr(attr).set(lock=True, keyable=False)
        ka_attr.addSeparatorAttr(node=self.upperSpine_controlStack[-1])
        self.upperSpine_controlStack[-1].addAttr('length', softMinValue=0.01, softMaxValue=5.0, defaultValue=1.0, keyable=True)

        self.fkUpperSpineJoint = pymel.createNode('joint')
        self.setName(self.fkUpperSpineJoint, 'fkUpperSpineJoint')
        self.fkUpperSpineJoint.jointOrient.set([0,0,0], lock=True)
        self.fkUpperSpineJoint.setParent(parentJoint)
        ka_transforms.snap(self.fkUpperSpineJoint, limb.defaultXform_upperSpine, t=1, r=1)

        self.fkUpperSpineEndJoint = pymel.createNode('joint')
        self.setName(self.fkUpperSpineEndJoint, 'fkUpperSpineEndJoint')
        self.fkUpperSpineEndJoint.jointOrient.set([0,0,0], lock=True)
        self.fkUpperSpineEndJoint.setParent(self.fkUpperSpineJoint)
        ka_transforms.snap(self.fkUpperSpineEndJoint, limb.defaultXform_upperSpineEnd, t=1, r=1)

        # drive joints ---------------------------------------------------------------------------
        pymel.parentConstraint(self.pelvis_controlStack[-1], self.fkPelvisJoint)
        for i, lowerSpine_controlStack in enumerate(self.lowerSpine_controlStacks):
            pymel.parentConstraint(self.lowerSpine_controlStacks[i][-1], self.lowerSpine_joints[i])

        pymel.parentConstraint(self.upperSpine_controlStack[-1], self.fkUpperSpineJoint)


        ## drive limb
        #limb.driveJoint(self.fkLegJoint, limb.drivenXform_leg, self.featureLabel)
        #limb.driveJoint(self.fkKneeJoint, limb.drivenXform_knee, self.featureLabel)
        #limb.driveJoint(self.fkAnkleJoint, limb.drivenXform_ankle, self.featureLabel)
        #limb.driveJoint(self.fkBallOfFootJoint, limb.drivenXform_ballOfFoot, self.featureLabel)
        #limb.driveJoint(self.fkToeJoint, limb.drivenXform_toe, self.featureLabel)

        ## flatten foot controls
        #for control in (self.ankle_controlStack[-1], self.ballOfFoot_controlStack[-1], self.toe_controlStack[-1]):
            #shape = control.getShape()
            #for cv in shape.cv:
                #cvPosition = cv.getPosition()
                #cvPositionWorldSpace = cv.getPosition(space='world')
                #if cvPosition[1]*self.sideInt > 0.0:
                    #pymel.xform(cv, worldSpace=True, translation=[cvPositionWorldSpace[0], 0, cvPositionWorldSpace[2]])


        ## visibility
        #self.fkLegJoint.v.set(0)

        #limb.driveVisibility(self.root, self.featureLabel)
