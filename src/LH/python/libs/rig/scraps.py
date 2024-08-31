#######################################################################
########################## CALAMARI #####################################
########################################################################
import sys

import animcurve.utils
import weights.utils
import importlib

linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)


from rig.utils import faceWeights, lhDeformerExport, exportUtils
importlib.reload(faceWeights)
importlib.reload(lhDeformerExport)
importlib.reload(exportUtils)

from rig.deformers import utils
importlib.reload(utils)
#cmds.getAttr("cluster1.weightList[0].weights")
#print cmds.attributeQuery("weights", node="cluster1", multi=True)

#utils.facesFromWeightmap(weightAttribute="cluster1.weightList[0].weights",geo="C_body_HI")
#exportUtils.lhDeformerWeightTransfer(srcMesh="C_body_HINew", srcDeformer = "C_testFace_SLD_SRC", destMesh = "C_body_HI", destDeformer="C_testFace_SLD")
utils.calimari("kryptoDMU_002_2Dogs3:kryptoDMU_001_linked:skinCluster17", "kryptoDMU_002_2Dogs3:kryptoDMU_001_linked:dog01", .0)
#print cmds.skinPercent( 'skinCluster1', transform='joint1', query=True )


#cmds.select(["C_body_HI.f[531]","C_body_HI.f[528]", "C_body_HI.f[505]"])

#######################################################################
########################## WEIGHTING TOOLS #####################################
########################################################################

from maya import cmds
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)
from .utils import weightingUtils
importlib.reload(weightingUtils)
if cmds.draggerContext("measureVectorCtx", exists=True):
    print("TRUE")
    cmds.deleteUI("measureVectorCtx")


#weightingUtils.dragSomething().clickAndMoveCommand()
#weightingUtils.weightAverage()
#print cmds.ls(orderedSelection=True, fl=True)

#print weightingUtils.gradientWeightsBetween2Points()
#print weightingUtils.gradientWeightsBetween2Points()


#wu = weightingUtils.weightValueDragger()
#wu.weightAttr = "LHWeightDeformer.C_testFace_SLD.lSideWeight"
#print wu.weightAttr
#weightingUtils.weightValueDragger().clickAndMoveCommand()
weightingUtils.gradientBetweenPoints()

#######################################################################
########################## CREATING AND PAINTING #####################################
########################################################################

import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)

from maya import cmds
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)
from rig.utils import weightMapUtils
from rig.utils import misc
from rig.deformers import base
from rig_2.component.subcomponent import weightStack
from rig.deformers import matrixDeformer 
from rig.deformers import utils
from rig_2.component.subcomponent import lip_sub
from rig.rigComponents import line 
from rig.rigComponents import lineTest 
from rig.rigComponents import meshRivetCtrl 
importlib.reload(line)
importlib.reload(lineTest)
importlib.reload(meshRivetCtrl)
importlib.reload(misc)
importlib.reload(weightMapUtils)
importlib.reload(lip_sub)
importlib.reload(utils)
importlib.reload(matrixDeformer)
importlib.reload(weightStack)
importlib.reload(base)

#lipTest.test()
lineTest.test()
cmds.refresh()
utils.cacheOutAllSlideDeformers()
cmds.refresh()
weights.utils.removeAllCurveWeightsNodes()
#weightMapUtils.createWeightMapOnSingleObject("lipCurveBase", "wireMembership", addAttr=True, geoType="nurbsCurve")
#weightMapUtils.createWeightMapOnSingleObject("pSphere1", "targetWeights", addAttr=True, geoType="mesh")


#######################################################################
########################## Add Naked COTROLS #####################################
########################################################################

import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)


from .utils import exportUtils

importlib.reload(exportUtils)

from .utils import misc
importlib.reload(misc)
from .utils import elements
importlib.reload(elements)

from .utils import misc
from .rigComponents import base
importlib.reload(base)
from .rigComponents import slidingCtrl
importlib.reload(slidingCtrl)



#print misc.getGeoData()

