import maya.cmds as cmds
import maya.mel as mel
import importlib
import decorator
importlib.reload(decorator)




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