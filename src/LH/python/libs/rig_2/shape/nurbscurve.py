
from maya import cmds, mel
import maya.OpenMaya as OpenMaya

from rig_2.mirror import utils as mirror_utils
from rig_2.misc import utils as misc_utils
from rig.utils import misc
import importlib

importlib.reload(misc_utils)

from rig_2.node import utils as node_utils
importlib.reload(node_utils)
from rig.utils import misc

def get_curve_shape_dict(mayaObject=None, space= OpenMaya.MSpace.kWorld):
    if not mayaObject: mayaObject = cmds.ls(sl=True)[0]
    shapes = []
    if not misc_utils.get_shape(mayaObject):
        return
    for shape in misc_utils.get_shape(mayaObject):
        if not shape or not cmds.objExists(shape):
            continue
        degree= cmds.getAttr( '{0}.degree'.format(shape) )
        spans= cmds.getAttr( '{0}.spans'.format(shape) )
        if degree + spans < 1:
            continue

        
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
        
        if not points:
            continue
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

def safe_create_curve(curve_dict,
                        name=None,
                        parent=None,
                        transform_suffix="CTL",
                        shape_suffix="SHP",
                        outliner_color=True,
                        color=True,
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
    if not cmds.objExists(transform_name):
        return create_curve(curve_dict=curve_dict,
                            name=name,
                            parent=parent,
                            transform_suffix=transform_suffix,
                            shape_suffix=shape_suffix,
                            outliner_color=outliner_color,
                            color=color,
                            check_existing=check_existing,
                            mirror=mirror,
                            shape_name=shape_name,
                            )
    shapes = cmds.listRelatives(transform_name, s=True)
    return transform_name, shapes





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
        
        if shape_suffix and not shape_name:
            curve_name = "{0}{1}_{2}".format(name, shape["name"], shape_suffix)

        if shape_name:
            curve_name = shape_name

        if shape_suffix and shape_name:
            curve_name = "{0}_{1}".format(shape_name, shape_suffix)

        if check_existing:
            curve_name = shape["name"]
            
        old_shape=None

        # make sure that somehow None wasn't part of the name....
        if "_None" in curve_name:
            curve_name = curve_name.replace("_None", "_SHP")

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
            cmds.connectAttr(newShape_path.fullPathName() + ".worldSpace", curve_name + ".create", force=True)
            cmds.refresh()

        # Color overrides 

        if color and "override_enabled" in list(shape.keys()) and cmds.objExists(curve_name):
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
    if outliner_color and "outliner_color" in list(curve_dict.keys()) and curve_dict["outliner_color"]:
        cmds.setAttr(curve_transform + ".useOutlinerColor" , True)
        cmds.setAttr(curve_transform + ".outlinerColor" , *curve_dict["outliner_color"][0])
        # mel.eval('AEdagNodeCommonRefreshOutliners();')

    # If one of the shapes under the transform is not in the dictionary, delete it, you may be updating a curve
    if check_existing:
        names = []
        for shape_dict in curve_dict["shapes"]:
            names.append(shape_dict["name"])
        if not curve_transform:
            return curve_transform, retShapes
        allShapes = cmds.listRelatives(curve_transform, s=True, fullPath=True)

        if not allShapes:
            return curve_transform, retShapes

        for shape in cmds.listRelatives(curve_transform, s=True, fullPath=True):
            if not shape:
                continue
            if shape not in names:
                cmds.delete(shape)
        # for shape in curve_dict["shapes"]:

    return curve_transform, retShapes


























def create_curve_new(curve_dict,
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
        
        if shape_suffix and not shape_name:
            curve_name = "{0}{1}_{2}".format(name, shape["name"], shape_suffix)

        if shape_name:
            curve_name = shape_name

        if shape_suffix and shape_name:
            curve_name = "{0}_{1}".format(shape_name, shape_suffix)

        if check_existing:
            curve_name = shape["name"]
            
        old_shape=None

        # make sure that somehow None wasn't part of the name....
        if "_None" in curve_name:
            curve_name = curve_name.replace("_None", "_SHP")

        existing_path = None
        if cmds.objExists(curve_name):
            existing_path = True
        if cmds.objExists(shape["name"]):
            cmds.delete(shape["name"])
        # print "FORM", shape["form"]
        # print "controlVertices", shape["controlVertices"]
        # print "knots", shape["knots"]
        # print "degree", shape["degree"]
        
        
        # cmds.curve( per=True,
        #         p=[(0, 0, 0), (3, 5, 6), (5, 6, 7), (9, 9, 9), (0, 0, 0), (3, 5, 6), (5, 6, 7)],
        #         k=[-2,-1,0,1,2,3,4,5,6] )
        
        # FORM 1
        # controlVertices [[0.26566388672743396, -4.2957875532137635, -0.1635602537186259], [4.277787111643967, -4.046562304977722, -0.19255549706438177], [4.850947572346329, -4.010958698086859, -0.19669767468520405], [3.3439972996211904, -7.554399561330459, -0.3151193447976379], [0.5313277734548679, -8.591575106427527, -0.3271205074372518], [-2.3876073074024284, -7.91043563023909, -0.2736975685894153], [-4.319619798891462, -4.580616408340668, -0.13042283275204775], [-3.746459338189099, -4.545012801449805, -0.13456501037287003], [0.26566388672743396, -4.2957875532137635, -0.1635602537186259]]
        # knots [0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.0, 6.0]
        # degree 3
        
        point = [tuple(p) for p in shape["controlVertices"]]
        # knots = [int(k) for k in shape["knots"]]
        degree = float(shape["degree"])
        knots = [int(k) for k in range(len(shape["controlVertices"]) + int(degree) -1 )]
        
        # knots = [i for i in range(len(shape["knots"]))]

        # numberOfPoints + degree - 1)
        # print "FORM", shape["form"]
        # print "point", point
        # print "knots", knots
        # print "degree", degree
        
        
        tmpCrv = cmds.curve(p=point,
                            k=knots,
                            degree=degree)

        newShape = cmds.listRelatives(tmpCrv, s=1)[0]
        cmds.parent(newShape, shape["parent"], r=1, s=1)

        cmds.delete(tmpCrv)
        newShape = cmds.rename(newShape, cmds.listRelatives(newShape, p=True)[0] + "Shape" )

        if color and "override_enabled" in list(shape.keys()) and cmds.objExists(curve_name):
            cmds.setAttr(curve_name + ".overrideRGBColors", shape["override_color"])
            cmds.setAttr(curve_name + ".overrideEnabled", shape["override_enabled"])
            cmds.setAttr(curve_name + ".overrideColor", shape["color"])
            cmds.setAttr(curve_name + ".overrideColorR", shape["color_r"])
            cmds.setAttr(curve_name + ".overrideColorG", shape["color_g"])
            cmds.setAttr(curve_name + ".overrideColorB", shape["color_b"])



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
