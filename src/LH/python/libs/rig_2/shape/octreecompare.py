import maya.api.OpenMaya as om
import maya.cmds as cmds
import numpy as np

# ---- Octree Node Definition ----
class OctreeNode:
    def __init__(self, min_bound, max_bound, depth=0, max_depth=5):
        """
        Initialize an Octree node. Each node either contains points (leaf) or subdivides into 8 children.

        Args:
            min_bound (list or array): The minimum coordinates (x, y, z) of this node's bounding box.
            max_bound (list or array): The maximum coordinates (x, y, z) of this node's bounding box.
            depth (int): Current depth level of this node in the octree.
            max_depth (int): Maximum depth to which the octree will be subdivided.
        """
        self.min_bound = np.array(min_bound)  # Minimum boundary of the node's 3D region
        self.max_bound = np.array(max_bound)  # Maximum boundary of the node's 3D region
        self.center = (self.min_bound + self.max_bound) / 2  # Center of the bounding box
        self.depth = depth  # Depth of this node in the octree
        self.max_depth = max_depth  # Maximum depth allowed for subdivision
        self.is_leaf = True  # True if the node is a leaf (contains points, not subdivided)
        self.points = []  # Points contained in this node if it's a leaf
        self.children = [None] * 8  # Array for the 8 child octants (subdivided regions)

    def insert(self, point):
        """
        Insert a point into the octree. If the node is a leaf and has too many points, it subdivides.

        Args:
            point (array): A 3D point (x, y, z) to be inserted into the octree.
        """
        if self.is_leaf:
            self.points.append(point)  # Add point to the current leaf node
            # If the number of points exceeds a threshold (8 points here) and depth is within limit:
            if len(self.points) > 8 and self.depth < self.max_depth:
                self.subdivide()  # Subdivide the node into 8 child octants
                # Re-insert all the points into the correct children nodes
                for p in self.points:
                    self._insert_in_child(p)
                self.points = []  # Clear the points list once subdivided
        else:
            # If it's already subdivided, directly insert the point into the correct child
            self._insert_in_child(point)

    def _insert_in_child(self, point):
        """
        Helper function to insert a point into one of the 8 children based on its location.

        Args:
            point (array): A 3D point (x, y, z).
        """
        index = 0  # This index determines in which of the 8 child octants the point belongs
        if point[0] > self.center[0]: index |= 1
        if point[1] > self.center[1]: index |= 2
        if point[2] > self.center[2]: index |= 4
        
        # Create a child node if it doesn't exist
        if not self.children[index]:
            new_min_bound = self.min_bound.copy()
            new_max_bound = self.max_bound.copy()
            # Adjust the bounds to form the child octant based on the index
            if index & 1: new_min_bound[0] = self.center[0]
            else: new_max_bound[0] = self.center[0]
            if index & 2: new_min_bound[1] = self.center[1]
            else: new_max_bound[1] = self.center[1]
            if index & 4: new_min_bound[2] = self.center[2]
            else: new_max_bound[2] = self.center[2]
            # Create the child octant node
            self.children[index] = OctreeNode(new_min_bound, new_max_bound, self.depth + 1, self.max_depth)
        # Insert the point into the appropriate child node
        self.children[index].insert(point)

    def subdivide(self):
        """
        Subdivide this node into 8 child octants. Each octant represents a smaller region of space.
        """
        self.is_leaf = False  # After subdivision, this node is no longer a leaf

    def count_voxels(self):
        """
        Count the number of voxels (leaf nodes) in the octree.

        Returns:
            int: Number of leaf nodes (each representing a voxel).
        """
        if self.is_leaf:
            return 1  # Each leaf node represents one voxel
        # Recursively count the voxels in child nodes
        return sum(child.count_voxels() for child in self.children if child)

# ---- Point Sampling and Octree Building ----
def sample_surface_points(mesh_name, num_samples=10000):
    """
    Sample points on the surface of the given mesh.

    Args:
        mesh_name (str): Name of the mesh in Maya.
        num_samples (int): Number of points to sample on the mesh surface.

    Returns:
        np.array: Array of sampled 3D points on the mesh surface.
    """
    sel_list = om.MSelectionList()
    sel_list.add(mesh_name)
    dag_path = sel_list.getDagPath(0)
    mesh_fn = om.MFnMesh(dag_path)
    
    points = mesh_fn.getPoints(om.MSpace.kWorld)  # Get the mesh vertices in world space
    faces = mesh_fn.getTriangles()[1]  # Get mesh faces (triangles)
    face_ids = np.random.choice(len(faces), num_samples, replace=True)  # Randomly select faces
    
    sampled_points = []
    # For each selected face, sample a point by averaging the face vertices
    for face_id in face_ids:
        p1, p2, p3 = [points[i] for i in mesh_fn.getPolygonVertices(face_id)]
        sampled_points.append(np.mean([p1, p2, p3], axis=0))  # Take the mean of vertices as sample
    
    return np.array(sampled_points)

def build_octree(points, max_depth=5):
    """
    Build an octree from the sampled surface points.

    Args:
        points (np.array): 3D points sampled from the mesh surface.
        max_depth (int): Maximum depth for the octree.

    Returns:
        OctreeNode: Root node of the octree.
    """
    # Compute the bounding box of the points
    min_bound = np.min(points, axis=0)
    max_bound = np.max(points, axis=0)
    # Create the root node of the octree covering the entire bounding box
    octree = OctreeNode(min_bound, max_bound, max_depth=max_depth)
    
    # Insert all points into the octree
    for point in points:
        octree.insert(point)
    
    return octree

