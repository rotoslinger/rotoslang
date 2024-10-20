from maya import cmds


def pre_import(char_name):
    # cleanly delete the old blendshape without deleting any Minimo nodes.
    '''
    ---background
    Maya automatically does garbage collection.

    When the blendshape is deleted using the ui the Minimo nodes for driving
    the blendshape weights are also deleted.

    This script will first delete connections, then delete the blendshape,
    then SHAPES can properly rebuild all of the connections 
    '''
    node = f"M_{char_name}_base_body_geoShapes_blendShape"
    compound_attr = 'weight'
    # Get the full path of the compound attribute (node + compound attribute)
    full_attr = f'{node}.weight'
    # Get all indices for the compound array
    bs_weight_names = cmds.listAttr(full_attr, multi=True)
    connections = []
    for name in bs_weight_names:
        full_attr = f'{node}.{name}'
        connections.append(cmds.listConnections(full_attr, plugs=True, source=True, destination=False)[0])
        print(connections)
    for idx, name in enumerate(bs_weight_names):
        print(f'{node}.{name}')
        print(connections[idx])
        cmds.disconnectAttr(connections[idx], f'{node}.{name}')
    cmds.delete(f"M_{char_name}_base_body_geoShapes_blendShape")

def post_import(char_name):
    # if a second ShapeOrig was created, delete it, the node network will not be interrupted 
    if cmds.objExists(f"{char_name}_base_body_geoShapeOrig1"):
        cmds.delete(f"{char_name}_base_body_geoShapeOrig1")
        print("deleted")

def select_blendshape(char_name):
    # important to keep an eye on the blendshape in node editor
    # use this script to easily select it
    cmds.select(f"M_{char_name}_base_body_geoShapes_blendShape")