#slidingCtrl.component(name="Corner", side="R", helperGeo = "manipSurf", uOutConnectionAttr = "C_testFace_SLD.C_BLipLR", vOutConnectionAttr = "C_testFace_SLD.C_BLipUD")
#slidingCtrl.component(name="Corner", side="R", helperGeo = "C_manipSurf_EX", uOutConnectionAttr = "C_testFace_SLD.rSide", vOutConnectionAttr = "C_testFace_SLD.rMouthUD")
#cmds.connectAttr("C_LCorner_CTL.outU", "C_testFace_SLD.lSide")
#cmds.connectAttr("C_LCorner_CTL.outV", "C_testFace_SLD.lMouthUD")
#slidingCtrl.normalizeSlidingCtrls()
#slidingCtrl.mirrorSlidingCtrls()
#slidingCtrl.copyWeightsFromSlideCtrls()
#misc.pushCurveShape()
#misc.updateGeoConstraint()
misc.addNakedLocatorToControl()
cmds.parent("C_body_HI1Shape", "L_corner_CTL", s=True, r=True)
#print cmds.ls(sl=True)[1:]
#for i in cmds.ls(sl=True):
#    cmds.setAttr(i + ".visibilityMode", 0)


#######################################################################
##########################  CREATE CONTROL SHAPES #####################################
########################################################################

import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)

linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"


from rig.utils import misc
importlib.reload(misc)

from rig.utils import exportUtils
importlib.reload(exportUtils)

from rig.deformers import utils
importlib.reload(utils)
#animCurve = cmds.ls(sl=True)[0]
#animCurvedict = utils.getAnimCurve(animCurve)
#print animCurvedict
#upperLip = {'frame_times': [-10.0, -9.848346598639456, -8.41049030612245, -1.0, 10.0], 'frame_values': [0.0, 0.0, 1.0, 0.0, 0.0], 'out_x_tangents': [1.0, 0.9999736547470093, 0.1614564061164856, 1.0, 1.0], 'is_breakdown': [False, False, False, False, False], 'weights_locked': [False, False, False, False, False], 'in_y_tangents': [0.0, 0.0, 0.9978874325752258, -0.0362398624420166, 0.0], 'name': u'upperLipLIPTHICKFalloff_ACV', 'out_tangents_type': [2, 1, 1, 1, 2], 'is_weighted': [False, False, False, False, False], 'tangents_locked': [True, False, False, False, True], 'in_tangents_type': [2, 1, 1, 1, 2], 'in_x_tangents': [1.0, 1.0, 0.0649663507938385, 0.9993430972099304, 1.0], 'out_y_tangents': [0.0, 0.007255702279508114, -0.986879825592041, 0.0, 0.0]}

#animCurvedict = {'frame_times': [-10.0, -5.0, -2.0, -1.0, 10.0], 'frame_values': [0.0, 0.0, 0.5936454849498327, 0.0, 0.0], 'out_x_tangents': [0.2083333283662796, 0.125, 0.0416666679084301, 0.4583333432674408, 1.0], 'is_breakdown': [False, False, False, False, False], 'weights_locked': [False, False, False, False, False], 'in_y_tangents': [0.0, 0.0, 0.7882182598114014, -0.5936455130577087, 0.0], 'name': u'lowerLipLIPTHICKFalloff_ACV', 'out_tangents_type': [2, 2, 1, 2, 2], 'is_weighted': [True, True, True, True, True], 'tangents_locked': [True, True, False, True, True], 'in_tangents_type': [2, 2, 1, 2, 2], 'in_x_tangents': [0.0, 0.2083333283662796, 0.22398191690444946, 0.0416666679084301, 0.4583333432674408], 'out_y_tangents': [0.0, 0.5936455130577087, -0.5936455130577087, 0.0, 0.0]}
#lowerLip ={'frame_times': [-10.0, -5.0, -2.0, -1.0, 10.0], 'frame_values': [0.0, 0.0, 0.5936454849498327, 0.0, 0.0], 'out_x_tangents': [0.2083333283662796, 0.125, 0.0416666679084301, 0.4583333432674408, 1.0], 'is_breakdown': [False, False, False, False, False], 'weights_locked': [False, False, False, False, False], 'in_y_tangents': [0.0, 0.0, 0.7882182598114014, -0.5936455130577087, 0.0], 'name': u'lowerLipLIPTHICKFalloff_ACV', 'out_tangents_type': [2, 2, 1, 2, 2], 'is_weighted': [True, True, True, True, True], 'tangents_locked': [True, True, False, True, True], 'in_tangents_type': [2, 2, 1, 2, 2], 'in_x_tangents': [0.0, 0.2083333283662796, 0.22398191690444946, 0.0416666679084301, 0.4583333432674408], 'out_y_tangents': [0.0, 0.5936455130577087, -0.5936455130577087, 0.0, 0.0]}


