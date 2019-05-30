import itertools, inspect
from collections import OrderedDict

from maya import cmds

from rig_2.name import utils as name_utils
reload(name_utils)
from rig_2.manipulator import control
reload(control)
from rig_2.tag import utils as tag_utils
reload(tag_utils)

from rig_2.component import base as component_base
reload(component_base)
from rig.utils import misc
reload(misc)
from rig_2.shape import mesh
reload(mesh)
from rig_2.root import hierarchy as rig_hierarchy
reload(rig_hierarchy)
from rig_2.node import utils as node_utils
reload(node_utils)
from rig_2.guide import elements as guide_elements
reload(guide_elements)
from rig_2.shape import nurbscurve

reload(nurbscurve)
from rig.rigComponents import simpleton
reload(simpleton)
from rig_2.manipulator import elements as manip_elements
reload(manip_elements)
from rig.deformers import utils as deformer_utils

reload(deformer_utils)
from rig_2 import decorator
reload(decorator)

from rig_2.mirror import utils as mirror_utils
reload(mirror_utils)

class Base(component_base.Subcomponent):
    def __init__(self,
                 parent_component_class=None,
                 class_name="rig_2.guide.face.Base",
                 side="C",
                 name="base",
                 component_name="base",
                 num_local_influence=4,
                 s_divisions=5,
                 t_divisions=7,
                 projection_x_subdivisions=10,
                 projection_y_subdivisions=5,
                 slide_x_subdivisions=10,
                 slide_y_subdivisions=6,
                 slide_patch_x_overshoot=0,
                 slide_patch_y_overshoot=0,
                 debug=False,
                 **kw
                 ):
        super(Base, self).__init__(self, class_name=class_name, side=side, name=name, component_name=component_name, **kw)
        # self.name="subcomponent",
        # If you don't want to inherit the last classes args, create a clean dictionary
        class_name = self.get_relative_path()
        self.ordered_args = OrderedDict()
        self.frame = inspect.currentframe()
        self.get_args()

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
        self.debug = debug
        
        # vars
        self.base_names=[]
        self.geo_to_be_base=[]
        self.lattice_geo = None




    def initialize(self):
        """ Check for a root, create if none """
        self.hierarchy_class = rig_hierarchy.base()
        self.hierarchy_class.initialize()

        if not cmds.objExists(self.hierarchy_class.root):
            self.hierarchy_class.create()

        self.aggr = "{0}_{1}Aggr_{2}".format(self.side, self.name, self.suffix)

        """
        Create component Hierarchy within the asset hierarchy. 
        These transforms should mirror the asset hierarchy's layout and should be populated based on global scaling needs.
        """

        self.geo, self.skeleton, self.rig, self.control, self.component = rig_hierarchy.init_hierarchy(side=self.side,
                                                                                              name=self.name,
                                                                                              suffix=self.suffix,
                                                                                              hierarchy_class=self.hierarchy_class)
        node_utils.get_node_agnostic("transform", name = self.aggr, parent=self.component)
        self.geo_rig = "C_{0}_GRP".format(self.component_name)
        if not cmds.objExists(self.geo_rig):
            self.geo_rig = cmds.createNode("transform", n=self.geo_rig, parent=self.geo)
            
        print "AGGR", self.aggr, self.component_name
        tag_utils.create_component_tag(self.aggr, self.component_name)
        tag_utils.tag_arg_node(self.aggr)
        misc.lock_attrs(node=self.aggr, attr=["all"])

    def create_nurbs(self):
        return
    
    def create_geo(self):
        return
    
    def create_mesh(self):
        return

    def create_base_geo(self):
        geo_to_be_base = self.geo_to_be_base
        if self.debug:
            geo_to_be_base = self.lattice_geo
        # Geometry should be named neatly, if it is not this will not work
        self.base_geo = []
        for geo in geo_to_be_base:
            # Don't need to make a base of the projection meshes, this is needed if you are doing a debug build
            geo_name = geo + "BASE"
            cmds.duplicate(geo, n=geo_name)
            cmds.setAttr(geo_name + ".v", 0)
            self.base_geo.append(geo_name)

    def create_lattice(self):
        self.ffd_deformer, self.lattice, self.lattice_base = cmds.lattice(self.lattice_geo,
                                                                          n="C_{0}".format(self.component_name),
                                                                          outsideLattice=1,
                                                                          ldivisions=(self.num_local_influence,
                                                                                      self.num_local_influence,
                                                                                      self.num_local_influence),
                                                                          divisions=(self.s_divisions,
                                                                                     self.t_divisions,
                                                                                     2),
                                                                          objectCentered=True
                                                                          )
        cmds.parent(self.lattice, self.lattice_base, self.geo_rig)
        cmds.setAttr(self.lattice + ".v", 0)


    def create_controls(self):
        self.controls = cluster_lattice_sheet(self.lattice, self.s_divisions, self.t_divisions, self.control, self.rig, self.component_name)

    @decorator.undo_chunk
    def create(self):
        super(Base, self).create()
        self.create_geo()
        self.create_mesh()
        self.create_nurbs()
        self.create_base_geo()
        self.create_lattice()
        self.create_controls()



