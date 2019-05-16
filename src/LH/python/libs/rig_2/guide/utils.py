from maya import cmds
import maya.OpenMaya as OpenMaya
from rig.utils import misc
reload(misc)
from rig.utils import exportUtils
reload(exportUtils)
from rig.utils import weightMapUtils
reload(weightMapUtils)

from rig.rigComponents import meshRivetCtrl
reload(meshRivetCtrl)

def get_gimbal_shapes(no_export_nodes=None):
    return
def get_guide_shapes(no_export_nodes=None):
    return
def get_control_shapes(no_export_nodes=None):
    return
def get_guide_positions(no_export_nodes=None):
    return

def get_no_exports():
    return

def set_gimbal_shapes(no_export_nodes=None):
    return
def set_guide_shapes(no_export_nodes=None):
    return
def set_control_shapes(no_export_nodes=None):
    return
def set_guide_positions(no_export_nodes=None):

    # Make sure to update all constraints after guides are set
    cmds.refresh()
    update_geo_constraints()
    return
def set_no_exports():
    pass

def export_all(filename):
    pass

def import_all(filename):
    pass


###############################################################################
############################### TRANSFORMS ####################################
###############################################################################
def getMatrixDeformerPivotLocations(matrixDeformer=None, debug=False):
    if matrixDeformer == None:
        matrixDeformer = cmds.ls(sl=True, typ="LHMatrixDeformer")
        if matrixDeformer:
            matrixDeformer = matrixDeformer[0]
    if not matrixDeformer:
        matrixDeformer = getMatrixDeformerFromControl()
    elemLength = cmds.getAttr(matrixDeformer + ".inputs", s=True)
    rotations = []
    translations = []
    scales = []
    for idx in range(elemLength):
        # print cmds.getAttr(matrixDeformer + ".inputs[{0}].matrix".format(idx))
        locator = cmds.listConnections(matrixDeformer + ".inputs[{0}].matrix".format(idx))[0]
        translations.append(cmds.xform(locator, q=True, ws=True, t=True))
        rotations.append(cmds.xform(locator, q=True, ws=True, ro=True))
        scales.append(cmds.xform(locator, q=True, ws=True, s=True))
    if debug:
        print "rotations", rotations
        print "translations", translations
        print "scales", scales

    return rotations, translations, scales



###############################################################################
################################# SHAPES ######################################
###############################################################################

def get_shape_dicts(shape_nodes, no_export_nodes=None):
    shapeDict = {}
    for shape in shape_nodes:
        if shape in no_export_nodes:
            continue
        shapeDict[shape] = exportUtils.nurbsCurveData(name = shape, space=OpenMaya.MSpace.kObject).nurbsCurve
    return shapeDict


###############################################################################
################################# TAGGING #####################################
###############################################################################

def add_no_export_tag(nodes):
    # if set to be tagged NO_EXPORT attr is added,
    # this is then exported along with whatever else and recreated on build
    # if it is removed, it will export
    for node in nodes:
        misc.tag_no_export(node)

def remove_no_export_tag(nodes):
    # if set to be tagged NO_EXPORT attr is added,
    # this is then exported along with whatever else and recreated on build
    # if it is removed, it will export
    for node in nodes:
        misc.remove_tag_no_export(node)

def no_export_add_remove_selector(nodes, add=True):
    if add:
        add_no_export_tag(nodes)
    else:
        remove_no_export_tag(nodes)

def gimbal_tag_no_export(add=True, checkbox_on=False):
    if not checkbox_on:
        return
    # select controls to be tagged and run
    # Will tag gimbal shapes from being saved out
    sorted_nodes = control_from_selected()
    nodes = misc.get_nodes_from_message(sorted_nodes, "gimbal")
    no_export_add_remove_selector(nodes, add)
    return nodes

def guide_tag_no_export(add=True, checkbox_on=False):
    if not checkbox_on:
        return
    # select controls to be tagged and run
    # Will tag guide positions from being saved out
    sorted_nodes = control_from_selected()
    nodes =  misc.get_nodes_from_message(sorted_nodes, "guide")
    no_export_add_remove_selector(nodes, add)
    return nodes

def guide_shape_tag_no_export(add=True, checkbox_on=False):
    if not checkbox_on:
        return
    # select controls to be tagged and run
    # Will tag guide positions from being saved out
    sorted_nodes = control_from_selected()
    nodes =  misc.get_nodes_from_message(sorted_nodes, "guide_shape")
    no_export_add_remove_selector(nodes, add)
    return nodes

def control_tag_no_export(add=True, checkbox_on=False):
    if not checkbox_on:
        return
    # select controls to be tagged and run
    # Will tag control shapes from being saved out
    return_shapes = []
    nodes = control_from_selected()
    for sel in nodes:
        # You need to have controls selected for this to work
        shape = misc.getShape(sel)
        if shape and cmds.objectType(shape) == "nurbsCurve":
            return_shapes.append(shape)
    no_export_add_remove_selector(return_shapes, add)
    return return_shapes

def control_from_selected():
    return [control for control in cmds.ls(sl=True) if cmds.objExists(control + ".CONTROL")]

# def tag_all(guide=True, guide_shape=True, ctrl_shape=True, gimbal_shape=True):
#     return gimbal_tag_no_export(gimbal_shape) + guide_tag_no_export(guide) + control_tag_no_export(ctrl_shape) + guide_shape_tag_no_export(guide_shape)

def tag_all_no_export(ctrl_shape=True, guide=True, guide_shape=True, gimbal_shape=True):
    control_tag_no_export(checkbox_on=ctrl_shape)
    guide_tag_no_export(checkbox_on=guide)
    guide_shape_tag_no_export(checkbox_on=guide_shape)
    gimbal_tag_no_export(checkbox_on=gimbal_shape)

def remove_tag_all_no_export(ctrl_shape=True, guide=True, guide_shape=True, gimbal_shape=True):
    control_tag_no_export(add=False, checkbox_on=ctrl_shape)
    guide_tag_no_export(add=False, checkbox_on=guide)
    guide_shape_tag_no_export(add=False, checkbox_on=guide_shape)
    gimbal_tag_no_export(add=False, checkbox_on=gimbal_shape)