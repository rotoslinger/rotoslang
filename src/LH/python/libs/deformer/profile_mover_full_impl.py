import maya.api.OpenMaya as om
import maya.api.OpenMayaMPx as ompx
import maya.cmds as cmds
import numpy as np

class CurveNetDeformerNode(ompx.MPxDeformerNode):
    kNodeName = "curveNetDeformer"
    kNodeId = om.MTypeId(0x87007)

    def __init__(self):
        super(CurveNetDeformerNode, self).__init__()

    def deform(self, dataBlock, geoIterator, matrix, multiIndex):
        inputGeom = geoIterator.inputGeometry()
        outputGeom = geoIterator.outputGeometry()

        # Get profile curves
        profileCurves = self.get_profile_curves()

        # Check for curves
        if not profileCurves:
            return

        # Compute curve weights and parameters
        weights, tValues = self.compute_curve_weights_and_parameters(profileCurves, geoIterator)

        # Deform each vertex
        while not geoIterator.isDone():
            pos = geoIterator.position()
            pos_np = np.array([pos.x, pos.y, pos.z])
            deformed_pos_np = self.deform_point(pos_np, profileCurves, weights, tValues)
            geoIterator.setPosition(om.MPoint(deformed_pos_np[0], deformed_pos_np[1], deformed_pos_np[2]))
            geoIterator.next()

    def deform_point(self, p, profile_curves, weights, t_values):
        p_deformed = np.copy(p)

        for curve, w_i, t_i in zip(profile_curves, weights, t_values):
            curve_point = self.profile_curve(curve, t_i)
            p_deformed += w_i * (curve_point - p)

        return p_deformed

    def profile_curve(self, curve, t):
        curve_fn = om.MFnNurbsCurve(curve)
        point = curve_fn.getPointAtParam(t, om.MSpace.kWorld)
        return np.array([point.x, point.y, point.z])

    def get_profile_curves(self):
        """
        Retrieves NURBS curves from the Maya scene. 
        Replace with actual method to get your curves.
        """
        # Example code to get NURBS curves by their names
        curve_names = ["curve1", "curve2", "curve3"]  # Replace with actual curve names
        profile_curves = []
        
        for name in curve_names:
            sel_list = om.MSelectionList()
            sel_list.add(name)
            node = sel_list.getDependNode(0)
            profile_curves.append(node)
        
        return profile_curves

    def compute_curve_weights_and_parameters(self, profile_curves, geoIterator):
        """
        Computes weights and parameter values for the curves.
        """
        weights = []
        t_values = []
        
        for curve in profile_curves:
            # Weight could be based on curve properties or other factors
            weight = 1.0 / len(profile_curves)
            weights.append(weight)
            
            # Compute parameter values. Here we use the middle of the curve for simplicity.
            curve_fn = om.MFnNurbsCurve(curve)
            t = curve_fn.numCVs() / 2.0 / (curve_fn.numCVs() - 1)
            t_values.append(t)
        
        return weights, t_values

def nodeCreator():
    return ompx.asMPxPtr(CurveNetDeformerNode())

def nodeInitializer():
    pass  # Initialize node attributes if needed

def initializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(CurveNetDeformerNode.kNodeName, CurveNetDeformerNode.kNodeId,
                             nodeCreator, nodeInitializer, ompx.MPxNode.kDeformerNode)
    except:
        om.MGlobal.displayError("Failed to register node: " + CurveNetDeformerNode.kNodeName)

def uninitializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(CurveNetDeformerNode.kNodeId)
    except:
        om.MGlobal.displayError("Failed to deregister node: " + CurveNetDeformerNode.kNodeName)