class Lips_Mouth_Jaw(Base):
    def __init__(self,
                 # INHERITTED
                #  s_divisions=5,
                #  t_divisions=7,
                #  local_influence=8,
                #  projection_x_subdivisions=9,
                #  projection_y_subdivisions=9,
                #  slide_x_subdivisions=9,
                #  slide_y_subdivisions=9,
                #  helper_geo_dict=None,
                 class_name=None,
                 side="C",
                 name="lipsMouthJaw",
                 component_name="lipsMouthJaw",
                 up_lip_complex=False,
                 low_lip_complex=False,
                 **kw
                 ):
        
        side="C"
        name="lipsMouthJaw"
        component_name="lipsMouthJaw"
        super(Lips_Mouth_Jaw, self).__init__(self, class_name=class_name, side=side, name=name, component_name=component_name, **kw) 
        # Add args to base class
        class_name = self.get_relative_path()
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
        self.component_name="lipsMouthJaw"
        self.mouth_jaw_component_name="mouthJaw"
        self.lips_component_name="lips"
        

    
    def create_geo(self):
        up_lip_dict = guide_elements.UP_LIP_SIMPLE
        if self.up_lip_complex:
            up_lip_dict = guide_elements.UP_LIP_COMPLEX
        low_lip_dict = guide_elements.LOW_LIP_SIMPLE
        if self.low_lip_complex:
            low_lip_dict = guide_elements.LOW_LIP_COMPLEX
            
        self.upper_lip = mesh.create_mesh(up_lip_dict, parent=self.geo_rig)
        self.lower_lip = mesh.create_mesh(low_lip_dict, parent=self.geo_rig)
        self.mouth_jaw = mesh.create_mesh(guide_elements.MOUTH_JAW, parent=self.geo_rig)
        # The slide mesh will be fit to the jaw
        self.slide_fit_to_mesh = self.mouth_jaw
        self.meshes_to_project= [self.upper_lip, self.lower_lip, self.mouth_jaw]
        self.up_lip_volume, dummy = nurbscurve.create_curve(guide_elements.UP_LIP_VOLUME,
                                                            guide_elements.UP_LIP_VOLUME["name"],
                                                            parent=self.geo_rig,
                                                            transform_suffix=None,
                                                            shape_suffix=None

                                                            )
        self.low_lip_volume, dummy = nurbscurve.create_curve(guide_elements.LOW_LIP_VOLUME,
                                                             guide_elements.LOW_LIP_VOLUME["name"],
                                                             parent=self.geo_rig,
                                                             transform_suffix=None,
                                                             shape_suffix=None

                                                             )
        self.up_lip_roll, dummy = nurbscurve.create_curve(guide_elements.UP_LIP_ROLL,
                                                          guide_elements.UP_LIP_ROLL["name"],
                                                          parent=self.geo_rig,
                                                          transform_suffix=None,
                                                          shape_suffix=None

                                                          )
        self.low_lip_roll, dummy = nurbscurve.create_curve(guide_elements.LOW_LIP_ROLL,
                                                           guide_elements.LOW_LIP_ROLL["name"],
                                                           parent=self.geo_rig,
                                                           transform_suffix=None,
                                                           shape_suffix=None
                                                           )
        self.lattice_geo = [self.upper_lip, self.lower_lip, self.mouth_jaw, self.up_lip_volume, self.low_lip_volume,
                            self.up_lip_roll, self.low_lip_roll]
        self.geo_to_be_base += [self.up_lip_volume, self.low_lip_volume,
                            self.up_lip_roll, self.low_lip_roll]
    def create_mesh(self):
        self.projection_meshes = []
        for mesh in self.meshes_to_project:
            self.projection_meshes.append(get_projection_geo(mesh, self.geo_rig, self.projection_x_subdivisions, self.projection_y_subdivisions))
        self.lattice_geo += self.projection_meshes
            
    def create_nurbs(self):
        self.slide_fit_to_mesh = self.mouth_jaw
        x, y, z, center = get_projection_dimensions(self.slide_fit_to_mesh)
        slide_name= "C_{0}_SLDE".format(self.component_name)
        x += self.slide_patch_x_overshoot
        y += self.slide_patch_y_overshoot
        self.slide_nurbs = cmds.nurbsPlane(name=slide_name,
                                           ax=[0,0,1],
                                           width = x,
                                           lengthRatio=y/x,
                                           patchesU=self.slide_x_subdivisions,
                                           patchesV=self.slide_y_subdivisions)[0]
        cmds.parent(self.slide_nurbs, self.geo_rig)
        
        cmds.move(center[0], center[1], center[2], self.slide_nurbs)
        self.lattice_geo.append(self.slide_nurbs)
        self.geo_to_be_base.append(self.slide_nurbs)
            



