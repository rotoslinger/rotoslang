import inspect
from maya import cmds
from collections import OrderedDict
from rig.rigComponents import elements 
from rig_2.component import base
from rig_2.node import utils as node_utils
from rig_2.tag import utils as tag_utils
from rig.deformers import matrixDeformer 
from rig.utils import misc 
import importlib

importlib.reload(base) 

# Must be built after the MouthJaw, as it will use the matrices created by this class
class TeethTongue(base.Component):
    def __init__(self,
                 component_name="teeth",
                 # These names need to be the same as in the mouthJaw and in the same order             
                 mat_def_attrs = ["C_jaw",
                                  "C_jawSecondary"],
                 jaw_frame_geo = "jawFrame_EX",
                 upper_teeth_geo = "C_upperTeeth_DEFORM",
                 lower_teeth_geo = "C_lowerTeeth_DEFORM",
                 tongue_geo = "C_tongue_DEFORM",
                 
                 **kw
                 ):
        super(TeethTongue, self).__init__(component_name=component_name, **kw)
        self.ordered_args = OrderedDict()
        # Getting args as the current locals at this point in parsing of the file
        self.frame = inspect.currentframe()
        self.get_args()
        
        self.jaw_frame_geo = jaw_frame_geo
        self.mat_def_attrs = mat_def_attrs
        self.upper_teeth_geo = upper_teeth_geo
        self.lower_teeth_geo = lower_teeth_geo
        self.tongue_geo = tongue_geo
        
    def create_teeth_anchor_deformers(self):
        rotLocatorNames = [x + "Rot" for x in self.mat_def_attrs]
        transLocatorNames = [x + "Trans" for x in self.mat_def_attrs]
        
        self.mat_def_translate = matrixDeformer.MatrixDeformer(name=self.component_name + "Translate_MatrixDef",
                                                               geoToDeform=self.jaw_frame_geo,
                                                               doCreateCtrls=False,
                                                               manualLocatorNames = transLocatorNames,
                                                               manual_weights=True,
                                                               centerToParent=True,
                                                               addAtIndex=0,
                                                               numToAdd=False,
                                                               reverseDeformerOrder = True,
                                                               controlParent = self.control_parent,
                                                               rigParent = self.rig,
                                                               hide = True,
                                                               connectTranslate = True,
                                                               connectRotate = False,
                                                               connectScale = False,
                                                               component_name=self.component_name
                                                               )
        self.mat_def_translate.create()
        
        self.mat_def_translate = matrixDeformer.MatrixDeformer(name=self.component_name + "Rotate_MatrixDef",
                                                               geoToDeform=self.jaw_frame_geo,
                                                               doCreateCtrls=False,
                                                               manualLocatorNames = rotLocatorNames,
                                                               manual_weights=True,
                                                               centerToParent=True,
                                                               addAtIndex=0,
                                                               numToAdd=False,
                                                               reverseDeformerOrder = True,
                                                               controlParent = self.control_parent,
                                                               rigParent = self.rig,
                                                               hide = True,
                                                               connectTranslate = False,
                                                               connectRotate = True,
                                                               connectScale = False,
                                                               component_name=self.component_name
                                                               )
        self.mat_def_translate.create()

    def create_geo_constraint(self):
        self.teeth_anchor = node_utils.get_locator(name=self.component_name + "Anchor", parent=self.output)
        self.component_membership_nodes.append(self.teeth_anchor)
        tag_utils.tag_rivet_mesh(self.jaw_frame_geo)
        self.geoConstraint = misc.geoConstraint(driverMesh = self.jaw_frame_geo, driven = self.teeth_anchor, parent = self.rig,
                                                name = "{0}_GCS".format(self.component_name),
                                                translate=True,
                                                rotate=True,
                                                scale=False,
                                                maintainOffsetT=False, 
                                                maintainOffsetR=False,
                                                maintainOffsetS=True,)
        self.component_membership_nodes.append(self.geoConstraint)

    def rig_teeth_tongue(self):
        # Temporary geo based rig for lower teeth and tongue.
        # This will need to be replaced with a more complex system for shaping the teeth and tongue
        self.cluster_deformers = []
        self.cluster_handles = []
        for geo in [self.lower_teeth_geo, self.tongue_geo]:
            deformer, handle = cmds.cluster(geo, name=geo + "_Cluster" )
            cmds.parent(handle, self.rig)
            cmds.setAttr(handle + ".v", 0)
            self.cluster_deformers.append(deformer)
            self.cluster_handles.append(handle)
            cmds.parentConstraint(self.teeth_anchor, handle, mo=True)
            

        
    def create(self):
        super(TeethTongue, self).create()
        self.create_teeth_anchor_deformers()
        self.create_geo_constraint()
        self.rig_teeth_tongue()
    
