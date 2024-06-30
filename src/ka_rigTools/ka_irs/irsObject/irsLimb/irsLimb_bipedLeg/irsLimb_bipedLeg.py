#====================================================================================
#====================================================================================
#
# irsLimb_bipedLeg
#
# DESCRIPTION:
#   a limb representing a bipedLeg
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

import ka_rigTools.ka_math as ka_math
import ka_rigTools.ka_python as ka_python
import ka_rigTools.ka_attr as ka_attr
import ka_rigTools.ka_controls as ka_controls
import ka_rigTools.ka_transforms as ka_transforms

import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb as irsLimb
import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_bipedLeg.features.irsLimb_bipedLegFeature_fk as irsLimb_bipedLegFeature_fk
import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_bipedLeg.features.irsLimb_bipedLegFeature_ik as irsLimb_bipedLegFeature_ik


DEFAULT_MATRICES = {'leg':[0.12940952255126015, -0.96592582628906831, 0.22414386804201353, 0.0, -0.48296291314453477, -0.25881904510252096, -0.83651630373780761, 0.0, 0.86602540378443837, -3.3306690738754686e-16, -0.50000000000000044, 0.0, 8.3186205731822778, 23.684880767565275, -0.015254908100829512, 1.0],
                    'knee':[-0.12605479060041203, -0.96769869229360117, -0.21833330185736818, 0.0, -0.48384934614680097, 0.25210958120082283, -0.83805165073523891, 0.0, 0.86602540378443837, -3.3306690738754686e-16, -0.50000000000000044, 0.0, 9.767520062279031, 12.870147750825865, 2.4943126220753538, 1.0],
                    'ankle':[0.43135196369013024, -0.50570933715196054, 0.74712351705591051, 0.0, -0.25285466857598093, -0.86270392738026003, -0.43795713290458721, 0.0, 0.86602540378443837, -3.3306690738754686e-16, -0.50000000000000044, 0.0, 8.4956272251208755, 3.1060679455834226, 0.29132960633450677, 1.0],
                    'ballOfFoot':[0.49986809646614561, 0.02296833779904367, 0.86579694016210373, 0.0, 0.011484168899521391, -0.9997361929322901, 0.01989116401667429, 0.0, 0.86602540378443837, -3.3306690738754686e-16, -0.50000000000000044, 0.0, 9.8905837677823225, 1.470645812552678, 2.7074652125747574, 1.0],
                    'toe':[0.49986809646614561, 0.02296833779904367, 0.86579694016210373, 0.0, 0.011484168899521391, -0.9997361929322901, 0.01989116401667429, 0.0, 0.86602540378443837, -3.3306690738754686e-16, -0.50000000000000044, 0.0, 11.159641085711382, 1.5289574699091055, 4.9055369649449725, 1.0],
                    'toeEnd':[0.49986809646614561, 0.02296833779904367, 0.86579694016210373, 0.0, 0.011484168899521391, -0.9997361929322901, 0.01989116401667429, 0.0, 0.86602540378443837, -3.3306690738754686e-16, -0.50000000000000044, 0.0, 11.745931822037706, 1.5558968240619167, 5.9210223082691407, 1.0],
                    'rollPivot_heel':[0.86602540378443893, 0.0, -0.49999999999999956, 0.0, 0.0, 1.0, 0.0, 0.0, 0.49999999999999956, 0.0, 0.86602540378443893, 0.0, 7.0, 0.0, -2.0000000000000009, 1.0],
                    'rollPivot_toe':[0.86602540378443893, 0.0, -0.49999999999999956, 0.0, 0.0, 1.0, 0.0, 0.0, 0.49999999999999956, 0.0, 0.86602540378443893, 0.0, 11.745931822037711, 0.378, 5.9210223082691398, 1.0],
                    'rollPivot_innerBank':[0.86602540378443893, 0.0, -0.49999999999999956, 0.0, 0.0, 1.0, 0.0, 0.0, 0.49999999999999956, 0.0, 0.86602540378443893, 0.0, 8.3978763612994403, 0.0, 4.149319910977348, 1.0],
                    'rollPivot_outerBank':[0.86602540378443893, 0.0, -0.49999999999999956, 0.0, 0.0, 1.0, 0.0, 0.0, 0.49999999999999956, 0.0, 0.86602540378443893, 0.0, 12.0, 0.0, 2.0, 1.0],
                    'groundPlane':[0.50000000620758756, -6.4623485355705287e-27, 0.86602540020048635, 0.0, -1.0694067571519877e-10, -1.0, 6.1742228933544593e-11, 0.0, 0.86602540020048635, -1.2348445633400802e-10, -0.50000000620758756, 0.0, 8.4956272443553615, 0.0, 0.29132963964962516, 1.0]
                   }

#DEFAULT_SCALE_MATRICES = {'leg':[2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                         #'knee':[1.5, 0.0, 0.0, 0.0, 0.0, 1.5, 0.0, 0.0, 0.0, 0.0, 1.5, 0.0, 0.0, 0.0, 0.0, 1.5],
                         #'ankle':[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                         #'ballOfFoot':[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                         #'toe':[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                         #'toeEnd':[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                        #}

DEFAULT_SIZES = {'leg':5,
                 'knee':3,
                 'ankle':2.5,
                 'ballOfFoot':2.5,
                 'toe':2.5,
                 'toeEnd':2,
                 }

BENDY_VIS_ATTRIBUTE_NAME = 'bendyVis'
KNEE_IK_VIS_ATTRIBUTE_NAME = 'kneeIk'


