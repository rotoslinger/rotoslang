import inspect
from collections import OrderedDict
from maya import cmds
import sys
from rig_2.component.subcomponent import weightStack
import importlib
importlib.reload(weightStack)
from rig.deformers import matrixDeformer
importlib.reload(matrixDeformer)
from rig.deformers import slideSimple
importlib.reload(slideSimple)
from rig.deformers import blendshapeSimple
importlib.reload(blendshapeSimple)
from rig.deformers import vectorDeformerSimple
importlib.reload(vectorDeformerSimple)
from rig.deformers import curveRollSimple
importlib.reload(curveRollSimple)
from rig.deformers import utils as deformer_utils
importlib.reload(deformer_utils)
from rig.utils import misc
importlib.reload(misc)
from rig.utils import LHCurveDeformerCmds
importlib.reload(LHCurveDeformerCmds)
from rig.rigComponents import meshRivetCtrl 
importlib.reload(meshRivetCtrl)
from rig.rigComponents import elements
importlib.reload(elements)
from decorators import initialize
importlib.reload(elements)
from rig.utils import lhExport
importlib.reload(lhExport)
from rig_2.manipulator import elements as manipulator_elements
from rig_2.component import base
from rig.rigComponents import mouthJaw
importlib.reload(base)

from rig_2.animcurve import utils as animcurve_utils
importlib.reload(animcurve_utils) 

from rig_2.node import utils as node_utils
importlib.reload(node_utils)

from rig_2.component import utils as component_utils
importlib.reload(component_utils)
from rig_2.component.subcomponent import brow_sub
importlib.reload(brow_sub)


