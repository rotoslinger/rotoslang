import importlib
import math

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2

import decorator
importlib.reload(decorator)


def matrix_to_euler_and_translate(flat_matrix):
    """
    Args:
        flat_matrix (list): A flat list representing a 4x4 matrix (16 elements).
    
    Returns:
        tuple: (translation, euler_rotation) where translation is a tuple of x, y, z values
               and euler_rotation is a tuple of x, y, z rotation in degrees.
    """
    
    # Create an MMatrix from the flat list
    m_matrix = om2.MMatrix(flat_matrix)
    
    # Create MTransformationMatrix from MMatrix
    m_transform_matrix = om2.MTransformationMatrix(m_matrix)
    
    # Extract translation
    translation = m_transform_matrix.translation(om2.MSpace.kWorld)
    translation = (translation.x, translation.y, translation.z)
    
    # Extract Euler rotation (in radians) and convert to degrees
    euler_rotation_rad = m_transform_matrix.rotation(asQuaternion=False)
    euler_rotation_deg = (
        om2.MAngle(euler_rotation_rad.x).asDegrees(),
        om2.MAngle(euler_rotation_rad.y).asDegrees(),
        om2.MAngle(euler_rotation_rad.z).asDegrees()
    )
    
    return translation, euler_rotation_deg

def euler_and_translate_to_matrix(translation, euler_rotation):
    """
    Args:
        translation (tuple): The translation as (x, y, z).
        euler_rotation (tuple): The Euler rotation in degrees as (x, y, z).
    
    Returns:
        list: A flat list representing a 4x4 matrix (16 elements).
    """
    
    # Convert Euler rotation to radians
    euler_rotation_rad = (
        om2.MAngle(euler_rotation[0], om2.MAngle.kDegrees).asRadians(),
        om2.MAngle(euler_rotation[1], om2.MAngle.kDegrees).asRadians(),
        om2.MAngle(euler_rotation[2], om2.MAngle.kDegrees).asRadians()
    )
    
    # Create an MTransformationMatrix
    m_transform_matrix = om2.MTransformationMatrix()
    
    # Set translation
    m_transform_matrix.setTranslation(om2.MVector(translation), om2.MSpace.kWorld)
    
    # Set Euler rotation
    m_euler_rotation = om2.MEulerRotation(euler_rotation_rad)
    m_transform_matrix.setRotation(m_euler_rotation)
    
    # Convert MTransformationMatrix back to MMatrix
    m_matrix = m_transform_matrix.asMatrix()
    
    # Convert MMatrix to a flat list (16 elements)
    flat_matrix = [m_matrix(i, j) for i in range(4) for j in range(4)]
    
    return flat_matrix

# For visualizing matrices

