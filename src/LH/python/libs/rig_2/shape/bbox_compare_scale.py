import maya.api.OpenMaya as om

def get_bounding_box(node_name):
    """Get the bounding box of a given node, handling different types of surfaces."""
    # Get the MObject for the given node name
    selection_list = om.MGlobal.getSelectionListByName(node_name)
    mobj = selection_list.getDependNode(0)

    # Determine the node type and get the bounding box
    if mobj.hasFn(om.MFn.kMesh):
        # For a mesh
        mesh_fn = om.MFnMesh(mobj)
        bbox = mesh_fn.boundingBox()
    elif mobj.hasFn(om.MFn.kNurbsCurve):
        # For a NURBS curve
        curve_fn = om.MFnNurbsCurve(mobj)
        bbox = curve_fn.boundingBox()
    elif mobj.hasFn(om.MFn.kNurbsSurface):
        # For a NURBS surface
        surface_fn = om.MFnNurbsSurface(mobj)
        bbox = surface_fn.boundingBox()
    elif mobj.hasFn(om.MFn.kTransform):
        # For a transform node
        transform_fn = om.MFnTransform(mobj)
        bbox = transform_fn.boundingBox()
    else:
        raise ValueError(f"Node {node_name} is not a recognized surface type.")

    # Convert bbox to a tuple of min and max points
    min_point = bbox.min
    max_point = bbox.max
    return min_point, max_point

def scale_object_to_bounding_box(node_name, target_min, target_max):
    """Scale an object to fit a specified bounding box."""
    # Get the object's current bounding box
    min_point, max_point = get_bounding_box(node_name)
    
    # Calculate the current size
    current_size = max_point - min_point
    
    # Calculate the target size
    target_size = target_max - target_min
    
    # Calculate scale factors for each axis
    scale_factors = target_size / current_size
    
    # Apply the scale factors to the object
    selection_list = om.MGlobal.getSelectionListByName(node_name)
    mobj = selection_list.getDependNode(0)
    
    if not mobj.hasFn(om.MFn.kTransform):
        raise ValueError(f"Node {node_name} is not a transform. Scaling can only be applied to transform nodes.")
    
    transform_fn = om.MFnTransform(mobj)
    current_scale = transform_fn.getTransformation().scale
    
    # Apply the new scale
    new_scale = current_scale * scale_factors
    transform_fn.setScale(new_scale)

# Example usage: Scale object to fit a bounding box from (0,0,0) to (10,10,10)
# scale_object_to_bounding_box('pCube1', om.MPoint(0, 0, 0), om.MPoint(10, 10, 10))
