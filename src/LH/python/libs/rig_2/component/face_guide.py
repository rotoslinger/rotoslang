import inspect
from collections import OrderedDict

from maya import cmds

from rig_2.component import utils as component_utils
from rig_2.tag import utils as tag_utils

from rig_2.component import base as component_base

from rig_2 import decorator
from rig_2.mirror import utils as mirror_utils
from rig_2.shape import mesh, nurbscurve
from rig_2.elements import face_guide_elements
import importlib

importlib.reload(tag_utils)
importlib.reload(component_base)
importlib.reload(decorator)
importlib.reload(mesh)
importlib.reload(nurbscurve)
importlib.reload(face_guide_elements)
importlib.reload(component_utils)



class Base(component_base.Component):
    def __init__(self,
                #  class_name="rig_2.guide.face.Base", # Will be set by "self.get_relative_path". This really only becomes important when you are doing a dynamic build from within maya 
                 side="C",
                 component_name="base",
                 num_local_influence=9,
                 s_divisions=9,
                 t_divisions=9,
                 projection_x_subdivisions=10,
                 projection_y_subdivisions=5,
                 slide_x_subdivisions=10,
                 slide_y_subdivisions=6,
                 slide_patch_x_overshoot=0,
                 slide_patch_y_overshoot=0,
                 hide_reference_geo=True,
                 debug=False,
                 is_guide_class=True,
                 input_driver="",
                 guide_geo_export_override=True,
                 **kw
                 ):
        super(Base, self).__init__(
                                   side=side,
                                   component_name=component_name, is_guide_class=is_guide_class, input_driver=input_driver, **kw)
        # Creating a clean dictionary to avoid inheriting arguments from base.Component
        self.ordered_args = OrderedDict()
        # Getting args as the current locals at this point in parsing of the file
        self.frame = inspect.currentframe()
        self.get_args()

        self.aim_surface=None
        # args
        self.s_divisions = s_divisions
        self.t_divisions = t_divisions
        self.num_local_influence = num_local_influence
        self.projection_x_subdivisions = projection_x_subdivisions
        self.projection_y_subdivisions = projection_y_subdivisions
        self.slide_x_subdivisions = slide_x_subdivisions
        self.slide_y_subdivisions = slide_y_subdivisions
        self.slide_patch_x_overshoot = slide_patch_x_overshoot
        self.slide_patch_y_overshoot = slide_patch_y_overshoot
        self.hide_reference_geo = hide_reference_geo
        self.debug = debug
        self.guide_geo_export_override = guide_geo_export_override

        # vars
        self.mesh_projection_x_overrides = []
        self.base_names=[]
        self.geo_to_be_base=[]
        
        self.l_geo_to_be_base=[]
        self.r_geo_to_be_base=[]
        
        self.lattice_geo = []
        self.l_lattice_geo = []
        self.r_lattice_geo = []
        self.lattice = None
        self.l_lattice = None
        self.r_lattice = None
        self.guide_geo = []
        self.slide_nurbs = ""
        self.l_slide_nurbs = ""
        self.r_slide_nurbs = ""
        self.rivet_orient_patch = ""
        self.l_rivet_orient_patch = ""
        self.r_rivet_orient_patch = ""
        self.input_anchor_nodes.append(self.input)

    def create_nurbs(self):
        return
    
    def create_geo(self):
        return
    
    def create_projection_meshes(self):
        return

    def create_base_geo(self):
        self.create_single_base_geo()
        self.create_mirror_base_geo()
        
    def create_single_base_geo(self):
        if not self.geo_to_be_base:
            return
        # Geometry should be named neatly, if it is not this will not work
        self.base_geo = self.create_base_geo_from_list(self.geo_to_be_base)
        self.lattice_geo += self.base_geo
    
    def create_mirror_base_geo(self):
        if not self.l_geo_to_be_base or not self.r_geo_to_be_base:
            return
        # Geometry should be named neatly, if it is not this will not work
        self.l_base_geo = self.create_base_geo_from_list(self.l_geo_to_be_base)
        self.l_lattice_geo += self.l_base_geo
    
        self.r_base_geo = self.create_base_geo_from_list(self.r_geo_to_be_base)
        self.r_lattice_geo += self.r_base_geo
    
    def create_base_geo_from_list(self, geo_list):
        return_list = []
    
        for geo in geo_list:
            geo_name = geo + "BASE"
            if not cmds.objExists(geo_name):
                cmds.duplicate(geo, n=geo_name)
                cmds.setAttr(geo_name + ".v", 0)
            tag_utils.tag_base_geo(geo_name)
            self.guide_geo.append(geo_name)
            return_list.append(geo_name)
        self.component_membership_nodes += return_list
        return return_list

    def create_base(self, node):
        node_name = node + "BASE"
        if not cmds.objExists(node_name):
            cmds.duplicate(node, n=node_name)
            cmds.setAttr(node_name + ".v", 0)
        tag_utils.tag_base_geo(node_name)
        self.component_membership_nodes += [node_name]
        return node_name
    
    def create_rivet_normal_patch(self, node, side=""):
        node_name = side + self.component_name + "_RivetOrientPatch"
        if not cmds.objExists(node_name):
            cmds.duplicate(node, n=node_name)
            # This patch will be driven by the face rig, so it needs to be constrained.  Also, don't forget to bake out guides...
            cmds.parent(node_name, self.input)
        self.guide_geo.append(node_name)
        tag_utils.tag_rivet_orient_patch(node_name)
        tag_utils.tag_guide_cacheable(node_name)
        self.component_membership_nodes += [node_name]
        if not side:
            self.lattice_geo += [node_name]
        if side=="L_":
            self.l_lattice_geo += [node_name]
        if side=="R_":
            self.r_lattice_geo += [node_name]
        return node_name

    def create_all_rivet_orient_patches(self):
        if self.slide_nurbs:
            self.rivet_orient_patch = self.create_rivet_normal_patch(self.slide_nurbs)
            
        if self.l_slide_nurbs:
            self.l_rivet_orient_patch = self.create_rivet_normal_patch(self.l_slide_nurbs, side="L_")
            
        if self.r_slide_nurbs:
            self.r_rivet_orient_patch = self.create_rivet_normal_patch(self.r_slide_nurbs, side="R_")


    def create_lattice(self):
        self.create_single_lattice()
        self.create_mirrored_lattice()
        
    def create_single_lattice(self):
        if not self.lattice_geo:
            return
        self.ffd_deformer, self.lattice, self.lattice_base = self.create_lattice_by_side(geo=self.lattice_geo)

    def create_mirrored_lattice(self):
        if not self.l_lattice_geo or not self.r_lattice_geo:
            return
        self.l_ffd_deformer, self.l_lattice, self.l_lattice_base = self.create_lattice_by_side(side="L", geo=self.l_lattice_geo)
        self.r_ffd_deformer, self.r_lattice, self.r_lattice_base = self.create_lattice_by_side(side="R", geo=self.r_lattice_geo, flip=True)

    def create_lattice_by_side(self, side="C", geo=None, flip=False):
        x, y, z, center = component_utils.get_projection_dimensions(geo, z_at_origin=False)
        if flip:
            x = x*-1
        if cmds.objExists("{0}_{1}".format(side, self.component_name)):
            lattice = "{0}_{1}".format(side, self.component_name) + "Lattice"
            lattice_base = "{0}_{1}".format(side, self.component_name) + "Base"
            cmds.setAttr(self.lattice + ".v", 0)
            return

        ffd_deformer, lattice, lattice_base = cmds.lattice(geo,
                                                            n="{0}_{1}".format(side, self.component_name),
                                                            outsideLattice=1,
                                                            ldivisions=(self.num_local_influence,
                                                                        self.num_local_influence,
                                                                        self.num_local_influence),
                                                            divisions=(self.s_divisions,
                                                                        self.t_divisions,
                                                                        2),
                                                        #   objectCentered=True,
                                                            )
        cmds.xform(lattice, ws=True, s=[x,y,z], t=center)
        cmds.xform(lattice_base, ws=True, s=[x,y,z], t=center)
        
        cmds.parent(lattice, lattice_base, self.geo)
        cmds.setAttr(lattice + ".v", 0)
        return ffd_deformer, lattice, lattice_base


    def create_lattice_controls(self):
        self.create_single_lattice_controls()
        self.create_mirrored_lattice_controls()

    def create_controls(self, lattice, side="C", is_symmetric=True, do_dynamic_connections=True):
        root_control, controls, clusters = component_utils.cluster_lattice_sheet(lattice_name=lattice,
                                                                                 s_count=self.s_divisions,
                                                                                 t_count=self.t_divisions,
                                                                                 control_parent=self.control_parent,
                                                                                 handle_parent=self.rig,
                                                                                 component_name=self.component_name,
                                                                                 side=side,
                                                                                 is_symmetric=is_symmetric,
                                                                                 do_dynamic_connections=do_dynamic_connections)
        if clusters and cmds.objExists(root_control):
            component_utils.safe_parent(clusters, root_control)
    
        return root_control, controls, clusters

    def create_mesh_projection_per_side(self, meshes_to_project, flip=False):
        temp_meshes = []
        for idx , mesh in enumerate(meshes_to_project):
            projection_mesh = component_utils.get_projection_geo(mesh, self.geo, self.projection_x_subdivisions, self.projection_y_subdivisions, flip=flip)
            tag_utils.tag_projection_mesh(projection_mesh)
            temp_meshes.append(projection_mesh)
        return temp_meshes

    def create_single_lattice_controls(self):
        if not self.lattice:
            return
        self.root_control, self.controls, self.clusters = self.create_controls(self.lattice)
        
    def create_mirrored_lattice_controls(self):
        if not self.l_lattice and not self.r_lattice:
            return
        
        self.l_root_control, self.l_controls, self.l_clusters = self.create_controls(self.l_lattice,
                                                                                     side="L",
                                                                                     is_symmetric=False,
                                                                                     do_dynamic_connections=False)
        self.r_root_control, self.r_controls, self.r_clusters = self.create_controls(self.r_lattice,
                                                                                     side="R",
                                                                                     is_symmetric=False,
                                                                                     do_dynamic_connections=False)
        mirror_utils.add_dynamic_mirror_connection(self.l_controls , hide_connected=False, scale=False)
        mirror_utils.add_dynamic_mirror_connection([self.l_root_control], hide_connected=False, scale=True)

    def create_guide_geo_tag(self):
        for node in self.guide_geo:
            tag_utils.tag_guide_geo(node)
            if self.guide_geo_export_override:
                tag_utils.tag_export_override(node)
                
    def create(self):
        super(Base, self).create()
        self.create_geo()
        self.create_projection_meshes()
        self.create_nurbs()
        self.create_base_geo()
        self.create_all_rivet_orient_patches()
        self.create_lattice()
        self.create_lattice_controls()
        self.create_guide_geo_tag()
        self.create_component_tag()



