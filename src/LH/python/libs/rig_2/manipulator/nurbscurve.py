from maya import cmds, mel
import maya.OpenMaya as OpenMaya
from rig_2.misc import utils as misc_utils
from rig_2.node import utils as node_utils
reload(node_utils)


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
                 name="C_wire",
                 parent=None,
                 transform_suffix = "CTL",
                 shape_suffix = "SHP",
                 outliner_color = True,
                 color = True):
    if not parent:
        parent = curve_dict["parent"]
    if parent and not cmds.objExists(parent):
        parent = None

    # Prepare transform
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
        curve_name = "{0}{1}_{2}".format(name, shape["name"], shape_suffix)
        if cmds.objExists(curve_name):
            continue
        # Verts
        controlVertices = OpenMaya.MPointArray()
        [controlVertices.append(OpenMaya.MPoint(i[0],i[1],i[2]))for i in shape.get("controlVertices")]

        # Knots
        uKnots = OpenMaya.MDoubleArray()
        [uKnots.append(i) for i in shape.get("knots")]

        # Create
        new_nurbsCurve = OpenMaya.MFnNurbsCurve()
        newShape = new_nurbsCurve.create(controlVertices,
                                         uKnots,
                                         shape.get("degree"),
                                         shape.get("form"),
                                         False,
                                         False,
                                         curve_transformMObject
                                         )
        
        # Name
        nurbsCurve_path = OpenMaya.MDagPath()
        path = nurbsCurve_path.getAPathTo(newShape)
        cmds.rename(path.fullPathName(),curve_name)

        # Color overrides 
        if color and "override_enabled" in shape.keys():
            cmds.setAttr(curve_name + ".overrideRGBColors", shape["override_color"])
            cmds.setAttr(curve_name + ".overrideEnabled", shape["override_enabled"])
            cmds.setAttr(curve_name + ".overrideColor", shape["color"])
            cmds.setAttr(curve_name + ".overrideColorR", shape["color_r"])
            cmds.setAttr(curve_name + ".overrideColorG", shape["color_g"])
            cmds.setAttr(curve_name + ".overrideColorB", shape["color_b"])
        retShapes.append(curve_name)
    
    # Outliner Color
    if outliner_color and "outliner_color" in curve_dict.keys() and curve_dict["outliner_color"]:
        cmds.setAttr(curve_transform + ".useOutlinerColor" , True)
        cmds.setAttr(curve_transform + ".outlinerColor" , *curve_dict["outliner_color"][0])
        mel.eval('AEdagNodeCommonRefreshOutliners();')

    return curve_transform, retShapes

