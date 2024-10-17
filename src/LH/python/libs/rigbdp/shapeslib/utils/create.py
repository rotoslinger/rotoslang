import maya.cmds as cmds
import maya.mel as mel

'''



createPoseInterpolatorNode(string $nodeName, int $flagCreateNeutralPose, int $flagDriverTwistAxis)
    returns tpl (transform of poseInterpolator node)

global proc int createNeutralPoses(string $nodeName)
    returns 1 if successful 0 if not


poseInterpolatorAddPose(string $tpl, string $poseName)
    returns poseIndex

poseInterpolatorAddShapePose(string $tpl, string $poseName, string $poseType, string $blendShapes[], int $startEdit)
    returns poseIndex
'''

def refresh_shapes_ui(mesh = "teshi_base_body_geo"):
    # Select the geometry
    cmds.select(mesh)
    mel.eval('SHAPES')
    # Run the MEL commands equivalent in Python
    mel.eval('shapesMain_getMeshSelection 0')

# Example usage of the function
# refresh_shapes_ui(mesh = "teshi_base_body_geo")

import maya.cmds as cmds
import maya.mel as mel

def process_pose_interpolator(empty_target, blendshape_node, next_available_index):
    """
    Processes pose interpolation and allows for a customizable empty target, blendshape node, 
    and next available index for the blendshape target list.

    Args:
        empty_target (str): The name of the empty target to be used in aliasAttr and shapesJob_compareInbetweenValues.
        blendshape_node (str): The name of the blendshape node to edit.
        next_available_index (int): The next available index in the blendshape target list.

    Postscript:
        This function executes multiple MEL and Maya commands, some of which print their results for debugging purposes.
    """
    # Unused variable: 1
    cmds.select('L_fkArm00_ctrl')
    cmds.select(clear=True)

    # Unused variable: 1
    cmds.select('teshi_base_body_geo')
    
    mel.eval('shapesAction_duplicateMeshFromMenu 1 1')
    
    # Using the empty_target and blendshape_node arguments
    mel.eval(f'aliasAttr {empty_target} {blendshape_node}.w[{next_available_index}]')
    
    result = mel.eval('pluginInfo -q -l "poseInterpolator"')
    print(result)  # Unused result, just for display

    rel = cmds.listRelatives(f'{blendshape_node}_L_arm00Out_jnt_PIShape', parent=True, path=True)
    print(rel)  # Unused rel, just for display

    for index in [0, 1, 2, 5]:
        output_value = cmds.getAttr(f'{blendshape_node}_L_arm00Out_jnt_PIShape.output[{index}]')
        print(f'Output at index {index}: {output_value}')  # Unused output_value, just for display

    result = mel.eval('pluginInfo -q -l "poseInterpolator"')
    print(result)  # Unused result, just for display
    
    # Extra attributes processing
    shape_type = mel.eval(f'data.getShapeRangeAttrType("{blendshape_node}_data", {next_available_index})')
    print(shape_type)  # Unused shape_type, just for display

    mel.eval('setFilterScript "initialShadingGroup"')
    
    filter_list = [
        "initialShadingGroup", "initialParticleSE", "defaultLightSet",
        "defaultObjectSet", "teshi_base_fur_C_hair_shadingEngine",
        "teshi_base_blendTarget_body_scm_shadingEngine", 
        "teshi_base_eyes_L_cornea_shadingEngine", "__EXPORT__GEO",
        "__EXPORT__CONTROLS", "__EXPORT__", "__EXPORT__SKEL", 
        "__EXPORT__EYE_OUTPUT", "__EXPORT__BODY_CONTROLS", "__EXPORT__FACE_CONTROLS", 
        "__EXPORT__CLOTH_CONTROLS"
    ]
    for filter_item in filter_list:
        mel.eval(f'setFilterScript "{filter_item}"')

    mel.eval('CBselectionChanged')
    mel.eval('autoUpdateAttrEd')

    cmds.columnLayout('shpUI_weightsServerSettingsColumn', edit=True, manage=True)
    
    current_time = cmds.currentTime(query=True)
    cmds.timeField('TimeSlider|MainTimeSliderLayout|rowLayout1|timeField1', edit=True, value=current_time)

    # Using the empty_target and blendshape_node arguments
    mel.eval(f'shapesJob_compareInbetweenValues {blendshape_node}.{empty_target}')
    
    result = mel.eval('pluginInfo -q -l "poseInterpolator"')
    print(result)  # Unused result, just for display

    for index in [0, 1, 2]:
        output_value = cmds.getAttr(f'{blendshape_node}_L_arm00Out_jnt_PIShape.output[{index}]')
        print(f'Output at index {index}: {output_value}')  # Unused output_value, just for display

    current_time = cmds.currentTime(query=True)
    cmds.timeField('TimeSlider|MainTimeSliderLayout|rowLayout1|timeField1', edit=True, value=current_time)

    mel.eval(f'shapesJob_compareInbetweenValues {blendshape_node}.{empty_target}')
    mel.eval(f'shapesAction_renameCorrective "emptyTarget" "{empty_target}";')
    # mel.eval(f'columnLayout -e -m 1 shpUI_weightsServerSettingsColumn;')