class Mouth_Guide(Base):
    def __init__(self,
                 side="C",
                 component_name="mouthGuide",
                 up_lip_complex=False,
                 low_lip_complex=False,
                 **kw
                 ):

        super(Mouth_Guide, self).__init__(
                                        side=side,
                                        component_name=component_name,
                                        **kw)
        # Add args to base class
        self.frame = inspect.currentframe()
        self.get_args()
        # args
        self.up_lip_complex = up_lip_complex
        self.low_lip_complex = low_lip_complex
        # vars
        self.upper_lip = None
        self.lower_lip = None
        self.mouth_jaw = None

        self.curves_list = []
        self.base_names=[]
        self.lattice_geo = []

        # overrides
        self.component_name="mouthGuide"
        self.mouth_jaw_component_name="mouthJaw"
        self.lips_component_name="lips"

    def create_geo(self):

        up_lip_dict = face_guide_elements.UP_LIP_SIMPLE
        if self.up_lip_complex:
            up_lip_dict = face_guide_elements.UP_LIP_COMPLEX
        low_lip_dict = face_guide_elements.LOW_LIP_SIMPLE
        if self.low_lip_complex:
            low_lip_dict = face_guide_elements.LOW_LIP_COMPLEX

        self.upper_lip = mesh.safe_create_mesh(up_lip_dict, parent=self.geo)
        self.lower_lip = mesh.safe_create_mesh(low_lip_dict, parent=self.geo)
        self.mouth_jaw = mesh.safe_create_mesh(face_guide_elements.MOUTH_JAW, parent=self.geo)

        for geo in [self.upper_lip, self.lower_lip, self.mouth_jaw]:
            tag_utils.tag_reference_geo(geo)

        # The slide mesh will be fit to the jaw
        self.slide_fit_to_mesh = self.mouth_jaw
        self.meshes_to_project= [self.upper_lip, self.lower_lip, self.mouth_jaw]

        self.create_curves()

        self.component_membership_nodes += [self.upper_lip, self.lower_lip, self.mouth_jaw]
                
        self.lattice_geo += [self.upper_lip, self.lower_lip, self.mouth_jaw]
        
        
        
    def create_curves(self):
        self.up_lip_volume, dummy = nurbscurve.safe_create_curve(face_guide_elements.UP_LIP_VOLUME,
                                                                 face_guide_elements.UP_LIP_VOLUME["name"],
                                                                 parent=self.geo,
                                                                 transform_suffix=None,
                                                                 shape_suffix=None

                                                                 )
        self.low_lip_volume, dummy = nurbscurve.safe_create_curve(face_guide_elements.LOW_LIP_VOLUME,
                                                                  face_guide_elements.LOW_LIP_VOLUME["name"],
                                                                  parent=self.geo,
                                                                  transform_suffix=None,
                                                                  shape_suffix=None
                                                                  )
        [tag_utils.tag_guide_curves(curve) for curve in [self.up_lip_volume, self.low_lip_volume]]


        self.up_lip_roll, dummy = nurbscurve.safe_create_curve(face_guide_elements.UP_LIP_ROLL,
                                                               face_guide_elements.UP_LIP_ROLL["name"],
                                                               parent=self.geo,
                                                               transform_suffix=None,
                                                               shape_suffix=None

                                                               )
        self.low_lip_roll, dummy = nurbscurve.safe_create_curve(face_guide_elements.LOW_LIP_ROLL,
                                                                face_guide_elements.LOW_LIP_ROLL["name"],
                                                                parent=self.geo,
                                                                transform_suffix=None,
                                                                shape_suffix=None
                                                                )
        [tag_utils.tag_guide_curves(curve) for curve in [self.up_lip_roll, self.low_lip_roll]]
        
        self.up_lip_volume_base = self.create_base(self.up_lip_volume)
        self.low_lip_volume_base = self.create_base(self.low_lip_volume)
        self.up_lip_roll_base = self.create_base(self.up_lip_roll)
        self.low_lip_roll_base = self.create_base(self.low_lip_roll)
        
        self.component_membership_nodes += [self.up_lip_volume, self.low_lip_volume,
                            self.up_lip_roll, self.low_lip_roll, self.up_lip_volume_base, self.low_lip_volume_base,
                            self.up_lip_roll_base, self.low_lip_roll_base]
                
        self.lattice_geo += [self.up_lip_volume, self.low_lip_volume,
                            self.up_lip_roll, self.low_lip_roll, self.up_lip_volume_base, self.low_lip_volume_base,
                            self.up_lip_roll_base, self.low_lip_roll_base]
        self.guide_geo +=[self.up_lip_volume, self.low_lip_volume,
                            self.up_lip_roll, self.low_lip_roll, self.up_lip_volume_base, self.low_lip_volume_base,
                            self.up_lip_roll_base, self.low_lip_roll_base]





    def create_projection_meshes(self):        
        self.meshes_to_project= [self.upper_lip, self.lower_lip, self.mouth_jaw]
        self.upper_lip_projection =  component_utils.get_projection_geo(self.upper_lip,
                                                                        self.geo,
                                                                        self.projection_x_subdivisions,
                                                                        self.projection_y_subdivisions,
                                                                        x_mult=.9)
        self.lower_lip_projection =  component_utils.get_projection_geo(self.lower_lip,
                                                                        self.geo,
                                                                        self.projection_x_subdivisions,
                                                                        self.projection_y_subdivisions,
                                                                        x_mult=.9)
        self.mouth_jaw_projection =  component_utils.get_projection_geo(self.mouth_jaw,
                                                                        self.geo,
                                                                        self.projection_x_subdivisions,
                                                                        self.projection_y_subdivisions,
                                                                        x_mult=1)
        self.lattice_geo += [self.upper_lip_projection, self.lower_lip_projection, self.mouth_jaw_projection]
        self.component_membership_nodes += [self.upper_lip_projection, self.lower_lip_projection, self.mouth_jaw_projection]
        self.guide_geo +=  [self.upper_lip_projection, self.lower_lip_projection, self.mouth_jaw_projection]
        
    def create_nurbs(self):
        self.slide_fit_to_mesh = self.mouth_jaw
        x, y, z, center = component_utils.get_projection_dimensions(self.slide_fit_to_mesh)
        slide_name= "C_{0}_SLDE".format(self.component_name)
        x += self.slide_patch_x_overshoot
        y += self.slide_patch_y_overshoot
        if cmds.objExists(slide_name):
            self.slide_nurbs = slide_name
        else:
            self.slide_nurbs = cmds.nurbsPlane(name=slide_name,
                                            ax=[0,0,1],
                                            width = x,
                                            lengthRatio=y/x,
                                            patchesU=self.slide_x_subdivisions,
                                            patchesV=self.slide_y_subdivisions)[0]
            tag_utils.tag_slide_geo(self.slide_nurbs)
            cmds.parent(self.slide_nurbs, self.geo)

            cmds.move(center[0], center[1], center[2], self.slide_nurbs)

        self.slide_nurbs_base = self.create_base(self.slide_nurbs)
        
        self.lattice_geo += [self.slide_nurbs, self.slide_nurbs_base]
        self.component_membership_nodes += [self.slide_nurbs, self.slide_nurbs_base]
        self.guide_geo +=  [self.slide_nurbs, self.slide_nurbs_base]

