import inspect
from collections import OrderedDict
from rig_2.component.subcomponent import lip_sub
import importlib
importlib.reload(lip_sub)

from rig.rigComponents import elements 
from rig_2.component import base
importlib.reload(base) 

from rig_2.component import utils as component_utils
importlib.reload(component_utils) 



class Lip(base.Component):
    def __init__(self,
                #  class_name=None, # Will be set by "self.get_relative_path". This really only becomes important when you are doing a dynamic build from within maya 
                 component_name="lip",
                 lip_guide_class=None, 
                 geo_asset_class=None,
                 tierCount1=1,
                 tierCount2=3,
                 tierCount3=5,
                 upper_remove_point_indicies=[],
                 lower_remove_point_indicies=[],
                 upper_lip_name="upLip",
                 lower_lip_name="lowLip",
                 control_rivet_mesh=None,
                 order_before_deformer = "",
                 slidePatch = "",
                 slidePatchBase = "",
                 controlAutoOrientMesh = "",
                 projectionMeshUpper = "",
                 projectionMeshLower = "",
                 up_lip_volume_curve = "",
                 low_lip_volume_curve = "",
                 baseUpperCurve = "",
                 baseLowerCurve= "",
                 rollCurveNameUpper = "",
                 rollCurveNameLower = "",
                # self.deformMeshUpper="C_upperLip"
                # self.baseUpper="C_upperLipBase"
                # self.deformMeshLower="C_lowerLip"
                # self.baseLower="C_lowerLipBase"
                 deformMeshUpper="C_upperLip",
                 baseUpper="C_upperLipBase",
                 deformMeshLower="C_lowerLip",
                 baseLower="C_lowerLipBase",

                #  deformMeshUpper="jawMouth",
                #  baseUpper="jawMouthBase",
                #  deformMeshLower="jawMouth",
                #  baseLower="jawMouthBase",
                 **kw
                 ):
        super(Lip, self).__init__(component_name=component_name, **kw)
        # Creating a clean dictionary to avoid inheriting arguments from base.Component
        self.ordered_args = OrderedDict()
        # Getting args as the current locals at this point in parsing of the file
        self.frame = inspect.currentframe()
        self.get_args()
        
        # args
        self.lip_guide_class = lip_guide_class
        self.geo_asset_class = geo_asset_class
        self.tierCount1 = tierCount1
        self.tierCount2 = tierCount2
        self.tierCount3 = tierCount3
        self.upper_remove_point_indicies = upper_remove_point_indicies
        self.lower_remove_point_indicies = lower_remove_point_indicies
        self.upper_lip_name = upper_lip_name
        self.lower_lip_name = lower_lip_name
        self.order_before_deformer =order_before_deformer
        self.slidePatch =slidePatch
        self.slidePatchBase = slidePatchBase
        self.controlAutoOrientMesh = controlAutoOrientMesh
        self.projectionMeshUpper = projectionMeshUpper
        self.projectionMeshLower = projectionMeshLower
        self.up_lip_volume_curve = up_lip_volume_curve
        self.low_lip_volume_curve = low_lip_volume_curve
        self.baseUpperCurve = baseUpperCurve
        self.baseLowerCurve=baseLowerCurve
        self.rollCurveNameUpper = rollCurveNameUpper
        self.rollCurveNameLower = rollCurveNameLower
        
        self.deformMeshUpper=deformMeshUpper
        self.baseUpper=baseUpper
        self.deformMeshLower=deformMeshLower
        self.baseLower=baseLower
        
        # SUPER TEMP!!!!!!!
        # constant placeholders until get multiwrap geo_asset_class class worked out
        # self.deformMeshUpper="C_upperLip"
        # self.baseUpper="C_upperLipBase"
        # self.deformMeshLower="C_lowerLip"
        # self.baseLower="C_lowerLipBase"
        
        self.rivet_mesh_upper = control_rivet_mesh
        self.rivet_mesh_lower = control_rivet_mesh
        if not self.rivet_mesh_upper:
            self.rivet_mesh_upper = self.deformMeshUpper
        if not self.rivet_mesh_lower:
            self.rivet_mesh_lower = self.deformMeshLower
        self.input_anchor_nodes.append(self.control_parent)
 
    def unpack_args_from_guide_class(self):
        # If a lip guide class is given, fill automatically find the correct geometry to set up the lip rig
        if self.lip_guide_class:
            # In order for the volume lip curves to deforme in the correct way, while keeping the guides live, we need to reorder the deformers
            self.order_before_deformer = self.lip_guide_class.ffd_deformer
            
            self.slidePatch=self.lip_guide_class.slide_nurbs
            self.slidePatchBase=self.lip_guide_class.slide_nurbs_base
            
            # WILL LIKELY WANT TO CHANGE THIS LATER!!!! ADD ORIENT MESH TO GUIDES FOR 
            self.controlAutoOrientMesh =self.lip_guide_class.rivet_orient_patch

            
            self.projectionMeshUpper=self.lip_guide_class.upper_lip_projection
            self.projectionMeshLower=self.lip_guide_class.lower_lip_projection

            self.up_lip_volume_curve=self.lip_guide_class.up_lip_volume
            self.low_lip_volume_curve=self.lip_guide_class.low_lip_volume

            self.baseUpperCurve=self.lip_guide_class.up_lip_volume_base
            self.baseLowerCurve=self.lip_guide_class.low_lip_volume_base

            self.rollCurveNameUpper = self.lip_guide_class.up_lip_roll
            self.rollCurveNameLower =self.lip_guide_class.low_lip_roll
        

    def unpack_constants(self):

        self.slideCtrlSize1=1
        self.slideCtrlSize2=.7
        self.slideCtrlSize3=.4
        self.slideControlSpeedDefaults = [.1,.1,.1]

        self.ctrlAutoPositionThreshold = 0.6

        self.thickToPoint = (0, -0.97, 0.244)

        self.slideCtrlShapeOffset1=[0, 1.0, 0]
        self.slideCtrlShapeOffset2=[0, 1.0, 0]
        self.slideCtrlShapeOffset3=[0, 1.0, 0]

        self.slideCtrlPosOffset1=[0, 0.0, 0]
        self.slideCtrlPosOffset2=[0, 0.0, 0]
        self.slideCtrlPosOffset3=[0, 0.0, 0]

        self.thickCtrlSize1=.7
        self.thickCtrlSize2=.65
        self.thickCtrlSize3=.35

        self.thickCtrlShapeOffset1 = [ 0, -2, 3]
        self.thickCtrlShapeOffset2 = [0,-2.0,1]
        self.thickCtrlShapeOffset3 = [0,-2.0,1]

        self.falloffDefaults=(-10, -9.9, -3, 10.0)
        self.falloffMatrixDefaults=(-11, -7, -2, 10.0)

        self.matDefCtrlSize1=.5
        self.matDefCtrlSize2=.5
        self.matDefCtrlSize3=.5

        self.matDefCtrlShapeOffset1=[0,-1.0,1]
        self.matDefCtrlShapeOffset2=[0,-1.0,1]
        self.matDefCtrlShapeOffset3=[0,-1.0,1]

        #Uppers
        self.falloffDefaultsUpper=(10, -1, -7, -10.0)
        self.falloffMatrixDefaultsUpper=(10, -1, -9, -10.0)

        self.matDefCtrlShapeOffset1Upper=[0,1.0,1]
        self.matDefCtrlShapeOffset2Upper=[0,1.0,1]
        self.matDefCtrlShapeOffset3Upper=[0,1.0,1]

        self.thickToPointUpper = (0, 0.953, 0.303)

        self.thickCtrlShapeOffset1Upper=[0, 2.0, 3]
        self.thickCtrlShapeOffset2Upper=[0, 2.0, 1]
        self.thickCtrlShapeOffset3Upper=[0, 2.0, 1]

        self.thickFalloffCurveUpper = elements.UPPER_LIP_THICK_FALLOFF
        self.matDefFalloffCurve = elements.LOWER_LIP_MATDEF_FALLOFF

        self.matDefFalloffCurveUpper = elements.UPPER_LIP_MATDEF_FALLOFF
    
    def create_upper_lip(self):
        self.upperLipClass = lip_sub.Lip(name="upperLip",
                                         component_name=self.component_name,
                                         position_name="upper",
                                         ctrlName = "upperLip",
                                         controlRivetMesh = self.rivet_mesh_upper,
                                         upperLip=True,
                                         tierCount1=self.tierCount1,
                                         tierCount2=self.tierCount2,
                                         tierCount3=self.tierCount3,
                                         thickToPoint=self.thickToPointUpper,
                                         slideCtrlSize1=self.slideCtrlSize1,
                                         slideCtrlSize2=self.slideCtrlSize2,
                                         slideCtrlSize3=self.slideCtrlSize3,
                                         matDefCtrlSize1=self.matDefCtrlSize1,
                                         matDefCtrlSize2=self.matDefCtrlSize2,
                                         matDefCtrlSize3=self.matDefCtrlSize3,
                                         matDefFalloffCurve = self.matDefFalloffCurveUpper,

                                         slideCtrlShapeOffset1=self.slideCtrlShapeOffset1,
                                         slideCtrlShapeOffset2=self.slideCtrlShapeOffset2,
                                         slideCtrlShapeOffset3=self.slideCtrlShapeOffset3,

                                         slideCtrlPosOffset1=self.slideCtrlPosOffset1,
                                         slideCtrlPosOffset2=self.slideCtrlPosOffset2,
                                         slideCtrlPosOffset3=self.slideCtrlPosOffset3,

                                         slideControlSpeedDefaults=self.slideControlSpeedDefaults,

                                         thickCtrlSize1=self.thickCtrlSize1,
                                         thickCtrlSize2=self.thickCtrlSize2,
                                         thickCtrlSize3=self.thickCtrlSize3,

                                         thickCtrlShapeOffset1=self.thickCtrlShapeOffset1Upper,
                                         thickCtrlShapeOffset2=self.thickCtrlShapeOffset2Upper,
                                         thickCtrlShapeOffset3=self.thickCtrlShapeOffset3Upper,
                                         thickFalloffCurve=self.thickFalloffCurveUpper,

                                         matDefCtrlShapeOffset1=self.matDefCtrlShapeOffset1Upper,
                                         matDefCtrlShapeOffset2=self.matDefCtrlShapeOffset2Upper,
                                         matDefCtrlShapeOffset3=self.matDefCtrlShapeOffset3Upper,

                                         rollCurveName = self.rollCurveNameUpper,
                                         rollFalloffCurve = elements.UPPER_LIP_ROLL_FALLOFF,

                                         ctrlAutoPositionThreshold = self.ctrlAutoPositionThreshold,

                                         falloffDefaults=self.falloffDefaultsUpper,
                                         falloffMatrixDefaults=self.falloffMatrixDefaultsUpper,
                                         fileName=None,
                                         deformMesh=self.deformMeshUpper,
                                         base=self.baseUpper,
                                         controlAutoOrientMesh = self.controlAutoOrientMesh,
                                         projectionMesh=self.projectionMeshUpper,
                                         slidePatch=self.slidePatch,
                                         slidePatchBase=self.slidePatchBase)
                    
        self.upperLipClass.create()
        self.upperLipSlide, self.upperLipThick = self.upperLipClass.slide_deformer, self.upperLipClass.vector_deformer
        self.upperLipCurveClass = lip_sub.Lip(name="upperLipCurve",
                                              component_name=self.component_name,
                                              ctrlName = "upperLip",
                                                position_name="upper",
                                              order_before_deformer=self.order_before_deformer,

                                              upperLip=True,
                                              doLipThick = False,
                                              doLipRoll = False,
                                              #fileName=fileName,
                                              controlRivetMesh = self.rivet_mesh_upper,
                                              multiSlideForBaseCurve=False,
                                              repositionRivetCtrls=True,
                                              tierCount1=self.tierCount1,
                                              tierCount2=self.tierCount2,
                                              tierCount3=self.tierCount3,

                                              slideCtrlSize1=self.slideCtrlSize1,
                                              slideCtrlSize2=self.slideCtrlSize2,
                                              slideCtrlSize3=self.slideCtrlSize3,
                                              matDefCtrlSize1=self.matDefCtrlSize1,
                                              matDefCtrlSize2=self.matDefCtrlSize2,
                                              matDefCtrlSize3=self.matDefCtrlSize3,

                                              slideCtrlShapeOffset1=self.slideCtrlShapeOffset1,
                                              slideCtrlShapeOffset2=self.slideCtrlShapeOffset2,
                                              slideCtrlShapeOffset3=self.slideCtrlShapeOffset3,

                                              slideCtrlPosOffset1=self.slideCtrlPosOffset1,
                                              slideCtrlPosOffset2=self.slideCtrlPosOffset2,
                                              slideCtrlPosOffset3=self.slideCtrlPosOffset3,

                                              slideControlSpeedDefaults=self.slideControlSpeedDefaults,

                                              matDefCtrlShapeOffset1=self.matDefCtrlShapeOffset1Upper,
                                              matDefCtrlShapeOffset2=self.matDefCtrlShapeOffset2Upper,
                                              matDefCtrlShapeOffset3=self.matDefCtrlShapeOffset3Upper,

                                              ctrlAutoPositionThreshold = self.ctrlAutoPositionThreshold,

                                              falloffDefaults=self.falloffDefaultsUpper,
                                              falloffMatrixDefaults=self.falloffMatrixDefaultsUpper,
                                              fileName=None,
                                              deformMesh=self.up_lip_volume_curve,
                                              base=self.baseUpperCurve,
                                              projectionMesh=self.projectionMeshUpper,
                                              controlAutoOrientMesh = self.controlAutoOrientMesh,
                                              slidePatch=self.slidePatch,
                                              slidePatchBase=self.slidePatchBase)
        self.upperLipCurveClass.create()

        
        

        self.upper_lip_volume_blend = lip_sub.lipCurveDeformSplit(name="C_UpperLipWire",
                                                                  curve=self.up_lip_volume_curve,
                                                                  deformedGeometry=self.deformMeshUpper,
                                                                  projectionPatch=self.projectionMeshUpper,
                                                                  deformedGeometryBase=self.baseUpper,
                                                                  addWeightStack=[self.upperLipClass.slide_weight_stack.node,
                                                                              self.upperLipClass.slide_weight_stack.node_LR],
                                                                  addAtIndex=self.tierCount1 + self.tierCount2 + self.tierCount3,
                                                                  handPaint=False,
                                                                  upperLip=True,
                                                                  removePointIndicies=self.upper_remove_point_indicies,
                                                                  reorderInFrontOfDeformer=self.upperLipSlide,
                                                                  falloffDefaults = "",
                                                                  curve_base=self.baseUpperCurve,
                                                                  component_name = self.component_name)
    def create_lower_lip(self):


        self.lowerLipClass = lip_sub.Lip(name="lowerLip",
                                         component_name=self.component_name,
                                        controlRivetMesh = self.rivet_mesh_lower,
                                        position_name="lower",

                                         upperLip=False,
                                         tierCount1=self.tierCount1,
                                         tierCount2=self.tierCount2,
                                         tierCount3=self.tierCount3,
                                         thickToPoint=self.thickToPoint,
                                         slideCtrlSize1=self.slideCtrlSize1,
                                         slideCtrlSize2=self.slideCtrlSize2,
                                         slideCtrlSize3=self.slideCtrlSize3,

                                         matDefCtrlSize1=self.matDefCtrlSize1,
                                         matDefCtrlSize2=self.matDefCtrlSize2,
                                         matDefCtrlSize3=self.matDefCtrlSize3,
                                         matDefFalloffCurve = self.matDefFalloffCurve,
                                         rollCurveName = self.rollCurveNameLower,

                                         rollFalloffCurve = elements.LOWER_LIP_ROLL_FALLOFF,


                                         slideCtrlShapeOffset1=self.slideCtrlShapeOffset1,
                                         slideCtrlShapeOffset2=self.slideCtrlShapeOffset2,
                                         slideCtrlShapeOffset3=self.slideCtrlShapeOffset3,

                                         slideCtrlPosOffset1=self.slideCtrlPosOffset1,
                                         slideCtrlPosOffset2=self.slideCtrlPosOffset2,
                                         slideCtrlPosOffset3=self.slideCtrlPosOffset3,

                                         slideControlSpeedDefaults=self.slideControlSpeedDefaults,

                                         matDefCtrlShapeOffset1=self.matDefCtrlShapeOffset1,
                                         matDefCtrlShapeOffset2=self.matDefCtrlShapeOffset2,
                                         matDefCtrlShapeOffset3=self.matDefCtrlShapeOffset3,

                                         ctrlAutoPositionThreshold = self.ctrlAutoPositionThreshold,

                                         thickCtrlSize1=self.thickCtrlSize1,
                                         thickCtrlSize2=self.thickCtrlSize2,
                                         thickCtrlSize3=self.thickCtrlSize3,


                                         thickCtrlShapeOffset1=self.thickCtrlShapeOffset1,
                                         thickCtrlShapeOffset2=self.thickCtrlShapeOffset2,
                                         thickCtrlShapeOffset3=self.thickCtrlShapeOffset3,

                                         falloffDefaults=self.falloffDefaults,
                                         falloffMatrixDefaults=self.falloffMatrixDefaults,
                                         fileName=None,
                                         deformMesh=self.deformMeshLower,
                                         controlAutoOrientMesh = self.controlAutoOrientMesh,
                                         base=self.baseLower,
                                         projectionMesh=self.projectionMeshLower,
                                         slidePatch=self.slidePatch,
                                         slidePatchBase=self.slidePatchBase)
        self.lowerLipClass.create()
        self.lowerLipSlide, self.lowerLipThick = self.lowerLipClass.slide_deformer, self.lowerLipClass.vector_deformer
        self.lowerLipCurveClass = lip_sub.Lip(name="lowerLipCurve",
                                              component_name=self.component_name,
                                              ctrlName = "lowerLip",
                                              position_name="lower",

                                              order_before_deformer=self.order_before_deformer,
                                              controlRivetMesh = self.rivet_mesh_lower,
                                              doLipThick = False,
                                              doLipRoll = False,
                                              upperLip=False,
                                              # multiSlideForBaseCurve=False,
                                              multiSlideForBaseCurve=False,
                                              # repositionRivetCtrls=True,
                                              repositionRivetCtrls=True,
                                              tierCount1=self.tierCount1,
                                              tierCount2=self.tierCount2,
                                              tierCount3=self.tierCount3,

                                              slideCtrlSize1=self.slideCtrlSize1,
                                              slideCtrlSize2=self.slideCtrlSize2,
                                              slideCtrlSize3=self.slideCtrlSize3,
                                              matDefCtrlSize1=self.matDefCtrlSize1,
                                              matDefCtrlSize2=self.matDefCtrlSize2,
                                              matDefCtrlSize3=self.matDefCtrlSize3,

                                              slideCtrlShapeOffset1=self.slideCtrlShapeOffset1,
                                              slideCtrlShapeOffset2=self.slideCtrlShapeOffset2,
                                              slideCtrlShapeOffset3=self.slideCtrlShapeOffset3,

                                              slideCtrlPosOffset1=self.slideCtrlPosOffset1,
                                              slideCtrlPosOffset2=self.slideCtrlPosOffset2,
                                              slideCtrlPosOffset3=self.slideCtrlPosOffset3,

                                              slideControlSpeedDefaults=self.slideControlSpeedDefaults,

                                              matDefCtrlShapeOffset1=self.matDefCtrlShapeOffset1,
                                              matDefCtrlShapeOffset2=self.matDefCtrlShapeOffset2,
                                              matDefCtrlShapeOffset3=self.matDefCtrlShapeOffset3,

                                              ctrlAutoPositionThreshold = self.ctrlAutoPositionThreshold,

                                              falloffDefaults=self.falloffDefaults,
                                              falloffMatrixDefaults=self.falloffMatrixDefaults,
                                              fileName=None,
                                              deformMesh=self.low_lip_volume_curve,
                                              base=self.baseLowerCurve,
                                              controlAutoOrientMesh = self.controlAutoOrientMesh,
                                              # deformMesh=lowerCurve,
                                              # base="lowerLipCurveBase",
                                              projectionMesh=self.projectionMeshLower,
                                              slidePatch=self.slidePatch,
                                              slidePatchBase=self.slidePatchBase)

        self.lowerLipCurveClass.create()


        self.lower_lip_volume_blend = lip_sub.lipCurveDeformSplit(name="C_LowerLipWire",
                                                                  curve=self.low_lip_volume_curve,
                                                                  deformedGeometry=self.deformMeshLower,
                                                                  projectionPatch=self.projectionMeshLower,
                                                                  deformedGeometryBase=self.baseLower,
                                                                  addWeightStack=[self.lowerLipClass.slide_weight_stack.node,
                                                                              self.lowerLipClass.slide_weight_stack.node_LR],
                                                                  addAtIndex=self.tierCount1 + self.tierCount2 + self.tierCount3,
                                                                  handPaint=False,
                                                                  upperLip=False,
                                                                  reorderInFrontOfDeformer=self.lowerLipSlide,
                                                                  removePointIndicies=self.lower_remove_point_indicies,
                                                                  falloffDefaults = "",
                                                                  curve_base=self.baseLowerCurve,
                                                                  component_name = self.component_name)
        
        
    def reposition_controls_by_weights(self):
        component_utils.autoposition_weight_stack_controls(self.lowerLipCurveClass.slide_weight_stack.node, project_to_curve=self.low_lip_volume_curve)
        component_utils.autoposition_weight_stack_controls(self.upperLipCurveClass.slide_weight_stack.node, project_to_curve=self.up_lip_volume_curve)

        

    def create(self):
        super(Lip, self).create()
        self.unpack_args_from_guide_class()
        self.unpack_constants()
        self.create_upper_lip()  
        self.create_lower_lip()
        self.reposition_controls_by_weights()