def get_slide_geo(mesh, parent, x_divisions=10, y_divisions=10):
    return

def get_projection_geo(mesh,
                       parent,
                       x_divisions=10,
                       y_divisions=10,
                       split_suffix="_GEO"):
    proj_name = mesh
    if split_suffix in mesh:
        proj_name = mesh.split(split_suffix)[0]
    proj_name += "_PRJ"
    x, y, z, center = get_projection_dimensions(mesh)
    plane = cmds.polyPlane( name = proj_name,
                           subdivisionsX = x_divisions,
                           subdivisionsY = y_divisions,
                           width = x,
                           height = y,
                           ax=[0,0,1])
    cmds.parent(plane, parent)
    
    cmds.move(center[0], center[1], center[2], plane)
    return plane[0]


def get_projection_dimensions(meshes, z_at_origin=True):
    # xmin, ymin, zmin, xmax, ymax, zmax
    bb = cmds.exactWorldBoundingBox(meshes)
    x = bb[0] - bb[3]
    y = bb[1] - bb[4]
    z = bb[2] - bb[5]
    center = cmds.objectCenter(meshes)
    # Put projection in front
    if z_at_origin:
        center[2] = 0
    return abs(x), abs(y), abs(z), center

def cluster_lattice_sheet(lattice_name, s_count, t_count, control_parent, handle_parent, component_name):
    return_controls = []
    bb = cmds.exactWorldBoundingBox(lattice_name)
    x = bb[0] - bb[3]
    y = bb[1] - bb[4]
    z = bb[2] - bb[5]
    center = cmds.objectCenter(lattice_name)
    offset = [center[0], bb[1], center[2]]
    root_control = simpleton.Component( side="C",
                                        name="{0}Root".format(component_name), 
                                        parent=control_parent,
                                        translate = center,
                                        rotate = [0,0,0],
                                        scale = [1,1,1],
                                        offset = offset,
                                        size=10,
                                        curveData = manip_elements.circle,
                                        component_name=component_name,
                                        null_transform = False,
                                        is_ctrl_guide = True
                                        )
    root_control.create()
    sides, range_names = name_utils.name_based_on_range(count=s_count, name=component_name + "Shaper",
                                                 suffixSeperator="",
                                                 suffix="",
                                                 side_name=False,
                                                 reverse_side=True,
                                                 do_return_side=True)
    controls = []
    for s, t in itertools.product(range(s_count), range(t_count)):
        cluster = cmds.cluster("{0}.pt[{1}][{2}][0:1]".format(lattice_name, s, t))[1]
        position = cmds.pointPosition("{0}.pt[{1}][{2}][1]".format(lattice_name, s, t), w=True)
        control = simpleton.Component( side=sides[s],
                                    name=range_names[s] + "Row{0:02}".format(t), 
                                    parent=root_control.ctrl,
                                    translate = position,
                                    rotate = [0,0,0],
                                    scale = [1,1,1],
                                    offset = [0,0,0],
                                    size=1,
                                    curveData = manip_elements.sphere_medium,
                                    component_name=component_name,
                                    null_transform = False,
                                    gimbal=False,
                                    is_ctrl_guide = True
                                    )
        control.create()
        controls.append(control.ctrl)
        cmds.parentConstraint(control.ctrl, cluster, mo=True)
        cmds.setAttr(cluster + ".v", 0)
    # After everything has been created make it dynamic symmetric
    for control in controls:
        if "L_" in control:
            mirror_utils.add_dynamic_mirror_connection([control])
    return controls


        
    
