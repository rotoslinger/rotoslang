# builtins
import importlib, os, sys, json

# third party
from maya import cmds
from maya import mel
# bdp
from rigbdp import decorator
from rigbdp.import_export import file as file_utils
from rigbdp import import_export
# from rigbdp import decorator

# reloads (DELETE_ME)
importlib.reload(decorator)
importlib.reload(file_utils)

@decorator.restore_selection
def export_animation_to_json(control_list=[], file_path=""):
    """Export animation keyframes from specified controls to a JSON file."""
    animation_data = {}
    if not file_path:
        file_path = import_export.get_scene_dir() + "rom.json"
    if not control_list:
        cmds.select('__EXPORT__CONTROLS')
        mel.eval('CBselectionChanged;')
        control_list = cmds.ls(sl=True)

    for control in control_list:
        if cmds.objExists(control):
            keyframes = cmds.keyframe(control, query=True, timeChange=True)
            if keyframes:
                animation_data[control] = {}
                for key in keyframes:
                    value = cmds.getAttr(control + '.translate')
                    animation_data[control][key] = {
                        'translateX': cmds.getAttr(control + '.translateX', time=key),
                        'translateY': cmds.getAttr(control + '.translateY', time=key),
                        'translateZ': cmds.getAttr(control + '.translateZ', time=key),
                        'rotateX': cmds.getAttr(control + '.rotateX', time=key),
                        'rotateY': cmds.getAttr(control + '.rotateY', time=key),
                        'rotateZ': cmds.getAttr(control + '.rotateZ', time=key)
                    }

    # Write the animation data to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(animation_data, json_file, indent=4)
    print(f'Animation data exported to {file_path}')

