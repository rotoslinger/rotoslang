import maya.api.OpenMaya as om2
from maya import cmds

def get_dag_path(node_name):
    """
    Returns the MDagPath for the given node, ensuring that the object exists.

    Args:
        node_name (str): Name of the node.

    Returns:
        MDagPath: The DAG path of the node.

    Raises:
        RuntimeError: If the object does not exist or is not a valid DAG node.
    """
    if not cmds.objExists(node_name):
        raise RuntimeError(f"Object '{node_name}' does not exist in the scene.")

    selection_list = om2.MSelectionList()
    try:
        selection_list.add(node_name)
        return selection_list.getDagPath(0)
    except RuntimeError as e:
        raise RuntimeError(f"Error in retrieving DAG path for '{node_name}': {e}")

def get_mesh_vertices(mesh_name):
    """
    Gets the world space vertex positions of a mesh using OpenMaya 2.

    Args:
        mesh_name (str): The name of the mesh.

    Returns:
        list: A list of world space vertex positions [(x, y, z), ...].
    """
    dag_path = get_dag_path(mesh_name)
    mesh_fn = om2.MFnMesh(dag_path)

    # Get vertex positions in world space
    points = mesh_fn.getPoints(om2.MSpace.kWorld)
    
    # Convert MPointArray to list of tuples
    return [(point.x, point.y, point.z) for point in points]

def set_mesh_vertices(mesh_name, positions):
    """
    Sets the vertex positions of a mesh using OpenMaya 2 in world space.

    Args:
        mesh_name (str): The name of the target mesh.
        positions (list): A list of world space vertex positions [(x, y, z), ...].
    """
    dag_path = get_dag_path(mesh_name)
    mesh_fn = om2.MFnMesh(dag_path)

    # Create MPointArray from the list of positions
    points = om2.MPointArray([om2.MPoint(pos) for pos in positions])

    # Set vertex positions in world space
    mesh_fn.setPoints(points, om2.MSpace.kWorld)

def match_mesh_verts(source_mesh, target_mesh):
    """
    Matches the vertex positions of the target mesh to the source mesh in world space using OpenMaya 2.

    Args:
        source_mesh (str): The name of the source mesh whose vertex positions will be used.
        target_mesh (str): The name of the target mesh whose vertex positions will be updated.

    Raises:
        ValueError: If the source and target meshes don't have the same number of vertices.
    """
    # Get vertex positions from the source mesh
    source_positions = get_mesh_vertices(source_mesh)
    print("SOURCE POSITIONS ARE WORKING")

    # Get the number of vertices in both meshes
    source_vert_count = len(source_positions)
    target_vert_count = om2.MFnMesh(get_dag_path(target_mesh)).numVertices

    # Check if the vertex count matches
    if source_vert_count != target_vert_count:
        raise ValueError(f"Meshes '{source_mesh}' and '{target_mesh}' have a different number of vertices.")

    # Set the target mesh vertices to match the source mesh vertices
    set_mesh_vertices(target_mesh, source_positions)

    print(f"Successfully matched the vertex positions of '{target_mesh}' to '{source_mesh}'.")

# Example usage:
# Replace 'sourceMesh' and 'targetMesh' with your actual mesh names
#match_mesh_verts('sourceMesh', 'targetMesh')