#utils.setAnimCurveShape(animCurve,lowerLip)
#print animCurvedict
#geo = misc.getGeoData()
print(misc.getGeoData())
#misc.createGeoFromData(elements.blockIcon)

#######################################################################
##########################  COMPONENT #####################################
########################################################################


import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)

from maya import cmds
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)
from rig.rigComponents import simpleton
from rig.rigComponents import lipTest 
importlib.reload(lipTest)
importlib.reload(simpleton)

cmds.file( new=True, f=True )

cmds.unloadPlugin("collision")

cmds.loadPlugin("/scratch/levih/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/CentOS-6.6_thru_8/mayaDevKit-2018.0/collision.so")


component = simpleton.Component(createJoint=False)
component.create()

#######################################################################
##########################  ANIM CURVE UTILS #####################################
########################################################################


import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)

from maya import cmds

linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

from rig.utils import misc
importlib.reload(misc)
from rig.utils import exportUtils
importlib.reload(exportUtils)
from rig.utils import animCurves
importlib.reload(animCurves)
from rig.rigComponents import elements
importlib.reload(elements)
from rig.deformers import utils
importlib.reload(utils)


#animCurve = cmds.ls(sl=True)[0]
#utils.setAnimCurveShape(animCurve, elements.MOUTH_LR)


# print AnimCurve
animCurve = cmds.ls(sl=True)[0]
animCurvedict = animcurve.utils.getAnimCurve(animCurve)
print(animCurvedict)

# Mirror AnimCurve
#animCurves.mirrorAnimCurve(side="L")

# Copy AnimCurve
#animCurves.copyAnimCurve()

# Copy Flip AnimCurve
#animCurves.copyFlipAnimCurve()




weights.utils.getAnimCurveWeightsDict()

#######################################################################
##########################  Deformer #####################################
########################################################################


import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)

import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)
from rig.deformers import vectorDeformerSimple
from rig.deformers import curveRollSimple 
from rig.deformers import multiWrap 
from rig.deformers import utils 
from rig.rigComponents import meshRivetCtrl 
importlib.reload(meshRivetCtrl)
importlib.reload(utils)
importlib.reload(vectorDeformerSimple)
importlib.reload(curveRollSimple)
importlib.reload(multiWrap)
from rig.utils import lhExport
importlib.reload(lhExport)

'''
cmds.file( new=True, f=True )

cmds.unloadPlugin("collision")

cmds.loadPlugin("/scratch/levih/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/CentOS-6.6_thru_8/mayaDevKit-2018.0/collision.so")
fileName = "/scratch/levih/dev/rotoslang/src/scenes/presentation/ForTransfer/lipRollTest.ma"
'''

'''
rotations, translations, scales = utils.getMatrixDeformerPivotLocations()
print "rotations", rotations
print "translations", translations
print "scales", scales
'''
print(weights.utils.getWeightStackHandWeightsDict())
#utils.getMatDefWeightsDict()
#utils.convertAnimCurveWeightsToHandWeights()
#meshRivetCtrl.mirrorSlidingCtrls(flipAll=True)
#utils.mirrorSelectedLocatorLToR()
#multiWrap.createTestMultiWrap()
#utils.getMatrixDeformerCtrlLocations(debug=True)
#utils.getMatrixDeformerPivotLocations(debug=True)


