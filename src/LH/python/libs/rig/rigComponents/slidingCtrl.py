from maya import cmds
from rigComponents import base
from utils.misc import formatName, create_ctl
from utils import misc


class component(base.component):
    def __init__(self,
                 uSpeedDefault=.05,
                 vSpeedDefault=.05,
                 initUDefault=0.5,
                 initVDefault=0.5,
                 **kw):
        self.uSpeedDefault = uSpeedDefault
        self.vSpeedDefault = vSpeedDefault
        self.initUDefault = initUDefault
        self.initVDefault = initVDefault
        super(component, self).__init__(**kw)

    #     self.helperGeo = "manipSurf"
    # def createHelperGeo(self):
    #     self.helperGeo = "manipSurf"

    def createCtrl(self):
        self.locator = misc.createLocator(name=misc.formatName(self.side,
                                                              self.name,
                                                              "LOC"),
                                         parent=self.cmptMasterParent)
        self.ctrl = misc.create_ctl(side=self.side,
                                    name=self.name,
                                    parent=self.locator,
                                    shape="circle",
                                    orient=[180, 90, 0],
                                    offset=[0, 0, 1],
                                    scale=[1, 1, 1],
                                    num_buffer=2,
                                    lock_attrs=["tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                    gimbal=True,
                                    size=.5)

        self.ctrlOffset = self.ctrl.buffers[0]
        self.ctrlInverseMatrix = self.ctrl.buffers[1]
        self.ctrl = self.ctrl.ctl


    def createAttrs(self):
        inputAttrs = ["uSpeed", "vSpeed", "initU", "initV"]
        outputAttrs = ["currentU", "currentV", "outU", "outV", "baseU", "baseV", "amountU", "amountV"]
        for attr in inputAttrs:
            setattr(self, attr, "{0}.{1}".format(self.ctrl, attr))

            cmds.addAttr(self.ctrl, ln=attr, at="float",
                         dv=getattr(self, "{0}Default".format(attr)), k=True)
        for attr in outputAttrs:
            setattr(self, attr, "{0}.{1}".format(self.ctrl, attr))
            cmds.addAttr(self.ctrl, ln=attr, at="double",
                         dv=0.0, k=True)


    def createNodes(self):
        #---invert the matrix of the control
        self.decomposeMatrix = misc.createAndConnectNode("decomposeMatrix",
                                                         name=misc.formatName(self.side,
                                                                              self.name + "DecomposeCtrl",
                                                                              "DMX"),
                                                         selfOutput="outputTranslate",
                                                         dstInput="{0}.{1}".format(self.ctrlInverseMatrix, "translate"))

        self.inverseMatrix = misc.createAndConnectNode("inverseMatrix",
                                                       name=misc.formatName(self.side,
                                                                            self.name + "InvertCtrl",
                                                                            "IMX"),
                                                       srcOutput="{0}.{1}".format(self.ctrl, "xformMatrix"),
                                                       selfInput="inputMatrix",
                                                       selfOutput="outputMatrix",
                                                       dstInput="{0}.{1}".format(self.decomposeMatrix, "inputMatrix")
                                                       )
        #--Combine UVSpeed and init
        #---Multuply by the speed first
        self.multNode = cmds.createNode("multiplyDivide", name=misc.formatName(self.side,
                                                                               "{0}{1}".format(self.name, "MultCtrl"),
                                                                               "MTD"))
        cmds.setAttr("{0}.operation".format(self.multNode), 1)
        cmds.connectAttr(self.ctrl + ".translateX", self.multNode + ".input1X")
        cmds.connectAttr(self.ctrl + ".translateY", self.multNode + ".input1Y")
        cmds.connectAttr(self.ctrl + ".uSpeed", self.multNode + ".input2X")
        cmds.connectAttr(self.ctrl + ".vSpeed", self.multNode + ".input2Y")
        #---Add the offset in for nuetral pose
        self.pmaNode = cmds.createNode("plusMinusAverage", name=misc.formatName(self.side,
                                                                                "{0}{1}".format(self.name, "AddCtrl"),
                                                                                "PMA"))
        cmds.setAttr("{0}.operation".format(self.multNode), 1)
        cmds.connectAttr(self.multNode + ".outputX", self.pmaNode + ".input2D[0].input2Dx")
        cmds.connectAttr(self.multNode + ".outputY", self.pmaNode + ".input2D[0].input2Dy")
        #---We want to clamp between 0 and 1 because this is the limit of nurbs UVs
        cmds.connectAttr(self.ctrl + ".initU", self.pmaNode + ".input2D[1].input2Dx")
        cmds.connectAttr(self.ctrl + ".initV", self.pmaNode + ".input2D[1].input2Dy")
        #---We want to clamp between 0 and 1 because this is the limit of nurbs UVs
        self.clampNode = cmds.createNode("clamp", name=misc.formatName(self.side,
                                                                       "{0}{1}".format(self.name, "ClampCtrl"),
                                                                       "CLP"))
        cmds.setAttr(self.clampNode + ".maxR", 1)
        cmds.setAttr(self.clampNode + ".maxG", 1)

        cmds.connectAttr(self.pmaNode + ".output2Dx", self.clampNode + ".inputR")
        cmds.connectAttr(self.pmaNode + ".output2Dy", self.clampNode + ".inputG")
        #---Wire the output back into the ctrl,
        cmds.connectAttr(self.clampNode + ".outputR", self.currentU)
        cmds.connectAttr(self.clampNode + ".outputG", self.currentV)

        #---Get info from the nurbs
        self.surfaceInfo = cmds.createNode("pointOnSurfaceInfo",
                                           name=misc.formatName(self.side,
                                                                self.name + "SurfaceInfo",
                                                                "SFI"),
                                           )
        cmds.connectAttr(self.currentU, self.surfaceInfo + ".parameterU")
        cmds.connectAttr(self.currentV, self.surfaceInfo + ".parameterV")
        cmds.connectAttr(self.helperGeo + ".worldSpace[0]", self.surfaceInfo + ".inputSurface")

        #---Create an aim constraint on some dummy objects
        cmds.connectAttr(self.surfaceInfo + ".position", self.locator + ".translate")

        dummyDst = cmds.spaceLocator(name="target", p=(0, 0, 0))[0]
        cmds.move(0, 1, 0, dummyDst)
        self.aim = cmds.aimConstraint(dummyDst,
                                      self.locator,
                                      name = misc.formatName(self.side,
                                                             self.name,
                                                             "AIM"),
                                      aimVector=[1, 0, 0],
                                      upVector=[0, 1, 0],
                                      worldUpType="vector",
                                      )[0]

        # cmds.connectAttr(self.surfaceInfo + ".position", self.aim + ".target[0].targetRotatePivot", force=True)
        cmds.connectAttr(self.surfaceInfo + ".tangentU", self.aim + ".target[0]targetTranslate", force=True)
        cmds.connectAttr(self.surfaceInfo + ".normalizedNormal", self.aim + ".worldUpVector")
        cmds.delete(dummyDst)
        cmds.setAttr(self.ctrlOffset + ".rx", -90)


        #---Get a clean output for the face rig
        cmds.connectAttr(self.surfaceInfo + ".position", self.aim + ".target[0].targetRotatePivot", force=True)
        self.pmaNtrlzNode = cmds.createNode("plusMinusAverage", name=misc.formatName(self.side,
                                                                                     "{0}{1}".format(self.name, "Nuetralize"),
                                                                                     "PMA"))

        # cmds.connectAttr(self.surfaceInfo + ".position", self.aim + ".target[0].targetRotatePivot", force=True)
        # self.pmaFinalOut = cmds.createNode("plusMinusAverage", name=misc.formatName(self.side,
        #                                                                             "{0}{1}".format(self.name, "FinalOut"),
        #                                                                             "PMA"))


        #---We want to clamp between 0 and 1 because this is the limit of nurbs UVs
        cmds.connectAttr(self.baseU, self.pmaNtrlzNode + ".input2D[0].input2Dx")
        cmds.connectAttr(self.baseV, self.pmaNtrlzNode + ".input2D[0].input2Dy")
        cmds.connectAttr(self.currentU, self.pmaNtrlzNode + ".input2D[1].input2Dx")
        cmds.connectAttr(self.currentV, self.pmaNtrlzNode + ".input2D[1].input2Dy")
        cmds.setAttr("{0}.operation".format(self.pmaNtrlzNode), 2)

        self.multNodeReverse = cmds.createNode("multiplyDivide", name=misc.formatName(self.side,
                                                                               "{0}{1}".format(self.name, "ReverseUV"),
                                                                               "MTD"))
        cmds.setAttr("{0}.operation".format(self.multNode), 1)
        cmds.setAttr(self.multNodeReverse + ".input2X", -1)
        cmds.setAttr(self.multNodeReverse + ".input2Y", -1)
        cmds.connectAttr(self.pmaNtrlzNode + ".output2Dx", self.multNodeReverse + ".input1X")
        cmds.connectAttr(self.pmaNtrlzNode + ".output2Dy", self.multNodeReverse + ".input1Y")

        self.multNodeAmount = cmds.createNode("multiplyDivide", name=misc.formatName(self.side,
                                                                               "{0}{1}".format(self.name, "Amount"),
                                                                               "MTD"))

        cmds.connectAttr(self.multNodeReverse + ".outputX", self.multNodeAmount + ".input1X")
        cmds.connectAttr(self.multNodeReverse + ".outputY", self.multNodeAmount + ".input1Y")

        cmds.connectAttr(self.amountU, self.multNodeAmount + ".input2X")
        cmds.connectAttr(self.amountV, self.multNodeAmount + ".input2Y")

        cmds.setAttr("{0}.operation".format(self.multNode), 1)
        cmds.connectAttr(self.multNodeAmount + ".outputX", self.outU)
        cmds.connectAttr(self.multNodeAmount + ".outputY", self.outV)



def normalizeSlidingCtrls(mayaObjects=None):
    if not mayaObjects: mayaObjects = cmds.ls(sl=True)
    #-- Shift currentU and V to initU and V
    #-- zero out translateX and Y
    # copy current to base
    for ctrl in mayaObjects:
        currentU = cmds.getAttr(ctrl + ".currentU")
        currentV = cmds.getAttr(ctrl + ".currentV")
        cmds.setAttr(ctrl + ".initU", currentU)
        cmds.setAttr(ctrl + ".initV", currentV)
        cmds.setAttr(ctrl + ".tx", 0.0)
        cmds.setAttr(ctrl + ".ty", 0.0)
        # you need to get these attribute values again because they have changed
        currentU = cmds.getAttr(ctrl + ".currentU")
        currentV = cmds.getAttr(ctrl + ".currentV")
        cmds.setAttr(ctrl + ".baseU", currentU)
        cmds.setAttr(ctrl + ".baseV", currentV)
