
from maya import cmds, mel
import maya.OpenMaya as OpenMaya

from rig_2.mirror import utils as mirror_utils
from rig_2.misc import utils as misc_utils
from rig.utils import misc

reload(misc_utils)

from rig_2.node import utils as node_utils
reload(node_utils)
from rig.utils import misc

def get_curve_shape_dict(mayaObject=None, space= OpenMaya.MSpace.kWorld):
    if not mayaObject: mayaObject = cmds.ls(sl=True)[0]
    shapes = []
    for shape in misc_utils.get_shape(mayaObject):
        controlVertices = []
        knots = []
        degree = []
        form = []
        parent = []
        shape_type = []

        # Get OM Shape
        nurbsCurve_node = OpenMaya.MSelectionList()
        nurbsCurve_node.add(shape)
        nurbsCurve_path = OpenMaya.MDagPath()
        nurbsCurve_node.getDagPath(0, nurbsCurve_path)
        fn_nurbsCurve = OpenMaya.MFnNurbsCurve(nurbsCurve_path)

        # ControlVertices
        points = OpenMaya.MPointArray()
        fn_nurbsCurve.getCVs(points, space)
        for idx in range(points.length()):
            controlVertices.append((points[idx].x,
                                    points[idx].y,
                                    points[idx].z))

        # Knots
        knots = OpenMaya.MDoubleArray()
        fn_nurbsCurve.getKnots(knots)
        knots = [i for i in knots]

        # Degree
        degree = fn_nurbsCurve.degree()

        # Form
        form = fn_nurbsCurve.form()

        # Curve Color
        override_enabled = cmds.getAttr(shape + ".overrideEnabled")
        color = cmds.getAttr(shape + ".overrideColor")
        override_color = cmds.getAttr(shape + ".overrideRGBColors")
        color_r = cmds.getAttr(shape + ".overrideColorR")
        color_g = cmds.getAttr(shape + ".overrideColorG")
        color_b = cmds.getAttr(shape + ".overrideColorB")

        # Final shape dict
        shapes.append({  "name"              : shape,
                         "controlVertices"   : controlVertices,
                         "knots"             : knots,
                         "degree"            : degree,
                         "form"              : form,
                         "parent"            : mayaObject,
                         "type"              : "nurbsCurve",
                         "override_enabled"  : override_enabled,
                         "color"             : color,
                         "override_color"    : override_color,
                         "color_r"           : color_r,
                         "color_g"           : color_g,
                         "color_b"           : color_b,
                        })

    # Outliner Color
    outliner_color = None
    if cmds.getAttr(mayaObject + ".useOutlinerColor"):
        outliner_color = cmds.getAttr(mayaObject + ".outlinerColor")
    # Return Curve                   
    tmp = cmds.listRelatives(mayaObject, parent = True)
    parent=None
    if tmp:
        parent = tmp[0]
    nurbs_curve = {
                   "name"  : mayaObject,
                   "shapes": shapes,
                   "parent": parent,
                   "outliner_color": outliner_color,
                   }
    return nurbs_curve

def create_curve(curve_dict,
                 name=None,
                 parent=None,
                 transform_suffix = "CTL",
                 shape_suffix = "SHP",
                 outliner_color = True,
                 color = True,
                 check_existing=False,
                 mirror=False,
                shape_name=None,
):
    if not name:
        name = curve_dict["name"]
    if not parent:
        parent = curve_dict["parent"]
    if parent and not cmds.objExists(parent):
        parent = None

    # Prepare transform
    transform_name = name
    if parent and cmds.objExists(parent) and shape_name and not shape_suffix:
        transform_name = parent
    if transform_suffix:
        transform_name = "{0}_{1}".format(name, transform_suffix)
    # curve_transform = cmds.createNode("transform", name = transform_name, p=parent)
    curve_transform = node_utils.get_node_agnostic(nodeType = "transform", name = transform_name, parent=parent)
    curve_transformNode = OpenMaya.MSelectionList()
    curve_transformNode.add(curve_transform)
    curve_transformPath = OpenMaya.MDagPath()
    curve_transformNode.getDagPath(0,curve_transformPath)
    curve_transformMObject = curve_transformPath.transform()
    retShapes = []
    for shape in curve_dict["shapes"]:
        # check if it already exists
        curve_name = shape["name"]
        if shape_suffix or shape_name:
            curve_name = "{0}{1}_{2}".format(name, shape["name"], shape_suffix)
            
        if check_existing:
            curve_name = shape["name"]
        old_shape=None
        existing_path = None
        if cmds.objExists(curve_name):
            existing_path = True
            # old_shape = cmds.rename(curve_name, "{0}_{1}".format(curve_name, random.randint(1,1000000000)))

        # Verts
        controlVertices = OpenMaya.MPointArray()
        [controlVertices.append(OpenMaya.MPoint(i[0],i[1],i[2]))for i in shape.get("controlVertices")]

        # Knots
        uKnots = OpenMaya.MDoubleArray()
        [uKnots.append(i) for i in shape.get("knots")]

        # Create
        new_nurbsCurve = OpenMaya.MFnNurbsCurve()
        # if existing_path:
        #     original_nurbsCurve = misc.getOMNurbsCurve(curve_name)
        newShape = new_nurbsCurve.create(controlVertices,
                                         uKnots,
                                         shape.get("degree"),
                                         shape.get("form"),
                                         False,
                                         False,
                                         curve_transformMObject
                                         )
        # original_nurbsCurve.copy(newShape, curve_transformMObject)
        # Name
        nurbsCurve_path = OpenMaya.MDagPath()
        newShape_path = nurbsCurve_path.getAPathTo(newShape)
        cmds.rename(newShape_path.fullPathName(),curve_name)

        if existing_path:
            cmds.connectAttr(newShape_path.fullPathName() + ".worldSpace", curve_name + ".create")
            cmds.refresh()

        # Color overrides 

        if color and "override_enabled" in shape.keys():
            cmds.setAttr(curve_name + ".overrideRGBColors", shape["override_color"])
            cmds.setAttr(curve_name + ".overrideEnabled", shape["override_enabled"])
            cmds.setAttr(curve_name + ".overrideColor", shape["color"])
            cmds.setAttr(curve_name + ".overrideColorR", shape["color_r"])
            cmds.setAttr(curve_name + ".overrideColorG", shape["color_g"])
            cmds.setAttr(curve_name + ".overrideColorB", shape["color_b"])

        # if old_shape:
        #     cmds.delete(old_shape)

        retShapes.append(curve_name)
        # if mirror:
        #     numCV = controlVertices.length()
        #     points = newShape_path.fullPathName() + '.cv[0:{0}]'.format(numCV)
        #     cmds.scale(-1.0, points, r=True, scaleX=True, scaleY=False, scaleZ=False, )



    # Outliner Color
    if outliner_color and "outliner_color" in curve_dict.keys() and curve_dict["outliner_color"]:
        cmds.setAttr(curve_transform + ".useOutlinerColor" , True)
        cmds.setAttr(curve_transform + ".outlinerColor" , *curve_dict["outliner_color"][0])
        mel.eval('AEdagNodeCommonRefreshOutliners();')

    # If one of the shapes under the transform is not in the dictionary, delete it, you may be updating a curve
    if check_existing:
        names = []
        for shape_dict in curve_dict["shapes"]:
            names.append(shape_dict["name"])

        for shape in cmds.listRelatives(curve_transform, s=True):
            if shape not in names:
                cmds.delete(shape)
        # for shape in curve_dict["shapes"]:

    return curve_transform, retShapes

