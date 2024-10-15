import maya.cmds as cmds
import decorator
def gather_joint_hier(root_joint):
    """
    Recursively gathers information about the joint hierarchy, including jointOrient and position.

    Args:
        root_joint (str): The name of the root joint.

    Returns:
        dict: A dictionary containing joint information (name, position, size, jointOrient, and parent).
    """
    joint_data = {}

    def recursive_gather(joint, parent=None):
        # Get joint attributes
        position = cmds.joint(joint, query=True, position=True)
        joint_orient = cmds.getAttr(f"{joint}.jointOrient")[0]
        size = cmds.getAttr(f"{joint}.radius")
        
        # Store the data with parent information
        joint_data[joint] = {
            'position': position,
            'jointOrient': joint_orient,
            'size': size,
            'parent': parent  # Track the parent of the joint
        }
        
        # Get children and continue recursively
        children = cmds.listRelatives(joint, type='joint', children=True) or []
        for child in children:
            recursive_gather(child, joint)  # Pass the current joint as the parent

    recursive_gather(root_joint)
    
    # Debugging output to check values
    print("Gathered Joint Hierarchy Data:")
    for joint, data in joint_data.items():
        print(f"Joint: {joint}, Data: {data}")
        
    return joint_data



################# Usage ################
joint_data = gather_joint_hier("joint1")
########################################


@decorator.sel_restore
def rebuild_joint_hier(joint_data, prefix='', suffix='_new', ):
    """
    Rebuilds a joint hierarchy from the provided joint data, creating and parenting joints in one step.

    Args:
        joint_data (dict): A dictionary containing joint hierarchy information.
        prefix (str): A string to prefix each joint name.
        suffix (str): A string to suffix each joint name. Defaults to '_new'.
        inherit_parent_orient (bool): Whether to inherit the joint's parent orientation if it's an end bone.
    
    Raises:
        RuntimeError: If a joint with the same name already exists.
    """
    created_joints = {}
    cmds.select(cl=True)
    # Create joints and parent them in one step
    for joint_name in joint_data:
        # Modify name with prefix and suffix
        new_name = f"{prefix}{joint_name}{suffix}"
        
        # Check if joint exists
        if cmds.objExists(new_name):
            raise RuntimeError(f"Joint '{new_name}' already exists. Please use a different prefix or suffix.")

        # Get the joint data
        data = joint_data[joint_name]
        position = data['position']
        joint_orient = data['jointOrient']
        size = data['size']
        
        # Determine the parent joint if it exists
        parent_joint = data.get('parent', None)
        if parent_joint:
            parent_name = f"{prefix}{parent_joint}{suffix}"
            if cmds.objExists(parent_name):
                cmds.select(parent_name)  # Set the parent joint as the selected joint
            else:
                cmds.select(clear=True)  # Clear selection if the parent does not exist

        # Create the joint with position and radius
        new_joint = cmds.joint(name=new_name, position=position, radius=size)
        # Set the joint orientation to ensure correct values
        cmds.joint(new_joint, edit=True, orientation=joint_orient)

        # Check if the joint is an end bone (no children)
        children = cmds.listRelatives(joint_name, type='joint', children=True) or []

        # Store the created joint
        created_joints[joint_name] = new_joint

    # Debugging output to check values
    print("Rebuilt Joint Hierarchy with Creation and Parenting in One Step:")
    for joint_name in joint_data:
        print(f"Joint: {joint_name}, Data: {joint_data[joint_name]}")
# ########################### Usage ######################
# joint_data = gather_joint_hier("joint1")
# rebuild_joint_hier(joint_data, prefix='', suffix='_new')
# ########################################################