def euler_to_matrix(rx=0, ry=0, rz=0):
    """
    Args:
        x_deg (float): Rotation around the X-axis in degrees.
        y_deg (float): Rotation around the Y-axis in degrees.
        z_deg (float): Rotation around the Z-axis in degrees.
    
    Prints:
        A readable 4x4 transformation matrix.
    """
    # Convert degrees to radians
    x_rad = math.radians(rx)
    y_rad = math.radians(ry)
    z_rad = math.radians(rz)
    
    # Rotation matrices around X, Y, Z axes
    rx = [
        [1, 0, 0, 0],
        [0, math.cos(x_rad), -math.sin(x_rad), 0],
        [0, math.sin(x_rad), math.cos(x_rad), 0],
        [0, 0, 0, 1]
    ]
    
    ry = [
        [math.cos(y_rad), 0, math.sin(y_rad), 0],
        [0, 1, 0, 0],
        [-math.sin(y_rad), 0, math.cos(y_rad), 0],
        [0, 0, 0, 1]
    ]
    
    rz = [
        [math.cos(z_rad), -math.sin(z_rad), 0, 0],
        [math.sin(z_rad), math.cos(z_rad), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    
    # Matrix multiplication function (for 4x4 matrices)
    def matrix_mult(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
    
    # Combine the rotations: first X, then Y, then Z
    rxy = matrix_mult(rx, ry)
    rotation_matrix = matrix_mult(rxy, rz)
    
    # Print the matrix in a readable format
    print("Transformation Matrix:")
    for row in rotation_matrix:
        print(" ".join(f"{val:.6f}" for val in row))

# Example usage
# euler_to_matrix(45, 30, 60)







@decorator.suppress_pose_editor
def addrbf(joint_name='L_arm00Out_jnt',
            control_name='L_fkArm00_ctrl',
            control_attrs = ['rx', 'ry', 'rz'],
            rom_dict = {'ry':[45,90, 135, -45, -90, -135],
                        'rz':[45,90, 135, -45, -90, -135]},
            pose_type = "swing",
            nuetral_val = 0, 
            blendshape_node='teshi_base_body_geo_bodyMechanics_skinCluster'):
    pass




@decorator.suppress_pose_editor
def add_pose_interpolator(joint_name='L_arm00Out_jnt',
                          control_name='L_fkArm00_ctrl',
                          control_attrs = ['rx', 'ry', 'rz'],
                          rom_dict = {'ry':[45,90, 135, -45, -90, -135],
                                      'rz':[45,90, 135, -45, -90, -135]},
                          pose_type = "swing",
                          nuetral_val = 0, 
                          blendshape_node='teshi_base_body_geo_bodyMechanics_skinCluster'):
    # possible pose types, default to swing as that is just the ry and rz
    # 'swingandtwist' 'swing' 'twist'
    # make certain you are on a value of 0 to start
    for attr in control_attrs:
        cmds.setAttr(f'{control_name}.{attr}', nuetral_val)

    # the eval needs a selection grrr
    # this is why suppress_pose_editor decorator has it's own decorator to restore selection, sigh
    cmds.select(joint_name)
    pose_interp_xform = mel.eval(f'createPoseInterpolatorNode( "{joint_name}_pi", 0, 0);')
    print(pose_interp_xform)
    pose_interp_shp = mel.eval(f'poseInterpolatorShape( "{pose_interp_xform}");')
    # connect the controller attrs
    for idx, attr in enumerate(control_attrs):
        idx = idx+1
        cmds.connectAttr(f'{control_name}.{attr}', f'{pose_interp_shp}.driver[0].driverController[{idx}]')
    mel.eval(f'createNeutralPoses( "{pose_interp_shp}");')
    for attr in rom_dict:
        cmds.setAttr(f'{control_name}.{attr}', 0)
        for val in rom_dict[attr]:
            cmds.setAttr(f'{control_name}.{attr}', val)
            '''	int $poseTypeIdx = 0;
                if ($poseType == "swingandtwist")
                    $poseTypeIdx = 0;
                else if ($poseType == "swing")
                    $poseTypeIdx = 1;
                else if ($poseType == "twist")
                    $poseTypeIdx = 2;
            '''
            f'poseInterpolatorAddShapePose(string $tpl, string $poseName, {pose_type}, [{blendshape_node}], 0)'
            cmds.pause(sec=1)
            cmds.refresh()
        cmds.setAttr(f'{control_name}.{attr}', nuetral_val)



    
    # global proc int poseInterpolatorAddShapePose(string $tpl, string $poseName, string $poseType, string $blendShapes[], int $startEdit)

    # create nuetral poses
    # update nuetral at nuetral pose

    # loop through attrs and add poses in the rom
    # make sure to not invert shape on creation, it is very f'ing important




    # return pose_interp









# @decorator.sel_restore
# def add_pose_interpolator(joint_name="upperarm_l", blendshape_node="blendShape1"):
#     """
#     Adds a pose interpolator for the specified joint.
    
#     Args:
#         joint_name (str): The name of the joint to use as a driver for the pose interpolator.
#     """
#     cmds.select(joint_name)

#     # Perform the interpolator add operation
#     mel.eval('performInterpolatorAdd 0;')
#     pose_interpolator = f'{joint_name}_poseInterpolator'


#     print(pose_interpolator)
#     cmds.parent(pose_interpolator, joint_name)
    

#     # create neutral poses
#     'L_arm00Out_jnt_poseInterpolator'
#     mel.eval(f'createNeutralPoses {pose_interpolator}')



    
#     # set value of rx, ry, rz
#     mel.eval(f"sculptTarget -e -target -1 {blendshape_node}")
    
#     # 8. Set sculpt target index (not available in cmds)
#     mel.eval("setSculptTargetIndex blendShape1 -1 1 1")




# def add_pose_interpolator(joint_name = 'upperarm_l',
#                           blendshape_node="blendShape1",
#                           control_name='arm_control',
#                           rom={}):
#     control_out_rx = f'{control_name}.rx'
#     control_out_ry = f'{control_name}.ry'
#     control_out_rz = f'{control_name}.rz'
#     rom = {('rx'):[0,45,90, 135, -45, -90, -135]}


# # def build_pose_interpolator(create_or_import=0, joint_name="", control_name=''):
# #     '''Args
# #     Creation, or import
# #     Bool Import
# #     String Bone
# #     String Control = “arm.outMatrix”
# #     String Blendshape
# #     '''
# #     driving_control = ""
# #     rom = {('rx'):[0,45,90, 135, -45, -90, -135]}


# def build_pose_system(create_or_import=0, joint_name="", ):
#    pass


# def update_pose_interp(rom = {('rx'):[0,45,90, 135, -45, -90, -135]}):

#     pass