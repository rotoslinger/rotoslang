import maya.api.OpenMaya as om
import maya.cmds as cmds
import numpy as np

import maya.api.OpenMaya as om
import maya.cmds as cmds


#### algorithm 1 ####
def get_intersections_count(mesh_a, mesh_b):
    """
    Return the number of intersecting faces between two meshes.
    """
    mfn_mesh_a = om.MFnMesh(cmds.ls(mesh_a, long=True)[0])
    mfn_mesh_b = om.MFnMesh(cmds.ls(mesh_b, long=True)[0])
    
    # Get bounding boxes for intersection check
    bbox_a = mfn_mesh_a.boundingBox()
    bbox_b = mfn_mesh_b.boundingBox()
    
    if not bbox_a.intersects(bbox_b):
        return 0

    # Check for intersections
    intersection_count = 0
    faces_a = mfn_mesh_a.getPolygonFaces()
    faces_b = mfn_mesh_b.getPolygonFaces()
    
    for face_a in faces_a:
        for face_b in faces_b:
            if mfn_mesh_a.hasIntersection(mfn_mesh_b, face_a, face_b):
                intersection_count += 1
    
    return intersection_count

def find_mesh_with_most_intersections(mesh_a, *meshes_b):
    max_intersections = -1
    best_mesh = None
    
    for mesh_b in meshes_b:
        intersections = get_intersections_count(mesh_a, mesh_b)
        if intersections > max_intersections:
            max_intersections = intersections
            best_mesh = mesh_b
    
    return best_mesh

# Example usage:
# best_mesh = find_mesh_with_most_intersections('meshA', 'meshB1', 'meshB2', 'meshB3')
# print("Mesh with most intersections:", best_mesh)


##### Algorithm 2 #####

import maya.api.OpenMaya as om
import maya.cmds as cmds
import math

def compute_volume(mesh):
    """
    Compute the volume of the mesh based on its bounding box.
    """
    mfn_mesh = om.MFnMesh(cmds.ls(mesh, long=True)[0])
    bbox = mfn_mesh.boundingBox()
    width = bbox.width()
    height = bbox.height()
    depth = bbox.depth()
    return width * height * depth

def compare_shapes(mesh_a, mesh_b):
    """
    Compare the shapes of two meshes.
    This is a placeholder for more sophisticated shape comparison.
    """
    return 1.0 / (1 + abs(compute_volume(mesh_a) - compute_volume(mesh_b)))

def find_most_similar_mesh(mesh_a, *meshes_b):
    best_mesh = None
    best_similarity = -float('inf')
    
    for mesh_b in meshes_b:
        similarity = compare_shapes(mesh_a, mesh_b)
        if similarity > best_similarity:
            best_similarity = similarity
            best_mesh = mesh_b
    
    return best_mesh

# Example usage:
# most_similar_mesh = find_most_similar_mesh('meshA', 'meshB1', 'meshB2', 'meshB3')
# print("Most similar mesh:", most_similar_mesh)


######## 3rd algorithm ########
def compute_volume_and_centroid(mesh):
    """
    Compute the volume and centroid of the mesh.
    """
    mfn_mesh = om.MFnMesh(cmds.ls(mesh, long=True)[0])
    bbox = mfn_mesh.boundingBox()
    
    # Compute volume as a simple approximation
    volume = bbox.width() * bbox.height() * bbox.depth()
    
    # Compute centroid
    centroid = bbox.center()
    
    return volume, np.array([centroid.x, centroid.y, centroid.z])

def compute_curvature(mesh):
    """
    Compute average curvature of the mesh.
    This is a placeholder function and may need more sophisticated computation.
    """
    mfn_mesh = om.MFnMesh(cmds.ls(mesh, long=True)[0])
    curvature_data = mfn_mesh.getFaceVertexNormals()
    average_curvature = np.mean([np.linalg.norm(norm) for norm in curvature_data])
    return average_curvature

def compute_shape_similarity(mesh_a, mesh_b):
    """
    Compute similarity score based on volume, centroid distance, and curvature.
    """
    volume_a, centroid_a = compute_volume_and_centroid(mesh_a)
    volume_b, centroid_b = compute_volume_and_centroid(mesh_b)
    
    curvature_a = compute_curvature(mesh_a)
    curvature_b = compute_curvature(mesh_b)
    
    # Compare volumes
    volume_similarity = 1 / (1 + abs(volume_a - volume_b))
    
    # Compare centroid distance
    centroid_distance = np.linalg.norm(centroid_a - centroid_b)
    centroid_similarity = 1 / (1 + centroid_distance)
    
    # Compare curvature
    curvature_similarity = 1 / (1 + abs(curvature_a - curvature_b))
    
    # Aggregate similarity score
    total_similarity = (volume_similarity + centroid_similarity + curvature_similarity) / 3
    
    return total_similarity

def find_most_similar_mesh(mesh_a, *meshes_b):
    best_mesh = None
    best_similarity = -float('inf')
    
    for mesh_b in meshes_b:
        similarity = compute_shape_similarity(mesh_a, mesh_b)
        if similarity > best_similarity:
            best_similarity = similarity
            best_mesh = mesh_b
    
    return best_mesh

# Example usage:
# most_similar_mesh = find_most_similar_mesh('meshA', 'meshB1', 'meshB2', 'meshB3')
# print("Most similar mesh:", most_similar_mesh)
