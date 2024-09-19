import maya.cmds as cmds

def scale_policube_to_mesh(mesh_name, polycube):
    # Get the bounding box of the mesh
    bbox = cmds.exactWorldBoundingBox(mesh_name)
    min_x, min_y, min_z = bbox[0], bbox[1], bbox[2]
    max_x, max_y, max_z = bbox[3], bbox[4], bbox[5]

    # Get the dimensions of the bounding box
    width = max_x - min_x
    height = max_y - min_y
    depth = max_z - min_z

    # Get the dimensions of the polycube
    polycube_bbox = cmds.exactWorldBoundingBox(polycube)
    polycube_min_x, polycube_min_y, polycube_min_z = polycube_bbox[0], polycube_bbox[1], polycube_bbox[2]
    polycube_max_x, polycube_max_y, polycube_max_z = polycube_bbox[3], polycube_bbox[4], polycube_bbox[5]

    polycube_width = polycube_max_x - polycube_min_x
    polycube_height = polycube_max_y - polycube_min_y
    polycube_depth = polycube_max_z - polycube_min_z

    # Calculate the scaling factors
    scale_x = width / polycube_width
    scale_y = height / polycube_height
    scale_z = depth / polycube_depth

    # Scale the polycube to match the dimensions of the mesh
    cmds.scale(scale_x, scale_y, scale_z, polycube)

    # Move the polycube to align with the mesh
    cmds.move(min_x + width / 2.0, min_y + height / 2.0, min_z + depth / 2.0, polycube)

def create_dummy_cubes_for_meshes():
    # Find all meshes in the scene
    meshes = cmds.ls(type='mesh')
    
    for mesh in meshes:
        # Get the transform node of the mesh
        transform = cmds.listRelatives(mesh, parent=True)[0]
        
        # Create a polycube and rename it
        polycube = cmds.polyCube(name = transform + "_DUMMY")[0]
        
        # Scale and move the polycube to match the mesh bounds
        scale_policube_to_mesh(transform, polycube)

# Run the script
create_dummy_cubes_for_meshes()