# The face is a master class that will control and wire up all of the face components.
class Brow(base.Component):
    def __init__(self,
                 component_name="brow",
                 guide_class=None,
                 tierCounts=[1,3,11],
                 nameBrows="Brow",
                 ctrlName = "brow",  # this will be used as a way to reuse controls between different components and deformers
                 deform_mesh="C_brow_GEO",
                 base_deform_mesh = "C_browBase_GEO",
                 control_rivet_mesh = "C_bodyBind_GEO",
                 ctrlAutoPositionThreshold = .001,
                 brow_hair_mesh="C_browHair_GEO",
                 curve_deformer_algorithm = 1,
                 **kw
                 ):
        super(Brow, self).__init__(component_name=component_name, **kw)
        self.ordered_args = OrderedDict()
        # Getting args as the current locals at this point in parsing of the file
        self.frame = inspect.currentframe()
        self.get_args()
        
        self.component_name=component_name
        self.guide_class=guide_class
        self.tierCounts=tierCounts
        self.nameBrows=nameBrows
        self.ctrlName = ctrlName
        self.deform_mesh=deform_mesh
        self.base_deform_mesh =base_deform_mesh
        self.control_rivet_mesh = control_rivet_mesh
        self.ctrlAutoPositionThreshold = ctrlAutoPositionThreshold
        self.brow_hair_mesh = brow_hair_mesh
        self.curve_deformer_algorithm = curve_deformer_algorithm
        
        
    def unpack_args_from_guide(self):
        # TODO need geo class to get geometry args from!!!
        # For Example, it would look something like this:
        # if self.model_class:
            # self.leftBrowMesh = self.model_class.leftBrowMesh
            # self.leftBrowBaseMesh = self.model_class.leftBrowBaseMesh
            # self.rightBrowMesh =  self.model_class.rightBrowMesh
            # self.rightBrowBaseMesh = self.model_class.rightBrowBaseMesh
        if self.guide_class:
            # In order for the volume lip curves to deforme in the correct way, while keeping the guides live, we need to reorder the deformers
            # find args from the guide class:
            self.slidePatch = self.guide_class.slide_nurbs
            self.slidePatchBase = self.guide_class.slide_nurbs_base
            self.L_projectionMesh=self.guide_class.l_projection_mesh
            self.R_projectionMesh=self.guide_class.r_projection_mesh
            self.C_projectionMesh=self.guide_class.c_projection_mesh
            self.rivet_orient_patch = self.guide_class.rivet_orient_patch
            self.l_brow_fit_curve = self.guide_class.l_curve
            self.r_brow_fit_curve = self.guide_class.r_curve
            self.c_brow_fit_curve = self.guide_class.c_curve
            self.c_brow_fit_curve_aim = self.guide_class.c_curve_aim
            self.l_brow_fit_curve_base = self.guide_class.l_curve_base
            self.r_brow_fit_curve_base = self.guide_class.r_curve_base
            self.c_brow_fit_curve_base = self.guide_class.c_curve_base
            self.c_brow_fit_curve_aim_base = self.guide_class.c_curve_aim_base
            self.brow_curves = {
                                "L":self.l_brow_fit_curve,
                                "R":self.r_brow_fit_curve,
                                "C":self.c_brow_fit_curve,
                                }
            

    def build_brow(self):
        # Wires up the face_input to the input_driver
        self.brow_class = brow_sub.Unibrow(guide_class=self.guide_class,
                                      nameBrows=self.nameBrows,
                                      component_name=self.component_name,
                                      tierCounts=self.tierCounts,
                                      control_rivet_mesh=self.control_rivet_mesh,
                                      ctrlAutoPositionThreshold=self.ctrlAutoPositionThreshold,
                                      deform_mesh=self.deform_mesh,
                                      base_deform_mesh=self.base_deform_mesh,
                                      # VERY IMPORTANT that this is the same between the brow and the fit brow so controls can be reused!!!!
                                      ctrlName=self.ctrlName,
                                      )
        self.brow_class.create()
        self.brow_fit_class = brow_sub.Unibrow(guide_class=self.guide_class,
                                          nameBrows=self.nameBrows + "Curve",
                                          component_name=self.component_name,
                                          tierCounts=self.tierCounts,
                                          control_rivet_mesh=self.control_rivet_mesh,
                                          ctrlAutoPositionThreshold=self.ctrlAutoPositionThreshold,
                                          ctrlName=self.ctrlName,
                                          fit_curve=True,)
        self.brow_fit_class.create()
        self.brow_aim_class = brow_sub.Unibrow(guide_class=self.guide_class,
                                          nameBrows=self.nameBrows + "CurveAim",
                                          component_name=self.component_name,
                                          tierCounts=self.tierCounts,
                                          control_rivet_mesh=self.control_rivet_mesh,
                                          ctrlAutoPositionThreshold=self.ctrlAutoPositionThreshold,
                                          ctrlName=self.ctrlName,
                                            deform_mesh=self.c_brow_fit_curve_aim,
                                            base_deform_mesh=self.c_brow_fit_curve_aim_base,
                                            reorder=True
                                          )
        self.brow_aim_class.create()
        
    def build_brow_hair_curve_deform(self):
        if self.brow_hair_mesh:
            if self.curve_deformer_algorithm == 0:
                # curve deform brow
                self.wire = cmds.wire(self.brow_hair_mesh, wire=self.c_brow_fit_curve, dds=[(0),(100000)] , name=self.nameBrows + "WireDeformer")[0]
                curve_base = misc.getShape(self.c_brow_fit_curve_base)
                cmds.connectAttr(self.c_brow_fit_curve_base + ".worldSpace[0]", self.wire + ".baseWire[0]", f=True)
            if self.curve_deformer_algorithm == 1:
                self.wire = LHCurveDeformerCmds.curveDeformerCmd( driverCurve = self.c_brow_fit_curve,
                                                                  aimCurve=self.c_brow_fit_curve_aim,
                                                                  driverCurveBase=self.c_brow_fit_curve_base,
                                                                  aimCurveBase=self.c_brow_fit_curve_aim_base,
                                                                  geom=[self.brow_hair_mesh],
                                                                  ihi=1,
                                                                  lockAttrs=0,
                                                                  side='C',
                                                                  name=self.nameBrows + "CurveDeformer").returnDeformer
        # # Split Brow

    def do_overrides(self):
                
        for i in range(3):
            weightcurve = self.brow_class.weight_curve_by_tier[1][i]
            if "L_" in weightcurve:
                animcurve_utils.setAnimCurveShape(weightcurve, elements.L_BROW_SECONDARY_ANIM_CURVE)
            if "R_" in weightcurve:
                animcurve_utils.setAnimCurveShape(weightcurve, elements.R_BROW_SECONDARY_ANIM_CURVE)
            # if "C_" in weightcurve:
            #     animcurve_utils.setAnimCurveShape(weightcurve, elements.C_BROW_SECONDARY_ANIM_CURVE)




    def create(self):
        super(Brow, self).create()
        self.unpack_args_from_guide()
        self.build_brow()
        self.build_brow_hair_curve_deform()
        self.do_overrides()
        
    