#dict = lhExport.lh_component_export(type = "meshRivetCtrl",path = "/scratch/levih/dev/rotoslang/src/scenes/deformerFiles/OptimizationTests/rivetComponentsTESTR.cpt")
#print dict.manipDict
#utils.getControlShapes()
#fileName = "/scratch/levih/dev/rotoslang/src/scenes/presentation/ForTransfer/lipIssues.ma"e

#cmds.file( fileName, i=True, f=True )

# CURVEROLLDEFORMER
#curveRoll = curveRollSimple.CurveRollSimple()
#curveRoll.create()

# VECTORDEFORMER
#vectorDeformerSimple.createTestVectorDeformerRaw()
#vectorDeformerSimple.createTestVectorDeformerClass()

#######################################################################
##########################  SKIN WEIGHT DRAGGER #####################################
########################################################################
import importlib
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
windows = 'C:/Users/harri/Documents/maya/2025/scripts/rotoslang/src/LH/python/libs'

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if "win" in os:
    os = windows

if os not in sys.path:
    sys.path.append(os)

import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig_2'
windows = 'C:/Users/harri/Documents/maya/2025/scripts/rotoslang/src/LH/python/libs/rig_2'

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if "win" in os:
    os = windows

if os not in sys.path:
    sys.path.append(os)

from maya import cmds
import sys
# linux = '/scratch/levih/dev/misc_tools'
# #---determine operating system
# os = sys.platform
# if "linux" in os:
#     os = linux
# if "darwin" in os:
#     os = mac
# if os not in sys.path:
#     sys.path.append(os)



from ka_rigTools import ka_weightBlender
importlib.reload(ka_weightBlender)   

from rig_2.tools import dragger
importlib.reload(dragger)

drag = dragger.Value_Dragger(range_start = 100,
                             range_min = 0,
                             range_max = 200,
                             start_func = ka_weightBlender.start,
                             change_func = ka_weightBlender.change,
                             end_func = ka_weightBlender.finish)

drag.clickAndMoveCommand()
cmds.setToolTo("selectSuperContext")
cmds.setToolTo("valueDragger")













#######################################################################
##########################  Camera UTILS #####################################
########################################################################


import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)

import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig_2'
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)


from maya import cmds
import sys
package = '/scratch/levih/dev/rotoslang/src/LH/python/libs/decorators'
#---determine operating system
if linux not in sys.path:
    sys.path.append(package)
    
from rig_2.manipulator import control
importlib.reload(control)

from rig_2.shape import nurbscurve

importlib.reload(nurbscurve)
#print nurbscurve.get_curve_shape_dict()


from rig_2.manipulator import misc
importlib.reload(misc)

from rig_2.manipulator import elements
importlib.reload(elements)

from rig_2.component import camera
importlib.reload(camera)
from rig_2.node import utils as node_utils
importlib.reload(node_utils)

cmds.file( new=True, f=True )

cam = camera.Component()
cam.create()
print(cam.camera.input_names)



#######################################################################
##########################  SCRATCH PANEL #####################################
########################################################################


import importlib
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
windows = 'C:/Users/harri/Documents/maya/2025/scripts/rotoslang/src/LH/python/libs'

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if "win" in os:
    os = windows

if os not in sys.path:
    sys.path.append(os)

import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig_2'
windows = 'C:/Users/harri/Documents/maya/2025/scripts/rotoslang/src/LH/python/libs/rig_2'

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if "win" in os:
    os = windows

if os not in sys.path:
    sys.path.append(os)


import sys
package = 'C:/Users/harri/Documents/maya/2025/scripts/rotoslang/src/LH/python/libs/decorators'
#---determine operating system
if linux not in sys.path:
    sys.path.append(package)
    
from rig.ui import scratch_panel
importlib.reload(scratch_panel)
scratch_panel.Scratch_Panel.openUI()