####################################################### Example usage ##########################################################
# controls = ['M_spineChestFkGimbal_ctrl', 'M_spineDrivenIk02_ctrl', 'L_handReverseRollFinger_ctrl', 'M_spineDriverLastTangent_ctrl', 'R_handPinky01_ctrl', 'M_neckHeadIk00_ctrl', 'R_footReverseRollHeel_ctrl', 'L_handThumb00Gimbal_ctrl', 'L_clavicle_ctrl', 'L_handThumb02_ctrl', 'R_ikArmHandleGimbal_ctrl', 'M_spineBellyIk_ctrl', 'L_handIndex00_ctrl', 'R_handIndex01Gimbal_ctrl', 'L_ikLegHandle_ctrl', 'L_fkArm01Gimbal_ctrl', 'R_handRing01Gimbal_ctrl', 'M_neckHeadFk00Gimbal_ctrl', 'M_neckHeadGimbal_ctrl', 'L_ikArmPV_ctrl', 'L_handReverseBankOutGimbal_ctrl', 'R_fkLeg01_ctrl', 'R_footReverseRollToe_ctrl', 'R_handThumb00Gimbal_ctrl', 'L_ikArmRoot_ctrl', 'L_handIndex02Gimbal_ctrl', 'R_armUpperBendy_ctrl', 'L_handMiddle01Gimbal_ctrl', 'L_fkArm00Gimbal_ctrl', 'L_armSettings_ctrl', 'R_ikLegHandle_ctrl', 'R_ikArmPV_ctrl', 'R_handThumb02_ctrl', 'L_handIndex01_ctrl', 'R_clavicle_ctrl', 'R_handPinky03Gimbal_ctrl', 'L_legSlide_ctrl', 'L_hand_ctrl', 'L_footReverseRollHeelGimbal_ctrl', 'M_all_ctrl', 'M_spineChestIkOffsetPivot_ctrl', 'M_spineBellyFkGimbal_ctrl', 'L_legUpperBendy_ctrl', 'M_spineDriven03Tangent01_ctrl', 'R_handReverseBankIn_ctrl', 'L_footToeGimbal_ctrl', 'R_handReverseBankOutGimbal_ctrl', 'M_spineBreathBelly_ctrl', 'L_footReverseBankIn_ctrl', 'M_spineDrivenIk03_ctrl', 'L_ikLegRoot_ctrl', 'R_handIndex01_ctrl', 'L_fkLeg02Gimbal_ctrl', 'R_handIndex03Gimbal_ctrl', 'L_footReverseBankOutGimbal_ctrl', 'R_handIndex02_ctrl', 'R_handPinky00_ctrl', 'L_foot_ctrl', 'L_handMiddle01_ctrl', 'M_spineLocalHip_ctrl', 'M_spineRoot_ctrl', 'M_neckHeadFk00_ctrl', 'M_spineDriven02Tangent00_ctrl', 'L_footReverseRollToeGimbal_ctrl', 'R_handThumb01Gimbal_ctrl', 'L_handReverseRollBallGimbal_ctrl', 'R_handThumb00_ctrl', 'L_handPinky03_ctrl', 'L_handRing03_ctrl', 'R_foot_ctrl', 'L_armUpperBendy_ctrl', 'R_legLowerBendy_ctrl', 'R_armSettings_ctrl', 'M_spineDriven04Tangent00_ctrl', 'L_footLollipop_ctrl', 'M_world_ctrl', 'R_footToeGimbal_ctrl', 'L_handLollipop_ctrl', 'L_handPinky03Gimbal_ctrl', 'L_handTipSmart_ctrl', 'R_footReverseBankInGimbal_ctrl', 'R_handRing01_ctrl', 'M_spineBellyFk_ctrl', 'R_armSlide_ctrl', 'L_handPinky00Gimbal_ctrl', 'M_spineRootGimbal_ctrl', 'M_spineDrivenIk01_ctrl', 'R_handMiddle01_ctrl', 'R_legUpperBendy_ctrl', 'L_handReverseRollHeelGimbal_ctrl', 'L_handRing03Gimbal_ctrl', 'L_handPinky00_ctrl', 'L_handMiddle02Gimbal_ctrl', 'R_handReverseRollBallGimbal_ctrl', 'L_footReverseRollToe_ctrl', 'L_legLowerBendy_ctrl', 'M_neckHeadIk01_ctrl', 'R_handMiddle00Gimbal_ctrl', 'R_fkLeg02Gimbal_ctrl', 'M_spineDriverFirstTangent_ctrl', 'R_fkArm02_ctrl', 'L_handRing00Gimbal_ctrl', 'L_handIndex01Gimbal_ctrl', 'R_handRing03_ctrl', 'L_footReverseRollBallGimbal_ctrl', 'R_handIndex00_ctrl', 'L_handMiddle02_ctrl', 'L_handMiddle03_ctrl', 'R_hand_ctrl', 'R_handRing02Gimbal_ctrl', 'R_fkArm01_ctrl', 'R_handReverseRollFingerGimbal_ctrl', 'R_handMiddle00_ctrl', 'L_handMiddle03Gimbal_ctrl', 'M_layoutSub_ctrl', 'L_handIndex03Gimbal_ctrl', 'M_spineChestIk_ctrl', 'R_fkArm02Gimbal_ctrl', 'L_armSlide_ctrl', 'R_fkArm00Gimbal_ctrl', 'R_fkLeg00Gimbal_ctrl', 'R_handReverseBankInGimbal_ctrl', 'M_layout_ctrl', 'R_footReverseBankIn_ctrl', 'L_handIndex00Gimbal_ctrl', 'L_ikArmHandle_ctrl', 'R_footReverseRollBall_ctrl', 'R_handThumb02Gimbal_ctrl', 'R_ikLegPV_ctrl', 'R_handReverseRollHeel_ctrl', 'L_handPinky01_ctrl', 'R_handRing02_ctrl', 'M_spineDriven02Tangent01_ctrl', 'L_handReverseBankOut_ctrl', 'R_handLollipop_ctrl', 'M_spineChestFk_ctrl', 'R_handThumb01_ctrl', 'R_fkLeg02_ctrl', 'L_handMiddle00_ctrl', 'L_handRing02_ctrl', 'M_spineUpperChestGimbal_ctrl', 'R_handPinky01Gimbal_ctrl', 'R_armLowerBendy_ctrl', 'M_spineUpperChest_ctrl', 'M_neckHeadSettings_ctrl', 'R_footToe_ctrl', 'L_fkLeg02_ctrl', 'L_ikLegPV_ctrl', 'M_spineDriven01Tangent01_ctrl', 'L_handReverseBankInGimbal_ctrl', 'L_handRing01_ctrl', 'R_handIndex03_ctrl', 'M_spineBreathChest_ctrl', 'R_handMiddle01Gimbal_ctrl', 'L_fkLeg00_ctrl', 'R_handMiddle02_ctrl', 'R_handPinky02_ctrl', 'M_spineDriven03Tangent00_ctrl', 'R_handPinky03_ctrl', 'R_footLollipop_ctrl', 'L_handRing00_ctrl', 'R_fkArm01Gimbal_ctrl', 'L_fkArm01_ctrl', 'R_handReverseRollFinger_ctrl', 'L_handThumb02Gimbal_ctrl', 'M_spineBellyIkGimbal_ctrl', 'L_fkArm00_ctrl', 'R_footReverseRollBallGimbal_ctrl', 'R_legSettings_ctrl', 'L_ikLegHandleGimbal_ctrl', 'R_fkArm00_ctrl', 'L_armLowerBendy_ctrl', 'R_ikArmHandle_ctrl', 'L_handReverseRollBall_ctrl', 'L_fkLeg00Gimbal_ctrl', 'L_handIndex02_ctrl', 'M_spineHipFkGimbal_ctrl', 'R_handMiddle03Gimbal_ctrl', 'R_handIndex00Gimbal_ctrl', 'L_footReverseRollBall_ctrl', 'L_fkArm02_ctrl', 'L_handPinky01Gimbal_ctrl', 'L_ikArmHandleGimbal_ctrl', 'M_spineRootOffsetPivot_ctrl', 'M_spineChestFkOffsetPivot_ctrl', 'R_handReverseRollBall_ctrl', 'R_footReverseBankOut_ctrl', 'L_handPinky02_ctrl', 'L_handThumb01Gimbal_ctrl', 'L_fkLeg01_ctrl', 'R_handIndex02Gimbal_ctrl', 'R_footReverseRollToeGimbal_ctrl', 'R_handRing00Gimbal_ctrl', 'M_spineLocalHipGimbal_ctrl', 'M_spineDriven00Tangent01_ctrl', 'L_fkArm02Gimbal_ctrl', 'R_fkLeg00_ctrl', 'L_handRing02Gimbal_ctrl', 'R_fkLeg01Gimbal_ctrl', 'L_legSettings_ctrl', 'L_handPinky02Gimbal_ctrl', 'R_legSlide_ctrl', 'R_handMiddle02Gimbal_ctrl', 'L_handThumb01_ctrl', 'L_footToe_ctrl', 'R_handRing00_ctrl', 'L_handMiddle00Gimbal_ctrl', 'R_handReverseBankOut_ctrl', 'L_footReverseBankOut_ctrl', 'R_footReverseBankOutGimbal_ctrl', 'R_handPinky02Gimbal_ctrl', 'R_ikLegRoot_ctrl', 'L_footReverseRollHeel_ctrl', 'R_handReverseRollHeelGimbal_ctrl', 'R_handRing03Gimbal_ctrl', 'M_spineHipIk_ctrl', 'L_footReverseBankInGimbal_ctrl', 'M_spineHipIkGimbal_ctrl', 'M_spineChestIkGimbal_ctrl', 'R_ikArmRoot_ctrl', 'L_handReverseRollHeel_ctrl', 'R_handMiddle03_ctrl', 'R_footReverseRollHeelGimbal_ctrl', 'M_spineHipFk_ctrl', 'M_spineDriven01Tangent00_ctrl', 'L_handReverseBankIn_ctrl', 'L_handThumb00_ctrl', 'L_handIndex03_ctrl', 'R_handTipSmart_ctrl', 'L_handRing01Gimbal_ctrl', 'M_neckHead_ctrl', 'L_handReverseRollFingerGimbal_ctrl', 'R_ikLegHandleGimbal_ctrl', 'L_fkLeg01Gimbal_ctrl', 'R_handPinky00Gimbal_ctrl']
# path=r'C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD\animtest\anim.json'
# export_animation_to_json(controls, r'C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD\animtest\anim.json')
####################################################### Example usage ##########################################################

def import_animation_from_json(file_path):
    """Import animation keyframes from a JSON file into specified controls."""
    with open(file_path, 'r') as json_file:
        animation_data = json.load(json_file)
    if not file_path:
        file_path = import_export.get_scene_dir()
    for control, keyframes in animation_data.items():
        if cmds.objExists(control):
            for time, attrs in keyframes.items():
                cmds.setKeyframe(control, time=time, attribute='translateX', value=attrs['translateX'])
                cmds.setKeyframe(control, time=time, attribute='translateY', value=attrs['translateY'])
                cmds.setKeyframe(control, time=time, attribute='translateZ', value=attrs['translateZ'])
                cmds.setKeyframe(control, time=time, attribute='rotateX', value=attrs['rotateX'])
                cmds.setKeyframe(control, time=time, attribute='rotateY', value=attrs['rotateY'])
                cmds.setKeyframe(control, time=time, attribute='rotateZ', value=attrs['rotateZ'])

    print(f'Animation data imported from {file_path}')

####################################################### Example usage ##########################################################
# Example usage
# import_animation_from_json(path)
####################################################### Example usage ##########################################################