class Lid_Guide(Base):
    def __init__(self,
                 side="C",
                 component_name="lidGuide",
                 s_divisions=3,
                 t_divisions=3,
                 **kw
                 ):

        super(Lid_Guide, self).__init__(
                                        side=side,
                                        component_name=component_name,
                                        s_divisions=s_divisions,
                                        t_divisions=t_divisions,
                                        **kw)
        # Add args to base class
        class_name = self.get_relative_path()
        self.frame = inspect.currentframe()
        self.get_args()
        self.l_slide_nurbs = ""
        self.r_slide_nurbs = ""


    def create_geo(self):

        l_brow = mesh.safe_create_mesh(face_guide_elements.L_UP_LID_MESH, parent=self.geo)
        self.l_lower_lid = mesh.safe_create_mesh(face_guide_elements.L_LOW_LID_MESH, parent=self.geo)
        
        r_brow = mesh.safe_create_mesh(face_guide_elements.R_UP_LID_MESH, parent=self.geo)
        self.r_lower_lid = mesh.safe_create_mesh(face_guide_elements.R_LOW_LID_MESH, parent=self.geo)

    
        for geo in [l_brow, self.l_lower_lid, r_brow, self.r_lower_lid]:
            tag_utils.tag_reference_geo(geo)
        
        self.l_curves = []
        self.r_curves = []
        
        for curve_dict in [face_guide_elements.L_UP_LID_CRV, face_guide_elements.L_LOW_LID_CRV]:
            curve, dummy = nurbscurve.safe_create_curve(curve_dict,
                                                        curve_dict["name"],
                                                        parent=self.geo,
                                                        transform_suffix=None,
                                                        shape_suffix=None
                                                        )
            self.l_curves.append(curve)
            
        for curve_dict in [face_guide_elements.R_UP_LID_CRV, face_guide_elements.R_LOW_LID_CRV]:
            curve, dummy = nurbscurve.safe_create_curve(curve_dict,
                                                        curve_dict["name"],
                                                        parent=self.geo,
                                                        transform_suffix=None,
                                                        shape_suffix=None
                                                        )
            self.r_curves.append(curve)
            
        [tag_utils.tag_guide_curves(curve) for curve in self.l_curves + self.r_curves]


        # Prepare data to be used later for fitting
        self.slide_fit_meshes = [l_brow, self.l_lower_lid]
        self.r_slide_fit_meshes = [r_brow, self.r_lower_lid]
        
        self.l_meshes_to_project= self.slide_fit_meshes
        self.r_meshes_to_project= self.r_slide_fit_meshes

        self.l_lattice_geo = self.l_meshes_to_project + self.l_curves
        self.r_lattice_geo = self.r_meshes_to_project + self.r_curves
        
        self.component_membership_nodes += self.l_meshes_to_project + self.r_meshes_to_project + self.l_curves + self.r_curves
        
        self.l_geo_to_be_base += self.l_curves
        self.r_geo_to_be_base += self.r_curves
        self.guide_geo += self.l_curves + self.r_curves

    def create_projection_meshes(self):
        self.l_projection_meshes = self.create_mesh_projection_per_side(self.l_meshes_to_project)
        self.r_projection_meshes = self.create_mesh_projection_per_side(self.r_meshes_to_project, flip=True)
        self.l_lattice_geo += self.l_projection_meshes
        self.r_lattice_geo += self.r_projection_meshes
        
        self.component_membership_nodes += self.l_projection_meshes + self.r_projection_meshes
        self.guide_geo += self.l_projection_meshes + self.r_projection_meshes

    def create_nurbs(self):
        # return
        side_mesh_dict = {"L": self.slide_fit_meshes, "R": self.r_slide_fit_meshes}
        for side in ["L", "R"]:
            fit_meshes = side_mesh_dict[side]
        # for side, fit_meshes in itertools.product(["L", "R"], [self.slide_fit_meshes, self.r_slide_fit_meshes]):
            x, y, z, center = component_utils.get_projection_dimensions(fit_meshes)
            slide_name= "{0}_{1}_SLDE".format(side, self.component_name)
            x += self.slide_patch_x_overshoot
            y += self.slide_patch_y_overshoot
            if cmds.objExists(slide_name):
                slide_nurbs = slide_name
            else:
                slide_nurbs = cmds.nurbsPlane(name=slide_name,
                                                ax=[0,0,1],
                                                width = x,
                                                lengthRatio=y/x,
                                                patchesU=self.slide_x_subdivisions,
                                                patchesV=self.slide_y_subdivisions)[0]
                tag_utils.tag_slide_geo(slide_nurbs)
                cmds.parent(slide_nurbs, self.geo)

                cmds.move(center[0], center[1], center[2], slide_nurbs)
                
            cmds.DeleteHistory(slide_nurbs)
            cmds.makeIdentity(slide_nurbs, apply=True, t=1, r=1, s=1, n=0, pn=1)
    
            if side == "L":
                self.l_lattice_geo += [slide_nurbs]
                self.l_geo_to_be_base += [slide_nurbs]
                self.l_slide_nurbs = slide_nurbs

            else:
                self.r_lattice_geo += [slide_nurbs]
                self.r_geo_to_be_base += [slide_nurbs]
                self.r_slide_nurbs = slide_nurbs
                
        self.component_membership_nodes += [self.l_slide_nurbs, self.r_slide_nurbs]
        self.guide_geo += [self.l_slide_nurbs, self.r_slide_nurbs]