def mirror_shape(source_curve_transform, target_curve_transform):
    pushCurveShape(source_curve_transform, target_curve_transform, mirror=True)

def copy_shape(color=False):
    selected = cmds.ls(sl=True)
    source_curve_transform = selected[0]
    target_curve_transforms = selected[1:]
    for target_curve_transform in target_curve_transforms:
        pushCurveShape(source_curve_transform, target_curve_transform, mirror=False, inheritColor=color)

def pushCurveShape(source_curve_transform=None, target_curve_transform=None, mirror=False, inheritColor=False):
    selection_for_memory = cmds.ls(sl=True)
    source_curve_shapes = cmds.listRelatives(source_curve_transform, type = "nurbsCurve")
    target_curve_shapes = cmds.listRelatives(target_curve_transform, type = "nurbsCurve")
    for idx, shape in enumerate(source_curve_shapes):
        target_name = None
        if len(target_curve_shapes)-1 <= idx:
            target_name = target_curve_shapes[idx]
        # This means a new curve must be created, so create a new name based on the idx
        if not target_name:
            target_name = "{0}{1:02}".format(target_curve_transform, idx)
        if mirror:
            target_name = mirror_utils.get_opposite_side(shape)
        if not target_name:
            continue
        target_curve = cmds.createNode("nurbsCurve", p=target_curve_transform)
        # target_curve = misc.getParent(target_curve)
        # parentNode = OpenMaya.MSelectionList()
        # parentNode.add(target_curve_transform)
        # parentPath = OpenMaya.MDagPath()
        # parentNode.getDagPath(0,parentPath)
        # parentMObject = parentPath.transform()

        # source = OpenMaya.MSelectionList()
        # source.add(shape)
        # sourcePath = OpenMaya.MDagPath()
        # source.getDagPath(0,sourcePath)
        # sourceMFnCurve = sourcePath.node()

        # dummy = OpenMaya.MObject()

        curveColor = target_curve

        if inheritColor:
            curveColor = shape

        color = cmds.getAttr(curveColor + ".overrideColor")
        override = cmds.getAttr(curveColor + ".overrideRGBColors")

        colorR = cmds.getAttr(curveColor + ".overrideColorR")
        colorG = cmds.getAttr(curveColor + ".overrideColorG")
        colorB = cmds.getAttr(curveColor + ".overrideColorB")

        if not cmds.objExists(target_name):
            cmds.rename(target_curve, target_name)
        else:
            cmds.delete(target_curve)
            target_curve = target_name

        if inheritColor:
            cmds.setAttr(target_curve + ".overrideRGBColors", override)
            cmds.setAttr(target_curve + ".overrideEnabled", True)
            cmds.setAttr(target_curve + ".overrideColor", color)
            cmds.setAttr(target_curve + ".overrideColorR", colorR)
            cmds.setAttr(target_curve + ".overrideColorG", colorG)
            cmds.setAttr(target_curve + ".overrideColorB", colorB)



        cmds.connectAttr(shape + ".worldSpace", target_curve + ".create",f=True)
        cmds.refresh()
        cmds.disconnectAttr(shape + ".worldSpace", target_curve + ".create")

        if mirror:
            fn_nurbsCurve = misc.getOMNurbsCurve(target_curve)
            numCV = fn_nurbsCurve.numCVs()
            points = target_curve + '.cv[0:{0}]'.format(numCV)
            cmds.scale(-1.0, points, r=True, scaleX=True, scaleY=False, scaleZ=False, )
    cmds.select(selection_for_memory)