class IrsLimb_bipedLeg(irsLimb.IrsLimb):
    features = [irsLimb_bipedLegFeature_fk.IrsLimb_bipedLegFeature_fk,
                irsLimb_bipedLegFeature_ik.IrsLimb_bipedLegFeature_ik,
               ]


    def __init__(self, root=None, **kwargs): #=======================================================================


        # modify kwargs --------------------------------------------------------------------------------------
        kwargs['name'] = kwargs.get('name', 'bipedLeg')


        # init superClass --------------------------------------------------------------------------------------
        self.__init__IrsLimb__(root, **kwargs)

        # set object variables --------------------------------------------------------------------------------------
        self.defaultXformsGroup = None
        self.defaultXform_leg = None
        self.defaultXform_knee = None
        self.defaultXform_ankle = None
        self.defaultXform_ballOfFoot = None
        self.defaultXform_toe = None
        self.defaultXform_toeEnd = None
        self.defaultXform_rollPivot_toe = None
        self.defaultXform_rollPivot_heel = None
        self.defaultXform_rollPivot_innerBank = None
        self.defaultXform_rollPivot_outerBank = None
        self.defaultXform_groundPlane = None
        self.defaultXform_legBendyControls = []
        self.defaultXform_kneeBendyControls = []

        self.outputXforms = []
        self.outputTransformsGroup = None
        self.outputXform_leg = None
        self.outputXform_knee = None
        self.outputXform_ankle = None
        self.outputXform_ballOfFoot = None
        self.outputXform_toe = None
        self.outputXform_toeEnd = None
        self.outputXform_legTwists = []
        self.outputXform_kneeTwists = []

        self.drivenTransformsGroup = None
        self.drivenXform_leg = None
        self.drivenXform_knee = None
        self.drivenXform_ankle = None
        self.drivenXform_ballOfFoot = None
        self.drivenXform_toe = None
        self.drivenXform_toeEnd = None
        self.drivenXform_legTwists = []
        self.drivenXform_kneeTwists = []

        self.kneeIkControlStack = None

        self.matrixDict = kwargs.get('matrixDict', DEFAULT_MATRICES)
        self.sizeDict = kwargs.get('sizeDict', DEFAULT_SIZES)

        self.rotationOfLeg = None
        self.rotationOfKnee = None

        self.posOfLeg = None
        self.posOfKnee = None
        self.posOfAnkle = None

        self.vectorOfKnee = None
        self.vectorOfAnkle = None

        self.lenLegTwist = 5
        self.lenKneeTwist = 5

        self.lenLegBendyControls = 3
        self.lenKneeBendyControls = 3

        # wrap or create
        if root:
            self.wrap(root)

        else:
            self.create()


    def create(self): #=============================================================================================
        self.startIrsObject()

        try:
            self._create()
        except:
            ka_python.printError()

        self.finishIrsObject()

        self.addFeature('fk')
        self.addFeature('ik')

    def _create(self): #=============================================================================================
        self.createSwitchControl(modes=['fk', 'ik'])


        # create default xforms --------------------------------------------------------------------------------------
        self.defaultXformsGroup = pymel.createNode('transform')
        self.setName(self.defaultXformsGroup, 'defaultXform_group')

        self.defaultXform_leg = pymel.createNode('transform')
        self.defaultXform_knee = pymel.createNode('transform')
        self.defaultXform_ankle = pymel.createNode('transform')
        self.defaultXform_ballOfFoot = pymel.createNode('transform')
        self.defaultXform_toe = pymel.createNode('transform')
        self.defaultXform_toeEnd = pymel.createNode('transform')
        self.defaultXform_rollPivot_heel = pymel.createNode('transform')
        self.defaultXform_rollPivot_toe = pymel.createNode('transform')
        self.defaultXform_rollPivot_innerBank = pymel.createNode('transform')
        self.defaultXform_rollPivot_outerBank = pymel.createNode('transform')
        self.defaultXform_groundPlane = pymel.createNode('transform')

        self.setName(self.defaultXform_leg, 'defaultXform_leg')
        self.setName(self.defaultXform_knee, 'defaultXform_knee')
        self.setName(self.defaultXform_ankle, 'defaultXform_ankle')
        self.setName(self.defaultXform_ballOfFoot, 'defaultXform_ballOfFoot')
        self.setName(self.defaultXform_toe, 'defaultXform_toe')
        self.setName(self.defaultXform_toeEnd, 'defaultXform_toeEnd')
        self.setName(self.defaultXform_rollPivot_heel, 'defaultXform_rollPivot_heel')
        self.setName(self.defaultXform_rollPivot_toe, 'defaultXform_rollPivot_toe')
        self.setName(self.defaultXform_rollPivot_innerBank, 'defaultXform_rollPivot_innerBank')
        self.setName(self.defaultXform_rollPivot_outerBank, 'defaultXform_rollPivot_outerBank')
        self.setName(self.defaultXform_groundPlane, 'defaultXform_groundPlane')

        pymel.xform(self.defaultXform_leg, matrix=self.matrixDict['leg'], worldSpace=True)
        pymel.xform(self.defaultXform_knee, matrix=self.matrixDict['knee'], worldSpace=True)
        pymel.xform(self.defaultXform_ankle, matrix=self.matrixDict['ankle'], worldSpace=True)
        pymel.xform(self.defaultXform_ballOfFoot, matrix=self.matrixDict['ballOfFoot'], worldSpace=True)
        pymel.xform(self.defaultXform_toe, matrix=self.matrixDict['toe'], worldSpace=True)
        pymel.xform(self.defaultXform_toeEnd, matrix=self.matrixDict['toeEnd'], worldSpace=True)
        pymel.xform(self.defaultXform_rollPivot_heel, matrix=self.matrixDict['rollPivot_heel'], worldSpace=True)
        pymel.xform(self.defaultXform_rollPivot_toe, matrix=self.matrixDict['rollPivot_toe'], worldSpace=True)
        pymel.xform(self.defaultXform_rollPivot_innerBank, matrix=self.matrixDict['rollPivot_innerBank'], worldSpace=True)
        pymel.xform(self.defaultXform_rollPivot_outerBank, matrix=self.matrixDict['rollPivot_outerBank'], worldSpace=True)
        pymel.xform(self.defaultXform_groundPlane, matrix=self.matrixDict['groundPlane'], worldSpace=True)

        self.defaultXformsGroup.setParent(self.root)
        self.defaultXform_leg.setParent(self.defaultXformsGroup)
        self.defaultXform_knee.setParent(self.defaultXform_leg)
        self.defaultXform_ankle.setParent(self.defaultXform_knee)
        self.defaultXform_ballOfFoot.setParent(self.defaultXform_ankle)
        self.defaultXform_toe.setParent(self.defaultXform_ballOfFoot)
        self.defaultXform_toeEnd.setParent(self.defaultXform_toe)
        self.defaultXform_rollPivot_innerBank.setParent(self.defaultXform_toeEnd)
        self.defaultXform_rollPivot_outerBank.setParent(self.defaultXform_toeEnd)
        self.defaultXform_rollPivot_heel.setParent(self.defaultXform_toeEnd)
        self.defaultXform_rollPivot_toe.setParent(self.defaultXform_toeEnd)
        self.defaultXform_groundPlane.setParent(self.defaultXformsGroup)


        self.rotationOfLeg = pymel.xform(self.defaultXform_leg, query=True, rotation=True, worldSpace=True)
        self.rotationOfKnee = pymel.xform(self.defaultXform_knee, query=True, rotation=True, worldSpace=True)

        self.posOfLeg = pymel.xform(self.defaultXform_leg, query=True, translation=True, worldSpace=True)
        self.posOfKnee = pymel.xform(self.defaultXform_knee, query=True, translation=True, worldSpace=True)
        self.posOfAnkle = pymel.xform(self.defaultXform_ankle, query=True, translation=True, worldSpace=True)

        self.vectorOfKnee = ka_math.subtractVectors(self.posOfKnee, self.posOfLeg)
        self.vectorOfAnkle = ka_math.subtractVectors(self.posOfAnkle, self.posOfKnee)


        currentParent = self.defaultXform_leg
        for i in range(self.lenLegBendyControls+2):
            if 1 != self.lenLegBendyControls+2:
                defaultXform_legBendyControl = pymel.createNode('transform')
                self.setName(defaultXform_legBendyControl, 'defaultXform_legBendyControl', index=i)
                defaultXform_legBendyControl.setParent(currentParent)

                moveVector = ka_math.multiplyVectors(self.vectorOfKnee, (float(i)/(self.lenLegBendyControls+1)))
                finalPosition = ka_math.addVectors(self.posOfLeg, moveVector)

                pymel.xform(defaultXform_legBendyControl, translation=finalPosition, worldSpace=True)
                pymel.xform(defaultXform_legBendyControl, rotation=self.rotationOfLeg, worldSpace=True)

                currentParent = defaultXform_legBendyControl
                self.defaultXform_legBendyControls.append(defaultXform_legBendyControl)

        currentParent = self.defaultXform_knee
        for i in range(self.lenKneeBendyControls+2):
            if 1 != self.lenKneeBendyControls+2:
                defaultXform_kneeBendyControl = pymel.createNode('transform')
                self.setName(defaultXform_kneeBendyControl, 'defaultXform_kneeBendyControl', index=i)
                defaultXform_kneeBendyControl.setParent(currentParent)

                moveVector = ka_math.multiplyVectors(self.vectorOfAnkle, (float(i)/(self.lenKneeBendyControls+1)))
                finalPosition = ka_math.addVectors(self.posOfKnee, moveVector)

                pymel.xform(defaultXform_kneeBendyControl, translation=finalPosition, worldSpace=True)
                pymel.xform(defaultXform_kneeBendyControl, rotation=self.rotationOfKnee, worldSpace=True)

                currentParent = defaultXform_kneeBendyControl
                self.defaultXform_kneeBendyControls.append(defaultXform_kneeBendyControl)


        # create outputXforms --------------------------------------------------------------------------------------
        self.outputXformsGroup = pymel.createNode('transform')
        self.setName(self.outputXformsGroup, 'outputXform_group')

        self.outputXform_leg = pymel.createNode('joint')
        self.outputXform_knee = pymel.createNode('joint')
        self.outputXform_ankle = pymel.createNode('joint')
        self.outputXform_ballOfFoot = pymel.createNode('joint')
        self.outputXform_toe = pymel.createNode('joint')
        self.outputXform_toeEnd = pymel.createNode('joint')

        self.setName(self.outputXform_leg, 'outputXform_leg')
        self.setName(self.outputXform_knee, 'outputXform_knee')
        self.setName(self.outputXform_ankle, 'outputXform_ankle')
        self.setName(self.outputXform_ballOfFoot, 'outputXform_ballOfFoot')
        self.setName(self.outputXform_toe, 'outputXform_toe')
        self.setName(self.outputXform_toeEnd, 'outputXform_toeEnd')

        self.outputXform_leg.jointOrient.set([0,0,0], lock=True)
        self.outputXform_knee.jointOrient.set([0,0,0], lock=True)
        self.outputXform_ankle.jointOrient.set([0,0,0], lock=True)
        self.outputXform_ballOfFoot.jointOrient.set([0,0,0], lock=True)
        self.outputXform_toe.jointOrient.set([0,0,0], lock=True)
        self.outputXform_toeEnd.jointOrient.set([0,0,0], lock=True)

        self.outputXformsGroup.setParent(self.root)
        self.outputXform_leg.setParent(self.outputXformsGroup)
        self.outputXform_knee.setParent(self.outputXform_leg)
        self.outputXform_ankle.setParent(self.outputXform_knee)
        self.outputXform_ballOfFoot.setParent(self.outputXform_ankle)
        self.outputXform_toe.setParent(self.outputXform_ballOfFoot)
        self.outputXform_toeEnd.setParent(self.outputXform_toe)

        pymel.xform(self.outputXform_leg, matrix=self.matrixDict['leg'], worldSpace=True)
        pymel.xform(self.outputXform_knee, matrix=self.matrixDict['knee'], worldSpace=True)
        pymel.xform(self.outputXform_ankle, matrix=self.matrixDict['ankle'], worldSpace=True)
        pymel.xform(self.outputXform_ballOfFoot, matrix=self.matrixDict['ballOfFoot'], worldSpace=True)
        pymel.xform(self.outputXform_toe, matrix=self.matrixDict['toe'], worldSpace=True)
        pymel.xform(self.outputXform_toeEnd, matrix=self.matrixDict['toeEnd'], worldSpace=True)


        self.outputXforms = [self.outputXform_leg]
        currentParent = self.outputXform_leg
        for i in range(self.lenLegTwist):
            if i != 0:
                outputXform_legTwist = pymel.createNode('joint')
                outputXform_legTwist.jointOrient.set([0,0,0], lock=True)
                outputXform_legTwist.setParent(currentParent)
                self.setName(outputXform_legTwist, 'outputXform_legTwist', index=i)

                moveVector = ka_math.multiplyVectors(self.vectorOfKnee, (float(i)/self.lenLegTwist))
                finalPosition = ka_math.addVectors(self.posOfLeg, moveVector)

                pymel.xform(outputXform_legTwist, translation=finalPosition, worldSpace=True)
                pymel.xform(outputXform_legTwist, rotation=self.rotationOfLeg, worldSpace=True)

                self.outputXform_legTwists.append(outputXform_legTwist)
                currentParent = outputXform_legTwist
                self.outputXforms.append(outputXform_legTwist)

        self.outputXforms.append(self.outputXform_knee)
        currentParent = self.outputXform_knee
        for i in range(self.lenLegTwist):
            if i != 0:
                outputXform_kneeTwist = pymel.createNode('joint')
                outputXform_kneeTwist.jointOrient.set([0,0,0], lock=True)
                outputXform_kneeTwist.setParent(currentParent)
                self.setName(outputXform_kneeTwist, 'outputXform_kneeTwist', index=i)

                moveVector = ka_math.multiplyVectors(self.vectorOfAnkle, (float(i)/self.lenKneeTwist))
                finalPosition = ka_math.addVectors(self.posOfKnee, moveVector)

                pymel.xform(outputXform_kneeTwist, translation=finalPosition, worldSpace=True)
                pymel.xform(outputXform_kneeTwist, rotation=self.rotationOfKnee, worldSpace=True)

                self.outputXform_kneeTwists.append(outputXform_kneeTwist)
                currentParent = outputXform_kneeTwist
                self.outputXforms.append(outputXform_kneeTwist)

        self.outputXform_knee.setParent(self.outputXform_legTwists[-1])
        self.outputXform_ankle.setParent(self.outputXform_kneeTwists[-1])
        self.outputXforms.extend([self.outputXform_ankle, self.outputXform_ballOfFoot, self.outputXform_toe])


        # create drivenXforms --------------------------------------------------------------------------------------
        self.drivenXformsGroup = pymel.createNode('transform')
        self.setName(self.drivenXformsGroup, 'drivenXform_group')

        bendyWorldSpaceGroup = pymel.createNode('transform')
        self.setName(bendyWorldSpaceGroup, 'bendyWorldSpaceGroup',)
        bendyWorldSpaceGroup.inheritsTransform.set(0)
        bendyWorldSpaceGroup.setParent(self.drivenXformsGroup)

        self.drivenXform_leg = pymel.createNode('joint')
        self.drivenXform_knee = pymel.createNode('joint')
        self.drivenXform_ankle = pymel.createNode('joint')
        self.drivenXform_ballOfFoot = pymel.createNode('joint')
        self.drivenXform_toe = pymel.createNode('joint')
        self.drivenXform_toeEnd = pymel.createNode('joint')
        self.drivenXforms = [self.drivenXform_leg, self.drivenXform_knee, self.drivenXform_ankle, self.drivenXform_ballOfFoot, self.drivenXform_toe, self.drivenXform_toeEnd]

        self.setName(self.drivenXform_leg, 'drivenXform_leg')
        self.setName(self.drivenXform_knee, 'drivenXform_knee')
        self.setName(self.drivenXform_ankle, 'drivenXform_ankle')
        self.setName(self.drivenXform_ballOfFoot, 'drivenXform_ballOfFoot')
        self.setName(self.drivenXform_toe, 'drivenXform_toe')
        self.setName(self.drivenXform_toeEnd, 'drivenXform_toeEnd')

        for drivenXForm in self.drivenXforms:
            drivenXForm.jointOrient.set([0,0,0], lock=True)

        self.drivenXformsGroup.setParent(self.root)
        self.drivenXform_leg.setParent(self.drivenXformsGroup)
        self.drivenXform_knee.setParent(self.drivenXform_leg)
        self.drivenXform_ankle.setParent(self.drivenXform_knee)
        self.drivenXform_ballOfFoot.setParent(self.drivenXform_ankle)
        self.drivenXform_toe.setParent(self.drivenXform_ballOfFoot)
        self.drivenXform_toeEnd.setParent(self.drivenXform_toe)

        pymel.xform(self.drivenXform_leg, matrix=self.matrixDict['leg'], worldSpace=True)
        pymel.xform(self.drivenXform_knee, matrix=self.matrixDict['knee'], worldSpace=True)
        pymel.xform(self.drivenXform_ankle, matrix=self.matrixDict['ankle'], worldSpace=True)
        pymel.xform(self.drivenXform_ballOfFoot, matrix=self.matrixDict['ballOfFoot'], worldSpace=True)
        pymel.xform(self.drivenXform_toe, matrix=self.matrixDict['toe'], worldSpace=True)
        pymel.xform(self.drivenXform_toeEnd, matrix=self.matrixDict['toeEnd'], worldSpace=True)

        self.drivenXform_leg.drawStyle.set(2)
        self.drivenXform_knee.drawStyle.set(2)

        currentParent = self.drivenXformsGroup
        for i in range(self.lenLegTwist+1):
            drivenXform_legTwist = pymel.createNode('joint')
            drivenXform_legTwist.jointOrient.set([0,0,0], lock=True)
            drivenXform_legTwist.setParent(currentParent)
            self.setName(drivenXform_legTwist, 'drivenXform_legTwist', index=i)

            moveVector = ka_math.multiplyVectors(self.vectorOfKnee, (float(i)/self.lenLegTwist))
            finalPosition = ka_math.addVectors(self.posOfLeg, moveVector)

            pymel.xform(drivenXform_legTwist, translation=finalPosition, worldSpace=True)
            pymel.xform(drivenXform_legTwist, rotation=self.rotationOfLeg, worldSpace=True)

            self.drivenXform_legTwists.append(drivenXform_legTwist)
            currentParent = drivenXform_legTwist

        currentParent = self.drivenXformsGroup
        for i in range(self.lenKneeTwist+1):
            drivenXform_kneeTwist = pymel.createNode('joint')
            drivenXform_kneeTwist.jointOrient.set([0,0,0], lock=True)
            drivenXform_kneeTwist.setParent(currentParent)
            self.setName(drivenXform_kneeTwist, 'drivenXform_kneeTwist', index=i)

            moveVector = ka_math.multiplyVectors(self.vectorOfAnkle, (float(i)/self.lenKneeTwist))
            finalPosition = ka_math.addVectors(self.posOfKnee, moveVector)

            pymel.xform(drivenXform_kneeTwist, translation=finalPosition, worldSpace=True)
            pymel.xform(drivenXform_kneeTwist, rotation=self.rotationOfKnee, worldSpace=True)

            self.drivenXform_kneeTwists.append(drivenXform_kneeTwist)
            currentParent = drivenXform_kneeTwist


        self.drivenXform_legTwists[-1].v.set(0)
        self.drivenXform_kneeTwists[-1].v.set(0)

        # knee IK --------------------------------------------------------------------------------------
        self.kneeIkControlStack = ka_controls.createControlStack('ikKnee', shape='pyramidPointer', size=1, side=self.side, pointAt='y')
        ka_transforms.snap(self.kneeIkControlStack[0], self.defaultXform_knee, t=True)
        self.kneeIkControlStack[0].setParent(self.drivenXform_knee)

        ka_controls.addSpace(self.kneeIkControlStack)

        kneeIk_legGroup = pymel.createNode('transform')
        kneeIk_kneeGroup = pymel.createNode('transform')
        kneeIk_ankleGroup = pymel.createNode('transform')

        self.setName(kneeIk_legGroup, 'kneeIk_legGroup')
        self.setName(kneeIk_kneeGroup, 'kneeIk_kneeGroup')
        self.setName(kneeIk_ankleGroup, 'kneeIk_ankleGroup')

        kneeIk_legGroup.setParent(self.drivenXform_leg)
        kneeIk_kneeGroup.setParent(kneeIk_legGroup)
        kneeIk_ankleGroup.setParent(kneeIk_kneeGroup)

        ka_transforms.snap(kneeIk_legGroup, self.defaultXform_leg, t=1, r=1)
        ka_transforms.snap(kneeIk_kneeGroup, self.defaultXform_knee, t=1, r=1)
        ka_transforms.snap(kneeIk_kneeGroup, self.defaultXform_ankle, t=1, r=1)

        pymel.aimConstraint(self.kneeIkControlStack[-1], kneeIk_legGroup, aimVector=[1*self.sideInt, 0, 0], worldUpObject=self.kneeIkControlStack[-1], worldUpType='objectrotation', upVector=[0,0,1], worldUpVector=[0,0,1])
        pymel.aimConstraint(self.drivenXform_ankle, kneeIk_kneeGroup, aimVector=[1*self.sideInt, 0, 0], worldUpObject=self.kneeIkControlStack[-1], worldUpType='objectrotation', upVector=[0,0,1], worldUpVector=[0,0,1])
        pymel.pointConstraint(self.kneeIkControlStack[-1], kneeIk_kneeGroup)
        pymel.pointConstraint(self.drivenXform_ankle, kneeIk_ankleGroup)


        # create ik curves --------------------------------------------------------------------------------------
        drivenLegIkCurvePoints = []
        for i in range(self.lenLegBendyControls+2):
            moveVector = ka_math.multiplyVectors(self.vectorOfKnee, (float(i)/(self.lenLegBendyControls+1)))
            finalPosition = ka_math.addVectors(self.posOfLeg, moveVector)
            drivenLegIkCurvePoints.append(finalPosition)

        drivenKneeIkCurvePoints = []
        for i in range(self.lenKneeBendyControls+2):
            moveVector = ka_math.multiplyVectors(self.vectorOfAnkle, (float(i)/(self.lenKneeBendyControls+1)))
            finalPosition = ka_math.addVectors(self.posOfKnee, moveVector)
            drivenKneeIkCurvePoints.append(finalPosition)

        # create curve zro that streches with scale
        drivenLegIkCurveZro = pymel.createNode('transform')
        self.setName(drivenLegIkCurveZro, 'drivenLegIkCurve', nodePurpose='zeroOutGroup')
        drivenLegIkCurveZro.setParent(kneeIk_legGroup)
        ka_transforms.snap(drivenLegIkCurveZro, self.defaultXform_leg, t=1, r=1)

        #multiplyDivide = pymel.createNode('multiplyDivide')
        #multiplyDivide.operation.set(2)
        #kneeIk_kneeGroup.tx >> multiplyDivide.input1X
        #self.defaultXform_knee.tx >> multiplyDivide.input2X
        #multiplyDivide.outputX >> drivenLegIkCurveZro.sx

        # create curve
        drivenLegIkCurve = pymel.curve( p=drivenLegIkCurvePoints, worldSpace=True, degree=3)
        drivenLegIkCurveShape = drivenLegIkCurve.getShape()
        self.setName(drivenLegIkCurve, 'drivenLegIkCurve')
        drivenLegIkCurve.setParent(drivenLegIkCurveZro)


        # create curve zro that streches with scale
        drivenKneeIkCurveZro = pymel.createNode('transform')
        self.setName(drivenKneeIkCurveZro, 'drivenKneeIkCurve', nodePurpose='zeroOutGroup')
        drivenKneeIkCurveZro.setParent(kneeIk_kneeGroup)
        ka_transforms.snap(drivenKneeIkCurveZro, self.defaultXform_knee, t=1, r=1)

        #multiplyDivide = pymel.createNode('multiplyDivide')
        #multiplyDivide.operation.set(2)
        #kneeIk_ankleGroup.tx >> multiplyDivide.input1X
        #self.defaultXform_ankle.tx >> multiplyDivide.input2X
        #multiplyDivide.outputX >> drivenKneeIkCurveZro.sx

        # create curve
        drivenKneeIkCurve = pymel.curve( p=drivenKneeIkCurvePoints, worldSpace=True, degree=3)
        drivenKneeIkCurveShape = drivenKneeIkCurve.getShape()
        self.setName(drivenKneeIkCurve, 'drivenKneeIkCurve')
        drivenKneeIkCurve.setParent(drivenKneeIkCurveZro)

        # create ik handles
        drivenLegIkHandle = pymel.ikHandle(startJoint=self.drivenXform_legTwists[0], endEffector=self.drivenXform_legTwists[-1], solver='ikSplineSolver')[0]
        self.setName(drivenLegIkHandle, 'drivenXform_legTwistIkHandle')
        drivenLegIkHandle.setParent(bendyWorldSpaceGroup)
        drivenLegIkHandle.dTwistControlEnable.set(1)
        drivenLegIkHandle.dWorldUpType.set(4)
        drivenLegIkHandle.dWorldUpVector.set(0,0,1)
        drivenLegIkHandle.dWorldUpVectorEnd.set(0,0,1)
        drivenLegIkHandle.dWorldUpAxis.set(3)
        drivenLegIkHandle.priority.set(3)
        self.drivenXform_leg.worldMatrix[0] >> drivenLegIkHandle.dWorldUpMatrix
        kneeIk_kneeGroup.worldMatrix[0] >> drivenLegIkHandle.dWorldUpMatrixEnd


        pymel.delete(drivenLegIkHandle.inCurve.inputs(plugs=True)[0].node().getParent())
        drivenLegIkCurveShape.worldSpace[0] >> drivenLegIkHandle.inCurve


        drivenKneeIkHandle = pymel.ikHandle(startJoint=self.drivenXform_kneeTwists[0], endEffector=self.drivenXform_kneeTwists[-1], solver='ikSplineSolver')[0]
        self.setName(drivenKneeIkHandle, 'drivenXform_kneeTwistIkHandle')
        drivenKneeIkHandle.setParent(bendyWorldSpaceGroup)
        drivenKneeIkHandle.dTwistControlEnable.set(1)
        drivenKneeIkHandle.dWorldUpType.set(4)
        drivenKneeIkHandle.dWorldUpVector.set(0,0,1)
        drivenKneeIkHandle.dWorldUpVectorEnd.set(0,0,1)
        drivenKneeIkHandle.dWorldUpAxis.set(3)
        drivenLegIkHandle.priority.set(4)
        kneeIk_kneeGroup.worldMatrix[0] >> drivenKneeIkHandle.dWorldUpMatrix
        self.drivenXform_ankle.worldMatrix[0] >> drivenKneeIkHandle.dWorldUpMatrixEnd


        pymel.delete(drivenKneeIkHandle.inCurve.inputs(plugs=True)[0].node().getParent())
        drivenKneeIkCurveShape.worldSpace[0] >> drivenKneeIkHandle.inCurve

        self.setName(drivenKneeIkCurve, 'drivenKneeIkCurve')

        # set up ik strech
        drivenLegIkCurveInfo = pymel.createNode('curveInfo')
        drivenKneeIkCurveInfo = pymel.createNode('curveInfo')

        drivenLegIkCurveShape.local >> drivenLegIkCurveInfo.inputCurve
        drivenKneeIkCurveShape.local >> drivenKneeIkCurveInfo.inputCurve

        drivenIkCurveDistanceDivider_leg = pymel.createNode('multiplyDivide')
        drivenIkCurveDistanceDivider_leg.input2X.set(1.0/(self.lenLegBendyControls+2))
        drivenIkCurveDistanceDivider_knee = pymel.createNode('multiplyDivide')
        drivenIkCurveDistanceDivider_knee.input2X.set(1.0/(self.lenKneeBendyControls+2))

        drivenLegIkCurveInfo.arcLength >> drivenIkCurveDistanceDivider_leg.input1X
        drivenKneeIkCurveInfo.arcLength >> drivenIkCurveDistanceDivider_knee.input1X

        for i, bendyJoint in enumerate(self.drivenXform_legTwists):
            if i != 0:
                drivenIkCurveDistanceDivider_leg.outputX >> bendyJoint.tx

        for i, bendyJoint in enumerate(self.drivenXform_kneeTwists):
            if i != 0:
                drivenIkCurveDistanceDivider_knee.outputX >> bendyJoint.tx


        # create the driven leg cv xforms ---------------------------------------------------------------------------
        clusterTransformsGroup_leg = pymel.createNode('transform')
        self.setName(clusterTransformsGroup_leg, 'clusterTransformsGroup_leg')
        clusterTransformsGroup_leg.setParent(bendyWorldSpaceGroup)
        ka_transforms.snap(clusterTransformsGroup_leg, self.defaultXform_leg, t=1, r=1)

        self.bendyLegControlStacks = []
        self.bendyLegClusterStacks = []
        clusterZeroGroups_leg = []
        last = len(drivenLegIkCurveShape.cv)-1
        for i, cv in enumerate(drivenLegIkCurveShape.cv):
            if i != 0:
                # make bendy cluster ------------------------
                clusterZeroGroup = pymel.createNode('transform', )
                self.setName(clusterZeroGroup, 'drivenLegIkCurveCluster', index=i, nodePurpose='zeroOutGroup')
                clusterZeroGroup.setParent(clusterTransformsGroup_leg)

                clusterOffsetGroup = pymel.createNode('transform', )
                self.setName(clusterOffsetGroup, 'drivenLegIkCurveCluster', index=i, nodePurpose='offsetGroup')
                clusterOffsetGroup.setParent(clusterZeroGroup)

                cluster, clusterTransform = pymel.cluster(cv)
                self.setName(cluster, 'drivenLegIkCurveCluster', index=i)
                self.setName(clusterTransform, 'drivenLegIkCurveTransform', index=i)
                clusterTransform.v.set(0)

                cvPos = cv.getPosition(space='world')
                pymel.xform(clusterZeroGroup, translation=cvPos, worldSpace=True)
                ka_transforms.snap(clusterZeroGroup, self.defaultXform_leg, r=1)

                clusterTransform.setParent(clusterOffsetGroup)

                self.bendyLegClusterStacks.append([clusterZeroGroup, clusterOffsetGroup, clusterTransform])

            if i != 0 and i != last:
                # make bendy control ------------------------
                weightedAverage = (1.0/(len(drivenLegIkCurveShape.cv))) * i
                sizeA = (self.sizeDict['leg']*1.5) * (1.0-weightedAverage)
                sizeB = (self.sizeDict['knee']*1.5) * weightedAverage
                size = sizeA+sizeB

                bendyControlerStack = ka_controls.createControlStack('legBendy', shape='circle', index=i-1, size=size, side=self.side)
                bendyControlerStack[0].setParent(kneeIk_legGroup)
                pymel.xform(bendyControlerStack[0], translation=cv.getPosition(space='world'), worldSpace=True)
                ka_transforms.snap(bendyControlerStack[0], self.drivenXform_leg, r=1,)
                for attr in ('rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'):
                    bendyControlerStack[-1].attr(attr).set(lock=True, keyable=False)

                self.bendyLegControlStacks.append(bendyControlerStack)

                # connect controler to cluster
                bendyControlerStack[-1].tx >> clusterOffsetGroup.tx
                bendyControlerStack[-1].ty >> clusterOffsetGroup.ty
                bendyControlerStack[-1].tz >> clusterOffsetGroup.tz

            # move controlers and clusters with strech ------------------------
            if i != 0:
                if i != last:
                    tx = bendyControlerStack[0].tx.get()
                else:
                    tx = clusterZeroGroup.tx.get()

                kneeTx = kneeIk_kneeGroup.tx.get()
                ratio = tx / kneeTx
                multiplyDivide = pymel.createNode('multiplyDivide')
                multiplyDivide.input2X.set(ratio)
                kneeIk_kneeGroup.tx >> multiplyDivide.input1X

                if i == 0:
                    multiplyDivide.outputX >> bendyControlerStack[0].tx

                elif i == last:
                    multiplyDivide.outputX >> clusterZeroGroup.tx

                else:
                    multiplyDivide.outputX >> bendyControlerStack[0].tx
                    multiplyDivide.outputX >> clusterZeroGroup.tx


        # create the driven knee cv xforms ---------------------------------------------------------------------------
        clusterTransformsGroup_knee = pymel.createNode('transform')
        self.setName(clusterTransformsGroup_knee, 'clusterTransformsGroup_knee')
        clusterTransformsGroup_knee.setParent(clusterTransformsGroup_leg)
        ka_transforms.snap(clusterTransformsGroup_knee, self.defaultXform_knee, t=1, r=1)

        self.bendyKneeControlStacks = []
        self.bendyKneeClusterStacks = []
        clusterZeroGroups_knee = []
        last = len(drivenKneeIkCurveShape.cv)-1
        for i, cv in enumerate(drivenKneeIkCurveShape.cv):
            if i != 0:
                # make bendy cluster ------------------------
                clusterZeroGroup = pymel.createNode('transform', )
                self.setName(clusterZeroGroup, 'drivenKneeIkCurveCluster', index=i, nodePurpose='zeroOutGroup')
                clusterZeroGroup.setParent(clusterTransformsGroup_knee)

                clusterOffsetGroup = pymel.createNode('transform', )
                self.setName(clusterOffsetGroup, 'drivenKneeIkCurveCluster_ofs', index=i, nodePurpose='offsetGroup')
                clusterOffsetGroup.setParent(clusterZeroGroup)

                cluster, clusterTransform = pymel.cluster(cv)
                self.setName(cluster, 'drivenKneeIkCurveCluster', index=i)
                self.setName(clusterTransform, 'drivenKneeIkCurveTransform', index=i)
                clusterTransform.v.set(0)

                cvPos = cv.getPosition(space='world')
                pymel.xform(clusterZeroGroup, translation=cvPos, worldSpace=True)
                ka_transforms.snap(clusterZeroGroup, self.defaultXform_knee, r=1)

                clusterTransform.setParent(clusterOffsetGroup)

                self.bendyKneeClusterStacks.append([clusterZeroGroup, clusterOffsetGroup, clusterTransform])


            if i != last:
                # make bendy control ------------------------
                weightedAverage = (1.0/(len(drivenLegIkCurveShape.cv))) * i
                sizeA = (self.sizeDict['knee']*1.5) * (1.0-weightedAverage)
                sizeB = (self.sizeDict['ankle']*1.5) * weightedAverage
                size = sizeA+sizeB

                bendyControlerStack = ka_controls.createControlStack('kneeBendy', shape='circle', index=i, size=size, side=self.side)
                bendyControlerStack[0].setParent(kneeIk_kneeGroup)
                pymel.xform(bendyControlerStack[0], translation=cv.getPosition(space='world'), worldSpace=True)
                ka_transforms.snap(bendyControlerStack[0], self.drivenXform_knee, r=1,)
                for attr in ('rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'):
                    bendyControlerStack[-1].attr(attr).set(lock=True, keyable=False)

                self.bendyKneeControlStacks.append(bendyControlerStack)


            if i != 0 and i != last:
                # connect controler to cluster ------------------------
                bendyControlerStack[-1].tx >> clusterOffsetGroup.tx
                bendyControlerStack[-1].ty >> clusterOffsetGroup.ty
                bendyControlerStack[-1].tz >> clusterOffsetGroup.tz


            # move controlers and clusters with strech ------------------------
            if i != last:
                tx = bendyControlerStack[0].tx.get()
            else:
                tx = clusterZeroGroup.tx.get()

            ankleTx = kneeIk_ankleGroup.tx.get()
            ratio = tx / ankleTx
            multiplyDivide = pymel.createNode('multiplyDivide')
            multiplyDivide.input2X.set(ratio)
            kneeIk_ankleGroup.tx >> multiplyDivide.input1X

            if i == 0:
                multiplyDivide.outputX >> bendyControlerStack[0].tx

            elif i == last:
                multiplyDivide.outputX >> clusterZeroGroup.tx

            else:
                multiplyDivide.outputX >> bendyControlerStack[0].tx
                multiplyDivide.outputX >> clusterZeroGroup.tx



        # connect bendy controls to length of limbs
        #for controlStack in self.bendyLegControlStacks:
            #tx = controlStack[0].tx.get()
            #kneeTx = kneeIk_kneeGroup.tx.get()
            #ratio = tx / kneeTx
            #multiplyDivide = pymel.createNode('multiplyDivide')
            #multiplyDivide.input2X.set(ratio)
            #kneeIk_kneeGroup.tx >> multiplyDivide.input1X
            #multiplyDivide.outputX >> controlStack[0].tx

        #for controlStack in self.bendyKneeControlStacks:
            #tx = controlStack[0].tx.get()
            #ankleTx = kneeIk_ankleGroup.tx.get()
            #ratio = tx / ankleTx
            #multiplyDivide = pymel.createNode('multiplyDivide')
            #multiplyDivide.input2X.set(ratio)
            #kneeIk_ankleGroup.tx >> multiplyDivide.input1X
            #multiplyDivide.outputX >> controlStack[0].tx

        # connect driven skeleton to output skeleton
        last = len(self.drivenXform_legTwists)-1
        for i, joint in enumerate(self.drivenXform_legTwists):
            if i != last:
                self.drivenXform_legTwists[i].tx >> self.outputXforms[i].tx
                self.drivenXform_legTwists[i].rx >> self.outputXforms[i].rx
                self.drivenXform_legTwists[i].ry >> self.outputXforms[i].ry
                self.drivenXform_legTwists[i].rz >> self.outputXforms[i].rz

                if i == 0:
                    pymel.parentConstraint(self.drivenXform_kneeTwists[i], self.outputXforms[i+last], maintainOffset=False)

                else:
                    self.drivenXform_kneeTwists[i].tx >> self.outputXforms[i+last].tx
                    self.drivenXform_kneeTwists[i].rx >> self.outputXforms[i+last].rx
                    self.drivenXform_kneeTwists[i].ry >> self.outputXforms[i+last].ry
                    self.drivenXform_kneeTwists[i].rz >> self.outputXforms[i+last].rz

        pymel.parentConstraint(self.drivenXform_ankle, self.outputXform_ankle, maintainOffset=False)

        self.drivenXform_ballOfFoot.tx >> self.outputXform_ballOfFoot.tx
        self.drivenXform_ballOfFoot.rx >> self.outputXform_ballOfFoot.rx
        self.drivenXform_ballOfFoot.ry >> self.outputXform_ballOfFoot.ry
        self.drivenXform_ballOfFoot.rz >> self.outputXform_ballOfFoot.rz

        self.drivenXform_toe.tx >> self.outputXform_toe.tx
        self.drivenXform_toe.rx >> self.outputXform_toe.rx
        self.drivenXform_toe.ry >> self.outputXform_toe.ry
        self.drivenXform_toe.rz >> self.outputXform_toe.rz

        self.drivenXform_toeEnd.tx >> self.outputXform_toeEnd.tx
        self.drivenXform_toeEnd.rx >> self.outputXform_toeEnd.rx
        self.drivenXform_toeEnd.ry >> self.outputXform_toeEnd.ry
        self.drivenXform_toeEnd.rz >> self.outputXform_toeEnd.rz




        # switch control --------------------------------------------------------------------------------------
        self.switchControl.setParent(self.drivenXform_knee)
        self.switchControl.t.set(0,0,2.5)
        self.switchControl.r.set(0,0,0)
        for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v',]:
            self.switchControl.attr(attr).set(lock=True, keyable=False)


        # visibility
        drivenLegIkHandle.v.set(0)
        drivenKneeIkHandle.v.set(0)
        self.drivenXform_legTwists[0].v.set(0)
        self.drivenXform_kneeTwists[0].v.set(0)
        self.drivenXform_ankle.v.set(0)

        # switch attrs
        self.switchControl.addAttr(BENDY_VIS_ATTRIBUTE_NAME, maxValue=1.0, minValue=0.0, defaultValue=0, keyable=True)
        for controlStack in self.bendyLegControlStacks:
            self.switchControl.attr(BENDY_VIS_ATTRIBUTE_NAME) >> controlStack[0].v

        for controlStack in self.bendyKneeControlStacks:
            self.switchControl.attr(BENDY_VIS_ATTRIBUTE_NAME) >> controlStack[0].v

        self.switchControl.addAttr(KNEE_IK_VIS_ATTRIBUTE_NAME, maxValue=1.0, minValue=0.0, defaultValue=0, keyable=True)