class Brow_Guide(Base):
    def __init__(self,
                 side="C",
                 component_name="browGuide",
                 s_divisions=7,
                 t_divisions=4,
                 **kw
                 ):

        super(Brow_Guide, self).__init__(
                                        side=side,
                                        component_name=component_name,
                                        s_divisions=s_divisions,
                                        t_divisions=t_divisions,
                                        **kw)
        # Add args to base class
        self.frame = inspect.currentframe()
        self.get_args()

    def create_geo(self):

        self.l_brow = mesh.safe_create_mesh(face_guide_elements.L_BROW_MESH, parent=self.geo)
        
        self.r_brow = mesh.safe_create_mesh(face_guide_elements.R_BROW_MESH, parent=self.geo)

    
        for geo in [self.l_brow, self.r_brow]:
            tag_utils.tag_reference_geo(geo)
        # [tag_utils.create_component_tag(curve, component_name=self.component_name) for curve in [self.up_lip_volume, self.low_lip_volume]]

        # The slide mesh will be fit to the jaw
        # self.mesh_projection_x_overrides = [.9, .9, 1]
        
        
        self.l_curve, dummy = nurbscurve.safe_create_curve(face_guide_elements.L_BROW_CRV,
                                                    face_guide_elements.L_BROW_CRV["name"],
                                                    parent=self.geo,
                                                    transform_suffix=None,
                                                    shape_suffix=None
                                                    )
        
        self.r_curve, dummy = nurbscurve.safe_create_curve(face_guide_elements.R_BROW_CRV,
                                                    face_guide_elements.R_BROW_CRV["name"],
                                                    parent=self.geo,
                                                    transform_suffix=None,
                                                    shape_suffix=None
                                                    )
        self.c_curve, dummy = nurbscurve.safe_create_curve(face_guide_elements.C_BROW_CRV,
                                                    face_guide_elements.C_BROW_CRV["name"],
                                                    parent=self.geo,
                                                    transform_suffix=None,
                                                    shape_suffix=None
                                                    )
        self.c_curve_aim, dummy = nurbscurve.safe_create_curve(face_guide_elements.C_BROW_AIM_CRV,
                                                    face_guide_elements.C_BROW_AIM_CRV["name"],
                                                    parent=self.geo,
                                                    transform_suffix=None,
                                                    shape_suffix=None
                                                    )
        self.l_curve_base = self.create_base(self.l_curve)
        self.r_curve_base = self.create_base(self.r_curve)
        self.c_curve_base = self.create_base(self.c_curve)
        self.c_curve_aim_base = self.create_base(self.c_curve_aim)

            
        [tag_utils.tag_guide_curves(curve) for curve in [self.l_curve,
                                                         self.r_curve,
                                                         self.c_curve,
                                                         self.c_curve_aim,
                                                         
                                                         self.l_curve_base,
                                                         self.r_curve_base,
                                                         self.c_curve_base,
                                                         self.c_curve_aim_base,
                                                         
                                                         ]]

        self.guide_geo += [self.l_curve,
                            self.r_curve,
                            self.c_curve,
                            self.c_curve_aim,
                            self.l_curve_base,
                            self.r_curve_base,
                            self.c_curve_base,
                            self.c_curve_aim_base,
                            ]

        # Prepare data to be used later for fitting
        self.slide_fit_meshes = [self.l_brow, self.r_brow]
        
        self.l_mesh_to_project= self.l_brow
        self.r_mesh_to_project= self.r_brow
        self.c_meshes_to_project= [self.l_brow, self.r_brow]

        self.lattice_geo =  [self.l_brow,
                             self.r_brow,
                             self.l_curve,
                             self.r_curve,
                             self.c_curve,
                             self.c_curve,
                             self.c_curve_aim,
                             self.l_curve_base,
                             self.r_curve_base,
                             self.c_curve_base,
                             self.c_curve_aim_base,
                             ]
        
        self.component_membership_nodes += [self.l_brow,
                                            self.r_brow,
                                            self.l_curve,
                                            self.r_curve,
                                            self.c_curve,
                                            self.c_curve_aim,

                                            self.l_curve_base,
                                            self.r_curve_base,
                                            self.c_curve_base,
                                            self.c_curve_aim_base,
                                            ]
        
        # self.geo_to_be_base += [self.l_curve, self.r_curve, self.c_curve]
        
    def create_projection_meshes(self):
        
        self.l_projection_mesh = component_utils.get_projection_geo(self.l_mesh_to_project,
                                                                    self.geo,
                                                                    self.projection_x_subdivisions,
                                                                    self.projection_y_subdivisions, )
        self.r_projection_mesh = component_utils.get_projection_geo(self.r_mesh_to_project,
                                                                    self.geo,
                                                                    self.projection_x_subdivisions,
                                                                    self.projection_y_subdivisions,
                                                                    flip=True)
        self.c_projection_mesh = component_utils.get_projection_geo([self.l_brow, self.r_brow],
                                                                    self.geo,
                                                                    self.projection_x_subdivisions,
                                                                    self.projection_y_subdivisions,
                                                                    flip=False,
                                                                    name="C_brow_PRJ")

        for mesh in [self.l_projection_mesh, self.r_projection_mesh, self.c_projection_mesh]:
            tag_utils.tag_projection_mesh(mesh)
        self.lattice_geo += [self.l_projection_mesh, self.r_projection_mesh, self.c_projection_mesh]
        self.component_membership_nodes += [self.l_projection_mesh, self.r_projection_mesh, self.c_projection_mesh]
        self.guide_geo += [self.l_projection_mesh, self.r_projection_mesh, self.c_projection_mesh]

    def create_nurbs(self):
        # return
        x, y, z, center = component_utils.get_projection_dimensions([self.l_mesh_to_project, self.r_mesh_to_project])
        slide_name= "C_{0}_SLDE".format(self.component_name)
        x += self.slide_patch_x_overshoot
        y += self.slide_patch_y_overshoot
        if cmds.objExists(slide_name):
            self.slide_nurbs = slide_name
        else:
            self.slide_nurbs = cmds.nurbsPlane(name=slide_name,
                                            ax=[0,0,1],
                                            width = x,
                                            lengthRatio=y/x,
                                            patchesU=self.slide_x_subdivisions,
                                            patchesV=self.slide_y_subdivisions)[0]
            tag_utils.tag_slide_geo(self.slide_nurbs)
            tag_utils.create_component_tag(self.slide_nurbs, component_name=self.component_name)
            cmds.parent(self.slide_nurbs, self.geo)
            cmds.move(center[0], center[1], center[2], self.slide_nurbs)
            
        cmds.DeleteHistory(self.slide_nurbs)
        cmds.makeIdentity(self.slide_nurbs, apply=True, t=1, r=1, s=1, n=0, pn=1)


        self.slide_nurbs_base = self.create_base(self.slide_nurbs)
        
        self.lattice_geo += [self.slide_nurbs, self.slide_nurbs_base]
        self.component_membership_nodes += [self.slide_nurbs, self.slide_nurbs_base]
        self.guide_geo +=  [self.slide_nurbs, self.slide_nurbs_base]