# Example call with the new arguments
refresh_shapes_ui(mesh = "teshi_base_body_geo")
process_pose_interpolator(empty_target="newSHAPEname", blendshape_node="M_teshi_base_body_geoShapes_blendShape", next_available_index=15)
refresh_shapes_ui(mesh = "teshi_base_body_geo")














import maya.cmds as cmds
import maya.mel as mel

# Perform the interpolator add operation
mel.eval("performInterpolatorAdd 0;")

# Check if the pose interpolator plugin is loaded
plugin_loaded = mel.eval("pluginInfo -q -l 'poseInterpolator';")

if plugin_loaded:
    # List the parent of the pose interpolator shape
    pose_interpolator_shape = "upperarm_l_poseInterpolatorShape"
    parent_shape = cmds.listRelatives(pose_interpolator_shape, parent=True, path=True)[0]
    print(f"Parent shape: {parent_shape}")

    # Add the joint as a driver for the pose interpolator
    mel.eval(f"poseInterpolatorDrivers '|{parent_shape}|{pose_interpolator_shape}';")

    # Get the driver index
    driver_index = mel.eval(f"poseInterpolatorDriverIndex '|{parent_shape}|{pose_interpolator_shape}' 'upperarm_l';")
    print(f"Driver index: {driver_index}")

    # Get the driver name
    driver_name = mel.eval(f"poseInterpolatorDriverName '|{parent_shape}|{pose_interpolator_shape}' {driver_index};")
    print(f"Driver name: {driver_name}")

    # Check if pose editor group is selected
    pose_editor_enabled = mel.eval("isPoseEditorGroupSelectedPIEnabled;")

    # Check if a pose is selected
    pose_selected = mel.eval("isPoseEditorPIRefItemSelected;")

    # Check if adding a pose is enabled
    add_pose_enabled = mel.eval("isPoseEditorAddPoseEnabled;")

    # Check for the shape again
    parent_shape_again = cmds.listRelatives(pose_interpolator_shape, parent=True, path=True)[0]
    print(f"Parent shape again: {parent_shape_again}")

    # More plugin checks
    for _ in range(7):  # Repeating the check multiple times
        assert mel.eval("pluginInfo -q -l 'poseInterpolator';") == 1
        parent_shape_check = cmds.listRelatives(pose_interpolator_shape, parent=True, path=True)[0]
        print(f"Parent shape check: {parent_shape_check}")

    # Create Pose Interpolator Node
    mel.eval(f"createPoseInterpolatorNode {parent_shape} 1 0;")




    # # Select the joint
    # cmds.select(clear=True)
    # cmds.select(add=True, "upperarm_l")

    # # Set various filter scripts
    # filter_scripts = [
    #     "initialShadingGroup", "initialParticleSE", "defaultLightSet",
    #     "defaultObjectSet", "lambert2SG", "lambert3SG", "lambert4SG",
    #     "lambert5SG", "Tail:lambert2SG", "blinn1SG", "SKM_BungeeManSG",
    #     "SKM_BungeeManSG1", "Skeleton:SKM_BungeeManSG", "Skeleton:SKM_BungeeManSG1",
    #     "PantsSelect", "TailSelect", "set1", "TorsoArmSelection", 
    #     "TorsoSelect", "LLegSelect", "RLegSelect", "topoSymmetrySet",
    #     "EarsSelect", "HeadSelect"
    # ]

    # for script in filter_scripts:
    #     mel.eval(f'setFilterScript "{script}";')

    # # List all mayaUsdProxyShapeBase types
    # usd_shapes = cmds.ls(type="mayaUsdProxyShapeBase", long=True)
    # print(f"USD Shapes: {usd_shapes}")

    # # Check the selection and other state updates
    # mel.eval("CBselectionChanged;")
    # mel.eval("refreshAE;")
    
    # # History checks for the specified joint
    # joint_history = cmds.listHistory("|root|pelvis|spine_01|spine_02|spine_03|spine_04|spine_05|spine_06|clavicle_l|upperarm_l", pdo=True, lf=False, il=2)
    # print(f"Joint history: {joint_history}")

    # # Menu item enables based on various conditions
    # cmds.menuItem("editMIGroup", edit=True, enable=mel.eval("isPoseEditorGroupSelectedPIEnabled;"))
    # cmds.menuItem("fileExportSelection", edit=True, enable=mel.eval("isPoseEditorExportSelectionEnabled;"))
    # cmds.menuItem("posesMIAddPose", edit=True, enable=mel.eval("isPoseEditorAddPoseEnabled;"))
    # cmds.menuItem("posesMIUpdatePose", edit=True, enable=mel.eval("isPoseEditorUpdatePosesEnabled;"))
    # cmds.menuItem("posesMIAddNeutralPoses", edit=True, enable=mel.eval("isPoseEditorAddNeutralPosesEnabled;"))
    # cmds.menuItem("posesMIMirrorPose", edit=True, enable=mel.eval("isPoseEditorPIorPoseMirrorEnabled;"))

    # # Additional updates
    # mel.eval("autoUpdateAttrEd;")
    # mel.eval("updateAnimLayerEditor('AnimLayerTab');")
    # mel.eval("statusLineUpdateInputField;")

    # # Check for existence and update commands
    # if not cmds.runTimeCommand("polyNormalSizeMenuUpdate", exists=True):
    #     mel.eval("source buildDisplayMenu;")
    # mel.eval("polyNormalSizeMenuUpdate;")

    # # Update selection menus
    # cmds.menuItem("seMIAddSelectionAsCombinationTarget", edit=True, enable=mel.eval("isAddSelectionAsCombinationTargetToSelectedBSDEnabled;"))
    # cmds.menuItem("seMIAddSelectionAsTarget", edit=True, enable=mel.eval("isAddSelectionAsTargetToSelectedBSDEnabled;"))
    # cmds.menuItem("seMIAddSelectionAsInBetweenTarget", edit=True, enable=mel.eval("isAddSelectionAsInBetweenTargetEnabled;"))

    # # Update command panel and time field
    # mel.eval("dR_updateCommandPanel;")
    # cmds.timeField("TimeSlider|MainTimeSliderLayout|rowLayout1|timeField1", edit=True, value=mel.eval("currentTime -query;"))

    # # Marking menu updates
    # mel.eval("MarkingMenuPopDown;")
    # for temp_menu in ["tempMM", "tempMM2"]:
    #     if cmds.popupMenu(temp_menu, exists=True):
    #         cmds.deleteUI(temp_menu)

    # mel.eval("MarkingMenuPopDown;")
