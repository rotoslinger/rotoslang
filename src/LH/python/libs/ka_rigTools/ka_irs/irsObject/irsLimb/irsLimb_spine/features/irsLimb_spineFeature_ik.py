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

import ka_rigTools.ka_math as ka_math
import ka_rigTools.ka_python as ka_python
import ka_rigTools.ka_controls as ka_controls
import ka_rigTools.ka_transforms as ka_transforms
import ka_rigTools.ka_attr as ka_attr

import ka_rigTools.ka_irs.irsObject.irsFeature as irsFeature

STRECHY_IK_ATTRIBUTE_NAME = 'strechyIk'
ATTRIBUTE_RANGE = 10

class IrsLimb_spineFeature_ik(irsFeature.IrsFeature):
    featureSlot = 1
    featureLabel = 'ik'

    def __init__(self, root=None, **kwargs):

        # set defaults
        kwargs['name'] = kwargs['name']+'_ik'

        # init superClass
        self.__init__IrsFeature__(root, **kwargs)

        self.irsLimb = kwargs['irsLimb']
        self.controls = []

        self.ikControlStack = None
        self.upVectorControlStack = None

        self.ikLegJoint = None
        self.ikKneeJoint = None
        self.ikAnkleJoint = None

        self.rollPivot_innerBank = None
        self.rollPivot_outerBank = None
        self.rollPivot_heel = None
        self.rollPivot_ballOfFoot = None
        self.rollPivot_toes = None
        self.rollPivot_toeEnd = None
        self.rollPivot_ankle = None

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


        # Create IkControl
        size = [limb.sizeDict['ankle'], limb.sizeDict['ankle'], limb.sizeDict['ankle']]
        self.ikControlStack = ka_controls.createControlStack(self.baseName, shape='cube', size=size, side=self.side, pointAt='y')
        ka_transforms.snap(self.ikControlStack[0], limb.defaultXform_ankle, t=True)

        for attr in lockAttrs: self.ikControlStack[-1].attr(attr).set(lock=True, keyable=False)

        ka_attr.addHeaderAttr(self.ikControlStack[-1], 'FOOT_ROLL')

        self.ikControlStack[-1].addAttr('footRoll', niceName='Foot/Heel Roll', softMinValue=-10.0, softMaxValue=20.0, defaultValue=0.0, keyable=True)
        self.ikControlStack[-1].addAttr('footBank', softMinValue=-10.0, softMaxValue=10.0, defaultValue=0.0, keyable=True)

        ka_attr.addSeparatorAttr(node=self.ikControlStack[-1])

        self.ikControlStack[-1].addAttr('toeEndSwivel', softMinValue=-10.0, softMaxValue=10.0, defaultValue=0.0, keyable=True)
        self.ikControlStack[-1].addAttr('footSwivel', softMinValue=-10.0, softMaxValue=10.0, defaultValue=0.0, keyable=True)
        self.ikControlStack[-1].addAttr('heelSwivel', softMinValue=-10.0, softMaxValue=10.0, defaultValue=0.0, keyable=True)

        ka_attr.addHeaderAttr(self.ikControlStack[-1], 'FOOT_ROLL_SETTINGS')

        self.ikControlStack[-1].addAttr('footRollAMaxAngle', niceName='Foot Roll A Max Angle', softMinValue=0.0, softMaxValue=90.0, defaultValue=35.0, keyable=True)
        self.ikControlStack[-1].addAttr('footRollBMaxAngle', niceName='Foot Roll B Max Angle',  softMinValue=0.0, softMaxValue=90.0, defaultValue=35.0, keyable=True)

        ka_attr.addSeparatorAttr(node=self.ikControlStack[-1])

        self.ikControlStack[-1].addAttr('addFootRollA', niceName='+/- Foot Roll Pivot A', keyable=True)
        self.ikControlStack[-1].addAttr('addFootRollB', niceName='+/- Foot Roll Pivot B', keyable=True)
        self.ikControlStack[-1].addAttr('addFootRollC', niceName='+/- Foot Roll Pivot C', keyable=True)
        self.ikControlStack[-1].addAttr('addFootRollD', niceName='+/- Foot Roll Pivot D', keyable=True)

        # Orient IK Control controler shape ---------------------------------------------------------------------------
        # get toe and ankle pos
        toePosition = pymel.xform(limb.defaultXform_ballOfFoot, query=True, translation=True, worldSpace=True)
        anklePosition = pymel.xform(limb.defaultXform_ankle, query=True, translation=True, worldSpace=True)

        # project them to the ground plane
        toeGroundPosition = list(toePosition)
        ankleGroundPosition = list(anklePosition)
        toeGroundPosition[1] = 0
        ankleGroundPosition[1] = 0

        # make into a vector
        flatToeVector = ka_math.subtractVectors(toeGroundPosition, ankleGroundPosition)
        flatToeVector = ka_math.normalizeVector(flatToeVector)

        flatToeVectorCrossProduct = ka_math.crossProduct([0, self.sideInt, 0], flatToeVector)

        footControlMatrix = [flatToeVectorCrossProduct[0], flatToeVectorCrossProduct[1], flatToeVectorCrossProduct[2], 0,
                             0, self.sideInt, 0, 0,
                             flatToeVector[0], flatToeVector[1], flatToeVector[2], 0,
                             anklePosition[0], anklePosition[1], anklePosition[2], 0,]


        pymel.xform(self.ikControlStack[-1], matrix=footControlMatrix, worldSpace=True)
        self.ikControlStack[-1].t.set(0,0,0)
        self.ikControlStack[-1].jointOrient.set(self.ikControlStack[-1].r.get())
        self.ikControlStack[-1].r.set(0,0,0)
        self.ikControlStack[-1].jointOrientX.lock()
        self.ikControlStack[-1].jointOrientY.lock()
        self.ikControlStack[-1].jointOrientZ.lock()


        self.ikControlStack[0].setParent(self.root)

        snapTarget = pymel.createNode('transform')

        # create roll pivots ---------------------------------------------------------------------------
        toePos_inPlaneSpace = ka_transforms.getInForienSpace_point(limb.defaultXform_toe, limb.defaultXform_groundPlane)
        toePos_inPlaneSpace = [toePos_inPlaneSpace[0], 0.0, toePos_inPlaneSpace[2]]
        rollPivot_toe_inPlaneSpace = ka_transforms.getInForienSpace_point(limb.defaultXform_rollPivot_toe, limb.defaultXform_groundPlane)
        toeEndVector_inPlaneSpace = ka_math.subtract(rollPivot_toe_inPlaneSpace, toePos_inPlaneSpace)
        angleBetween_toeRollPivotAndGroundPlane = ka_math.angleBetween(toeEndVector_inPlaneSpace, [1*self.sideInt, 0, 0,])

        toePivotBPos_inWorldSpace = ka_transforms.getInWorldSpace_point(toePos_inPlaneSpace, limb.defaultXform_groundPlane)

        self.rollPivot_innerBank = pymel.createNode('transform')
        self.rollPivot_outerBank = pymel.createNode('transform')
        self.rollPivot_heel = pymel.createNode('transform')
        self.rollPivot_ballOfFoot = pymel.createNode('transform')
        self.rollPivot_ballOfFoot = pymel.createNode('transform')
        self.rollPivot_ballOfFoot_zro = pymel.createNode('transform')
        self.rollPivot_toes = pymel.createNode('transform')
        self.rollPivot_toes_zro = pymel.createNode('transform')
        self.rollPivot_toesB = pymel.createNode('transform')
        self.rollPivot_toesB_zro = pymel.createNode('transform')
        self.rollPivot_toeEnd = pymel.createNode('transform')
        self.rollPivot_ankle = pymel.createNode('transform')

        self.setName(self.rollPivot_innerBank, 'rollPivot_innerBank')
        self.setName(self.rollPivot_outerBank, 'rollPivot_outerBank')
        self.setName(self.rollPivot_heel, 'rollPivot_heel')
        self.setName(self.rollPivot_ballOfFoot, 'rollPivot_ballOfFoot')
        self.setName(self.rollPivot_ballOfFoot_zro, 'rollPivot_ballOfFoot_zro')
        self.setName(self.rollPivot_toes, 'rollPivot_toes')
        self.setName(self.rollPivot_toes_zro, 'rollPivot_toes_zro')
        self.setName(self.rollPivot_toesB, 'rollPivot_toesB')
        self.setName(self.rollPivot_toesB_zro, 'rollPivot_toesB_zro')
        self.setName(self.rollPivot_toeEnd, 'rollPivot_toeEnd')
        self.setName(self.rollPivot_ankle, 'rollPivot_ankle')

        self.rollPivot_innerBank.setParent(self.ikControlStack[-1])
        self.rollPivot_outerBank.setParent(self.rollPivot_innerBank)
        self.rollPivot_heel.setParent(self.rollPivot_outerBank)
        self.rollPivot_toes_zro.setParent(self.rollPivot_heel)
        self.rollPivot_toes.setParent(self.rollPivot_toes_zro)
        self.rollPivot_toeEnd.setParent(self.rollPivot_toes)
        self.rollPivot_toesB_zro.setParent(self.rollPivot_toeEnd)
        self.rollPivot_toesB.setParent(self.rollPivot_toesB_zro)
        self.rollPivot_ballOfFoot_zro.setParent(self.rollPivot_toesB)
        self.rollPivot_ballOfFoot.setParent(self.rollPivot_ballOfFoot_zro)
        self.rollPivot_ankle.setParent(self.rollPivot_ballOfFoot)

        ka_transforms.snap(self.rollPivot_innerBank, limb.defaultXform_rollPivot_innerBank, t=1, r=1)
        ka_transforms.snap(self.rollPivot_outerBank, limb.defaultXform_rollPivot_outerBank, t=1, r=1)
        ka_transforms.snap(self.rollPivot_heel, limb.defaultXform_rollPivot_heel, t=1, r=1)
        ka_transforms.snap(self.rollPivot_toes_zro, limb.defaultXform_toe, t=1, r=1)
        ka_transforms.snap(self.rollPivot_toes, limb.defaultXform_toe, t=1, r=1)
        pymel.xform(self.rollPivot_toes_zro, translation=toePivotBPos_inWorldSpace, worldSpace=True)
        ka_transforms.snap(self.rollPivot_toeEnd, limb.defaultXform_rollPivot_toe, t=1, r=1)
        ka_transforms.snap(self.rollPivot_toesB_zro, limb.defaultXform_toe, t=1, r=1)
        ka_transforms.snap(self.rollPivot_toesB, limb.defaultXform_toe, t=1, r=1)
        ka_transforms.snap(self.rollPivot_ballOfFoot_zro, limb.defaultXform_ballOfFoot, t=1, r=1)
        ka_transforms.snap(self.rollPivot_ballOfFoot, limb.defaultXform_ballOfFoot, t=1, r=1)
        ka_transforms.snap(self.rollPivot_ankle, limb.defaultXform_ankle, t=1, r=1)

        # set driven keys
        # Inner bank
        animCurve_innerBank = pymel.createNode('animCurveUA')
        animCurve_innerBank.rename('innerBank_animCurveUA')
        animCurve_innerBank.preInfinity.set(1)

        pymel.setKeyframe(animCurve_innerBank, insert=True, float=-1 * ATTRIBUTE_RANGE)
        pymel.setKeyframe(animCurve_innerBank, insert=True, float=0)
        pymel.keyframe(animCurve_innerBank, index=0, absolute=True, valueChange=90)
        pymel.keyTangent(animCurve_innerBank, itt='linear', ott='linear')

        self.ikControlStack[-1].footBank >> animCurve_innerBank.input
        animCurve_innerBank.output >> self.rollPivot_innerBank.rz

        # Outer bank
        animCurve_outerBank = pymel.createNode('animCurveUA')
        animCurve_outerBank.rename('outerBank_animCurveUA')
        animCurve_outerBank.postInfinity.set(1)

        pymel.setKeyframe(animCurve_outerBank, insert=True, float=0)
        pymel.setKeyframe(animCurve_outerBank, insert=True, float=ATTRIBUTE_RANGE)
        pymel.keyframe(animCurve_outerBank, index=1, absolute=True, valueChange=-90)
        pymel.keyTangent(animCurve_outerBank, itt='linear', ott='linear')

        self.ikControlStack[-1].footBank >> animCurve_outerBank.input
        animCurve_outerBank.output >> self.rollPivot_outerBank.rz

        # Heel roll
        animCurve_heelRoll = pymel.createNode('animCurveUA')
        animCurve_heelRoll.rename('heelRoll_animCurveUA')
        animCurve_heelRoll.preInfinity.set(1)

        pymel.setKeyframe(animCurve_heelRoll, insert=True, float=-1*ATTRIBUTE_RANGE)
        pymel.setKeyframe(animCurve_heelRoll, insert=True, float=0)
        pymel.keyframe(animCurve_heelRoll, index=0, absolute=True, valueChange=-90)
        pymel.keyTangent(animCurve_heelRoll, itt='linear', ott='linear')

        self.ikControlStack[-1].footRoll >> animCurve_heelRoll.input
        animCurve_heelRoll.output >> self.rollPivot_heel.rx

        # Foot Roll --------
        attrToAngleRange = pymel.createNode('setRange')
        attrToAngleRange.maxX.set(180)
        attrToAngleRange.oldMaxX.set(20)
        self.ikControlStack[-1].footRoll >> attrToAngleRange.valueX

        # ballOfFoot roll
        ballOfFootRollCondition = pymel.createNode('condition')
        ballOfFootRollCondition.operation.set(4)
        attrToAngleRange.outValueX >> ballOfFootRollCondition.firstTerm
        self.ikControlStack[-1].footRollAMaxAngle >> ballOfFootRollCondition.secondTerm
        attrToAngleRange.outValueX >> ballOfFootRollCondition.colorIfTrueR
        self.ikControlStack[-1].footRollAMaxAngle >> ballOfFootRollCondition.colorIfFalseR

        ballOfFootRollAdder = pymel.createNode('plusMinusAverage')
        self.ikControlStack[-1].addFootRollA >> ballOfFootRollAdder.input1D[1]
        ballOfFootRollCondition.outColorR >> ballOfFootRollAdder.input1D[0]
        ballOfFootRollAdder.output1D >> self.rollPivot_ballOfFoot.rz

        # toe roll A
        toeRollDifference = pymel.createNode('plusMinusAverage')
        toeRollDifference.operation.set(2)
        ballOfFootRollCondition.outColorR >> toeRollDifference.input1D[1]
        attrToAngleRange.outValueX >> toeRollDifference.input1D[0]


        toeRollConditionA = pymel.createNode('condition')
        toeRollConditionA.operation.set(2)
        toeRollConditionA.secondTerm.set(0)
        toeRollConditionA.colorIfFalseR.set(0)
        toeRollDifference.output1D >> toeRollConditionA.firstTerm
        toeRollDifference.output1D >> toeRollConditionA.colorIfTrueR

        toeRollConditionB = pymel.createNode('condition')
        toeRollConditionB.operation.set(4)
        toeRollConditionA.outColorR >> toeRollConditionB.firstTerm
        self.ikControlStack[-1].footRollBMaxAngle >> toeRollConditionB.secondTerm
        toeRollConditionA.outColorR>> toeRollConditionB.colorIfTrueR
        self.ikControlStack[-1].footRollBMaxAngle >> toeRollConditionB.colorIfFalseR

        toeRollAdder = pymel.createNode('plusMinusAverage')
        self.ikControlStack[-1].addFootRollB >> toeRollAdder.input1D[1]
        toeRollConditionB.outColorR >> toeRollAdder.input1D[0]
        toeRollAdder.output1D >> self.rollPivot_toesB.rz

        # toe roll B
        toeRollBDifference = pymel.createNode('plusMinusAverage')
        toeRollBDifference.operation.set(2)
        ballOfFootRollCondition.outColorR >> toeRollBDifference.input1D[2]
        toeRollConditionB.outColorR >> toeRollBDifference.input1D[1]
        attrToAngleRange.outValueX >> toeRollBDifference.input1D[0]

        toeRollBConditionA = pymel.createNode('condition')
        toeRollBConditionA.operation.set(2)
        toeRollBConditionA.secondTerm.set(0)
        toeRollBConditionA.colorIfFalseR.set(0)
        toeRollBDifference.output1D >> toeRollBConditionA.firstTerm
        toeRollBDifference.output1D >> toeRollBConditionA.colorIfTrueR

        toeRollBConditionB = pymel.createNode('condition')
        toeRollBConditionB.operation.set(4)
        toeRollBConditionA.outColorR >> toeRollBConditionB.firstTerm
        toeRollBConditionB.secondTerm.set(angleBetween_toeRollPivotAndGroundPlane)
        toeRollBConditionA.outColorR>> toeRollBConditionB.colorIfTrueR
        toeRollBConditionB.colorIfFalseR.set(angleBetween_toeRollPivotAndGroundPlane)

        toeRollBAdder = pymel.createNode('plusMinusAverage')
        self.ikControlStack[-1].addFootRollC >> toeRollBAdder.input1D[1]
        toeRollBConditionB.outColorR >> toeRollBAdder.input1D[0]
        toeRollBAdder.output1D >> self.rollPivot_toes.rz

        # toe roll End
        toeRollEndDifference = pymel.createNode('plusMinusAverage')
        toeRollEndDifference.operation.set(2)
        toeRollBConditionB.outColorR >> toeRollEndDifference.input1D[3]
        ballOfFootRollCondition.outColorR >> toeRollEndDifference.input1D[2]
        toeRollConditionB.outColorR >> toeRollEndDifference.input1D[1]
        attrToAngleRange.outValueX >> toeRollEndDifference.input1D[0]

        toeRollEndCondition = pymel.createNode('condition')
        toeRollEndCondition.operation.set(2)
        toeRollEndCondition.secondTerm.set(0)
        toeRollEndCondition.colorIfFalseR.set(0)
        toeRollEndDifference.output1D >> toeRollEndCondition.firstTerm
        toeRollEndDifference.output1D >> toeRollEndCondition.colorIfTrueR

        toeRollEndAdder = pymel.createNode('plusMinusAverage')
        self.ikControlStack[-1].addFootRollD >> toeRollEndAdder.input1D[1]
        toeRollEndCondition.outColorR >> toeRollEndAdder.input1D[0]
        toeRollEndAdder.output1D >> self.rollPivot_toeEnd.rz


        # create up vector Control ---------------------------------------------------------------------------
        self.upVectorControlStack = ka_controls.createControlStack(self.baseName, shape='cube', side=self.side, pointAt='y')

        # create ik hinge ---------------------------------------------------------------------------
        self.ikLegJoint = pymel.createNode('joint')
        self.setName(self.ikLegJoint, 'ikLegJoint')
        self.ikLegJoint.jointOrient.set([0,0,0], lock=True)
        self.ikLegJoint.setParent(self.root)
        ka_transforms.snap(self.ikLegJoint, limb.defaultXform_leg, t=1, r=1)

        self.ikKneeJoint = pymel.createNode('joint')
        self.setName(self.ikKneeJoint, 'ikKneeJoint')
        self.ikKneeJoint.jointOrient.set([0,0,0], lock=True)
        self.ikKneeJoint.preferredAngle.set([0,0,45*self.sideInt], lock=True)
        self.ikKneeJoint.setParent(self.ikLegJoint)
        ka_transforms.snap(self.ikKneeJoint, limb.defaultXform_knee, t=1, r=1)

        self.ikKneeEndJoint = pymel.createNode('joint')
        self.setName(self.ikKneeEndJoint, 'ikKneeEndJoint')
        self.ikKneeEndJoint.setParent(self.ikKneeJoint)
        self.ikKneeEndJoint.jointOrient.set([0,0,0], lock=True)
        ka_transforms.snap(self.ikKneeEndJoint, limb.defaultXform_ankle, t=1, r=1)


        # create up vector setup
        upVectorMidGroup = pymel.createNode('transform')
        self.setName(upVectorMidGroup, 'upVectorMidGroup')
        upVectorMidGroup.setParent(self.ikControlStack[-1])
        pymel.pointConstraint(self.ikControlStack[-1], self.ikLegJoint, upVectorMidGroup)
        pymel.aimConstraint(self.ikControlStack[-1], upVectorMidGroup, aimVector=[0,-1,0], upVector=[1,0,0], worldUpVector=[1,0,0], worldUpObject=self.ikControlStack[-1], worldUpType='objectrotation')
        startDistanceFromPole = ((self.ikLegJoint.tx.get() + self.ikKneeJoint.tx.get()) / 2.0) * 1.2
        self.upVectorControlStack[0].setParent(upVectorMidGroup)
        self.upVectorControlStack[0].t.set(0, 0, self.sideInt*startDistanceFromPole)
        self.upVectorControlStack[0].r.set(0, 0, 0)

        # create IK Handle ---------------------------------------------------------------------------
        self.ikHandle, ikEffector = pymel.ikHandle(startJoint=self.ikLegJoint, endEffector=self.ikKneeEndJoint, solver='ikRPsolver')
        self.ikHandle.setParent(self.rollPivot_ankle)
        self.ikHandle.t.set(0,0,0)
        self.ikHandle.r.set(0,0,0)
        pymel.poleVectorConstraint(self.upVectorControlStack[-1], self.ikHandle)


        # make ankle ---------------------------------------------------------------------------
        self.ikAnkleJoint = pymel.createNode('joint')
        self.setName(self.ikAnkleJoint, 'ikAnkleJoint')
        self.ikAnkleJoint.jointOrient.set([0,0,0], lock=True)
        self.ikAnkleJoint.setParent(self.ikKneeJoint)
        ka_transforms.snap(self.ikAnkleJoint, limb.defaultXform_ankle, t=1, r=1)


        # make ballOfFoot ---------------------------------------------------------------------------
        size = [limb.defaultXform_toe.tx.get(), 2, 2]
        self.ballOfFoot_controlStack = ka_controls.createControlStack(self.baseName+'_ballOfFoot', size=size, side=limb.side, shape='cubePeg')
        self.ballOfFoot_controlStack[0].setParent(self.rollPivot_toesB)
        ka_transforms.snap(self.ballOfFoot_controlStack[0], limb.defaultXform_ballOfFoot, t=1, r=1)
        for attr in lockAttrs: self.ballOfFoot_controlStack[-1].attr(attr).set(lock=True, keyable=False)
        ka_attr.addSeparatorAttr(node=self.ballOfFoot_controlStack[-1])
        self.ballOfFoot_controlStack[-1].addAttr('length', softMinValue=0.01, softMaxValue=5.0, defaultValue=1.0, keyable=True)

        self.ikBallOfFootJoint = pymel.createNode('joint')
        self.setName(self.ikBallOfFootJoint, 'ikBallOfFootJoint')
        self.ikBallOfFootJoint.jointOrient.set([0,0,0], lock=True)
        self.ikBallOfFootJoint.setParent(self.ikAnkleJoint)
        ka_transforms.snap(self.ikBallOfFootJoint, limb.defaultXform_ballOfFoot, t=1, r=1)

        # make toe ---------------------------------------------------------------------------
        size = [limb.defaultXform_toeEnd.tx.get(), 2, 2]
        self.toe_controlStack = ka_controls.createControlStack(self.baseName+'_toe', size=size, side=limb.side, shape='peg')
        self.toe_controlStack[0].setParent(self.rollPivot_toeEnd)
        ka_transforms.snap(self.toe_controlStack[0], limb.defaultXform_toe, t=1, r=1)
        for attr in lockAttrs: self.toe_controlStack[-1].attr(attr).set(lock=True, keyable=False)
        ka_attr.addSeparatorAttr(node=self.toe_controlStack[-1])
        self.toe_controlStack[-1].addAttr('length', softMinValue=0.01, softMaxValue=5.0, defaultValue=1.0, keyable=True)

        self.ikToeJoint = pymel.createNode('joint')
        self.setName(self.ikToeJoint, 'ikToeJoint')
        self.ikToeJoint.jointOrient.set([0,0,0], lock=True)
        self.ikToeJoint.setParent(self.ikBallOfFootJoint)
        ka_transforms.snap(self.ikToeJoint, limb.defaultXform_toe, t=1, r=1)

        self.ikToeJointEnd = pymel.createNode('joint')
        self.setName(self.ikToeJointEnd, 'ikToeJointEnd')
        self.ikToeJointEnd.jointOrient.set([0,0,0], lock=True)
        self.ikToeJointEnd.setParent(self.ikToeJoint)
        ka_transforms.snap(self.ikToeJointEnd, limb.defaultXform_toeEnd, t=1, r=1)


        # setup stretchy ik ---------------------------------------------------------------------------
        kneeTx = self.ikKneeJoint.tx.get()
        ankleTx = self.ikKneeEndJoint.tx.get()
        initialLength = self.ikKneeJoint.tx.get() + self.ikKneeEndJoint.tx.get()
        diffrenceOfControlAndLeg = ka_math.subtractVectors(pymel.xform(self.ikControlStack[-1], query=True, translation=True, worldSpace=True), pymel.xform(self.ikLegJoint, query=True, translation=True, worldSpace=True))

        distanceNode = pymel.createNode('distanceBetween')
        diffrenceFromLeg = pymel.createNode('plusMinusAverage')

        diffrenceFromLeg.input3D[0].set(diffrenceOfControlAndLeg)

        ratios = pymel.createNode('multiplyDivide')
        ratios.input2X.set(kneeTx / initialLength)
        ratios.input2Y.set(ankleTx / initialLength)

        ankleToWorldSpace_vectorProduct = pymel.createNode('vectorProduct')
        ankleToWorldSpace_vectorProduct.operation.set(4)
        self.rollPivot_ankle.parentMatrix >> ankleToWorldSpace_vectorProduct.matrix
        self.rollPivot_ankle.tx >> ankleToWorldSpace_vectorProduct.input1X
        self.rollPivot_ankle.ty >> ankleToWorldSpace_vectorProduct.input1Y
        self.rollPivot_ankle.tz >> ankleToWorldSpace_vectorProduct.input1Z

        ankleToRootSpace_vectorProduct = pymel.createNode('vectorProduct')
        ankleToRootSpace_vectorProduct.operation.set(4)
        self.root.worldInverseMatrix[0] >> ankleToRootSpace_vectorProduct.matrix
        ankleToWorldSpace_vectorProduct.output >> ankleToRootSpace_vectorProduct.input1

        self.ikLegJoint.t >> distanceNode.point1
        ankleToRootSpace_vectorProduct.output >> distanceNode.point2

        strechCondition = pymel.createNode('condition')
        strechCondition.secondTerm.set(initialLength)
        strechCondition.operation.set(2)
        strechCondition.colorIfFalseR.set(initialLength)
        distanceNode.distance >> strechCondition.firstTerm
        distanceNode.distance >> strechCondition.colorIfTrueR

        strechCondition.outColorR >> ratios.input1X
        strechCondition.outColorR >> ratios.input1Y

        ratios.outputX >> self.ikKneeJoint.tx
        ratios.outputY >> self.ikKneeEndJoint.tx

        # flatten shapes to groundPlane ---------------------------------------------------------------------------
        self.ballOfFoot_controlStack
        self.toe_controlStack

        for control in (self.ballOfFoot_controlStack[-1], self.toe_controlStack[-1]):
            for eachSlice in (slice(5, 6), slice(8, 12), slice(15, 15)):
                for point in control.cv[eachSlice]:
                    worldSpaceOfPoint = pymel.xform(point, query=True, translation=True, worldSpace=True)
                    pointInGroundPlaneSpace = ka_transforms.getInForienSpace_point(worldSpaceOfPoint, limb.defaultXform_groundPlane)
                    pointInGroundPlaneSpace = [pointInGroundPlaneSpace[0], 0, pointInGroundPlaneSpace[2]]
                    worldSpaceOfPoint = ka_transforms.getInWorldSpace_point(pointInGroundPlaneSpace, limb.defaultXform_groundPlane)
                    pymel.xform(point, translation=worldSpaceOfPoint, worldSpace=True)

        #shape = self.ikControlStack[-1].getShape()



        pointIndices = [0,1,2,3,4,7,13,14]
        for index in pointIndices:
            point = self.ikControlStack[-1].cv[index]

            worldSpaceOfPoint = pymel.xform(point, query=True, translation=True, worldSpace=True)
            pointInGroundPlaneSpace = ka_transforms.getInForienSpace_point(worldSpaceOfPoint, limb.defaultXform_groundPlane)
            pointInGroundPlaneSpace = [pointInGroundPlaneSpace[0], 0, pointInGroundPlaneSpace[2]]
            worldSpaceOfPoint = ka_transforms.getInWorldSpace_point(pointInGroundPlaneSpace, limb.defaultXform_groundPlane)
            pymel.xform(point, translation=worldSpaceOfPoint, worldSpace=True)

        ballOfFootPosition_inWorldSpace = pymel.xform(limb.defaultXform_ballOfFoot, query=True, translation=True, worldSpace=True)
        ballOfFootPosition_inPlaneSpace = ka_transforms.getInForienSpace_point(ballOfFootPosition_inWorldSpace, limb.defaultXform_groundPlane)

        pointIndices = [0,3,4,7]
        for index in pointIndices:
            point = self.ikControlStack[-1].cv[index]

            worldSpaceOfPoint = pymel.xform(point, query=True, translation=True, worldSpace=True)
            pointInGroundPlaneSpace = ka_transforms.getInForienSpace_point(worldSpaceOfPoint, limb.defaultXform_groundPlane)
            pointInGroundPlaneSpace = [ballOfFootPosition_inPlaneSpace[0], pointInGroundPlaneSpace[1], pointInGroundPlaneSpace[2]]
            worldSpaceOfPoint = ka_transforms.getInWorldSpace_point(pointInGroundPlaneSpace, limb.defaultXform_groundPlane)
            pymel.xform(point, translation=worldSpaceOfPoint, worldSpace=True)

            #translation[1] = 0.0
            #pymel.xform(shape.cv[index], translation=translation, worldSpace=True)


        # drive joints ---------------------------------------------------------------------------
        pymel.parentConstraint(self.rollPivot_ankle, self.ikAnkleJoint, maintainOffset=False)
        pymel.parentConstraint(self.ballOfFoot_controlStack[-1], self.ikBallOfFootJoint)
        pymel.parentConstraint(self.toe_controlStack[-1], self.ikToeJoint)

        # drive limb ---------------------------------------------------------------------------
        limb.driveJoint(self.ikLegJoint, limb.drivenXform_leg, self.featureLabel)
        limb.driveJoint(self.ikKneeJoint, limb.drivenXform_knee, self.featureLabel)
        limb.driveJoint(self.ikAnkleJoint, limb.drivenXform_ankle, self.featureLabel)
        limb.driveJoint(self.ikBallOfFootJoint, limb.drivenXform_ballOfFoot, self.featureLabel)
        limb.driveJoint(self.ikToeJoint, limb.drivenXform_toe, self.featureLabel)
        limb.driveJoint(self.ikToeJointEnd, limb.drivenXform_toeEnd, self.featureLabel)



        # visibility ---------------------------------------------------------------------------
        self.ikLegJoint.v.set(0)
        self.ikHandle.v.set(0)

        limb.driveVisibility(self.root, self.featureLabel)

        # switchs ---------------------------------------------------------------------------
        limb.switchControl.addAttr(STRECHY_IK_ATTRIBUTE_NAME, maxValue=1.0, minValue=0.0, defaultValue=1.0, keyable=True)

        ka_controls.addSpace(limb.kneeIkControlStack, self.upVectorControlStack[-1], label='ikUpVector')