# ---- Octree Comparison ----
def compare_octrees(octreeA, octreeB):
    """
    Compare two octrees using Intersection over Union (IoU) metric.

    Args:
        octreeA (OctreeNode): Octree for mesh A.
        octreeB (OctreeNode): Octree for mesh B.

    Returns:
        float: IoU score representing the similarity between the two meshes.
    """
    voxelsA = octreeA.count_voxels()  # Number of voxels in octree A
    voxelsB = octreeB.count_voxels()  # Number of voxels in octree B
    
    intersection = _compare_octree_nodes(octreeA, octreeB)  # Count the intersecting voxels
    union = voxelsA + voxelsB - intersection  # Union of voxels
    
    return intersection / union if union != 0 else 0  # Return IoU score

def _compare_octree_nodes(nodeA, nodeB):
    """
    Recursively compare two octree nodes to find the number of intersecting voxels.

    Args:
        nodeA (OctreeNode): Node from octree A.
        nodeB (OctreeNode): Node from octree B.

    Returns:
        int: Number of intersecting voxels (overlapping regions).
    """
    # If both nodes are leaves, we count one intersection
    if nodeA.is_leaf and nodeB.is_leaf:
        return 1
    # If one node is a leaf and the other is not, there is no overlap
    if nodeA.is_leaf or nodeB.is_leaf:
        return 0
    
    # Recursively compare the children of the two nodes
    intersection = 0
    for i in range(8):
        if nodeA.children[i] and nodeB.children[i]:
            intersection += _compare_octree_nodes(nodeA.children[i], nodeB.children[i])
    
    return intersection

# ---- Main Function to Find Most Similar Mesh ----
def find_most_similar_mesh(meshA, meshesB, max_depth=5, num_samples=10000):
    """
    Find the mesh from meshesB that is most similar to meshA using an octree-based comparison.

    Args:
        meshA (str): Name of the reference mesh A.
        meshesB (list of str): List of mesh names to compare against.
        max_depth (int): Maximum depth of the octree.
        num_samples (int): Number of surface points to sample from each mesh.

    Returns:
        tuple: (best_match, best_score) where best_match is the name of the most similar mesh, 
               and best_score is the IoU similarity score.
    """
    # Sample points and build an octree for meshA
    pointsA = sample_surface_points(meshA, num_samples)
    octreeA = build_octree(pointsA, max_depth=max_depth)
    
    best_match = None  # Variable to store the best match
    best_score = 0  # Variable to store the highest similarity score
    
    # Compare meshA's octree with each mesh in meshesB
    for meshB in meshesB:
        pointsB = sample_surface_points(meshB, num_samples)  # Sample points from meshB
        octreeB = build_octree(pointsB, max_depth=max_depth)  # Build octree for meshB
        
        score = compare_octrees(octreeA, octreeB)  # Compare the octrees using IoU
        print(f"Similarity score for {meshB}: {score}")
        
        # If this score is the highest, update the best match
        if score > best_score:
            best_score = score
            best_match = meshB
    
    return best_match, best_score  # Return the best match and its similarity score

# ---- Example Usage ----
meshA = 'pCube1'  # Name of the reference mesh
meshesB = ['pSphere1', 'pCone1', 'pTorus1']  # List of meshes to compare

best_match, score = find_most_similar_mesh(meshA, meshesB)
print(f"The most similar mesh to {meshA} is {best_match} with a similarity score of {score}")



'''
Verbose documentation:
Detailed Explanations:
Octree Node (OctreeNode class):

The octree divides 3D space into smaller regions recursively. Each node in the tree represents a region of space, defined by a bounding box (min_bound and max_bound).
Each node can either contain points (making it a leaf node) or it can subdivide into 8 child nodes (octants) if it contains too many points.
This hierarchical division allows us to efficiently store and compare 3D spatial data without needing to use a fixed grid for the entire space.
Bounding Box:

The bounding box is used for spatial organization only. It helps determine how to subdivide space and where to place points. We are not directly comparing bounding boxes but rather using them to efficiently divide space into octants.
The actual shape of the mesh is captured by sampling surface points, which are then organized into the octree. The comparison is done based on the distribution of these points, not the bounding box itself.
Point Sampling (sample_surface_points function):

We sample a specified number of points from the surface of each mesh. These points represent the geometry of the mesh and are used to construct the octree.
The MFnMesh class from the Maya API is used to access the mesh’s vertices and faces. We randomly select triangles on the surface and sample points from them.
Octree Construction (build_octree function):

We insert the sampled points into the octree, starting with a root node that covers the entire bounding box of the points.
As points are inserted, the octree subdivides itself if the number of points in a region exceeds a threshold (8 points in this case). This subdivision stops when the maximum depth is reached or the points are sufficiently divided.
Shape Comparison (compare_octrees function):

The comparison between two meshes is done by comparing their octrees using the Intersection over Union (IoU) metric.
We count the number of leaf nodes (voxels) in each octree and compute the number of intersecting voxels between the two octrees. The IoU score is the ratio of the intersection to the union of the voxels, providing a measure of similarity.
Finding the Most Similar Mesh (find_most_similar_mesh function):

This function builds an octree for meshA and compares it with each mesh in meshesB.
The comparison is based on the IoU score, and the mesh with the highest score is considered the most similar to meshA.
Summary of the Bounding Box Role:
The bounding box is not used directly for shape comparison. Instead, it helps divide space efficiently into octants, which contain points that represent the actual shape of the mesh.
We compare the shapes of the meshes by sampling points from their surfaces and organizing those points into octree structures. The octrees are then compared based on how their occupied regions overlap (using the IoU metric).
This method provides a robust way to compare complex 3D shapes while keeping memory and computation efficient through the use of the octree. Let me know if you'd like to explore any further details or enhancements!

'''