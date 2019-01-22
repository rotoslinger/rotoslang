from maya import cmds


def addSlideCtrl(*args):
    pass
def nuetralizeSlideCtrl(*args):
    pass
def mirrorSlideCtrl(*args):
    pass

def findWeights(self, *args):
    cmds.textScrollList(self.deformer_list3,
                        e = 1,
                        ra = 1)
    self.slideDeformers = cmds.ls(type = "LHSlideDeformer")
    self.vecDeformers = cmds.ls(type = "LHVectorDeformer")
    self.curveRollDeformers = cmds.ls(type = "LHCurveRollDeformer")
    self.weightDeformers = cmds.ls(type = "LHWeightDeformer")
    self.deformers = self.slideDeformers + self.vecDeformers + self.curveRollDeformers + self.weightDeformers
#         self.deformers.append(cmds.ls(type = "LHVectorDeformer"))

    cmds.textScrollList(self.deformer_list3,
                        e = 1,
                        ra = 1)
    cmds.textScrollList(self.deformer_list3,
                        e = 1,
                        append = self.deformers,
                        sc = self.__selectDeformerAttrRemoveAction)