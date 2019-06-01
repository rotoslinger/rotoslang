import itertools, inspect, ast
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
                 hide_reference_geo=True,
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
        self.hide_reference_geo = hide_reference_geo
        self.debug = debug
        
        # vars
        self.base_names=[]
        self.geo_to_be_base=[]
        self.lattice_geo = None


    # def initialize(self):
        
    #     """ Check for a root, create if none """
    #     self.hierarchy_class = rig_hierarchy.base()
    #     self.hierarchy_class.initialize()

    #     if not cmds.objExists(self.hierarchy_class.root):
    #         self.hierarchy_class.create()

    #     self.aggr = "{0}_{1}Aggr_{2}".format(self.side, self.name, self.suffix)

    #     """
    #     Create component Hierarchy within the asset hierarchy. 
    #     These transforms should mirror the asset hierarchy's layout and should be populated based on global scaling needs.
    #     """

    #     self.geo, self.skeleton, self.rig, self.control, self.component = rig_hierarchy.init_hierarchy(side=self.side,
    #                                                                                           name=self.name,
    #                                                                                           suffix=self.suffix,
    #                                                                                           hierarchy_class=self.hierarchy_class)
    #     node_utils.get_node_agnostic("transform", name = self.aggr, parent=self.component)

    #     tag_utils.create_component_tag(self.component, self.component_name)
    #     tag_utils.tag_arg_node(self.component)
        
    #     misc.lock_attrs(node=self.aggr, attr=["all"])

    #     self.rig_geo = "C_{0}_GRP".format(self.component_name)
    #     node_utils.get_node_agnostic("transform", name = self.rig_geo, parent=self.geo)

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
            tag_utils.tag_base_geo(geo)
            tag_utils.create_component_tag(geo, component_name=self.component_name)
            # Don't need to make a base of the projection meshes, this is needed if you are doing a debug build
            geo_name = geo + "BASE"
            if not cmds.objExists(geo_name):
                cmds.duplicate(geo, n=geo_name)
                cmds.setAttr(geo_name + ".v", 0)
            self.base_geo.append(geo_name)

    def create_lattice(self):
        if cmds.objExists("C_{0}".format(self.component_name)):
            self.lattice = "C_{0}".format(self.component_name) + "Lattice"
            self.lattice_base = "C_{0}".format(self.component_name) + "Base"
            cmds.setAttr(self.lattice + ".v", 0)
            return

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
        cmds.parent(self.lattice, self.lattice_base, self.rig_geo)
        cmds.setAttr(self.lattice + ".v", 0)


    def create_controls(self):
        self.root_control, self.controls, self.clusters = cluster_lattice_sheet(self.lattice, self.s_divisions, self.t_divisions, self.control, self.rig, self.component_name)
        if self.clusters and cmds.objExists(self.root_control):
            safe_parent( self.clusters, self.root_control)

    @decorator.undo_chunk
    def create(self):
        super(Base, self).create()
        self.create_geo()
        self.create_mesh()
        self.create_nurbs()
        self.create_base_geo()
        self.create_lattice()
        self.create_controls()

def safe_parent(objects_to_parent, parent):
    if not cmds.objExists(parent):
        return
    for maya_object in objects_to_parent:
        if not cmds.objExists(maya_object):
            continue
        rel = cmds.listRelatives(maya_object, parent=True)
        if rel and rel[0] == parent:
            continue
        cmds.parent(maya_object, parent)

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
                 test = "AAAAAAAAAAAAAAA",
                 test2 = {"something":5, "soemthingelse":20.0, "sthin":"whone", "OTHER":{"inside":5}},
                 test3 = [{"something":5, "soemthingelse":20.0, "sthin":"whone", "OTHER":{"inside":5}}],
                 **kw
                 ):
        
        side="C"
        name="lipsMouthJaw"
        component_name="lipsMouthJaw"
        super(Lips_Mouth_Jaw, self).__init__(self, class_name=class_name, side=side, name=name, component_name=component_name, is_root=True,**kw) 
        # Add args to base class
        class_name = self.get_relative_path()
        self.frame = inspect.currentframe()
        self.get_args()
        # print "test3", test3
        # print "test3 type", type(test3)
        # print "test2 key1 type", type(test2["something"])
        # print "test2 key2", test2["soemthingelse"]
        # print "test2 key2 type", type(test2["soemthingelse"])
        # print "test3 value",test3[0]["OTHER"]["inside"]
        # print "test3 type", type(test3[0]["OTHER"]["inside"])
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
            
        self.upper_lip = mesh.safe_create_mesh(up_lip_dict, parent=self.rig_geo)
        self.lower_lip = mesh.safe_create_mesh(low_lip_dict, parent=self.rig_geo)
        self.mouth_jaw = mesh.safe_create_mesh(guide_elements.MOUTH_JAW, parent=self.rig_geo)
        
        for geo in [self.upper_lip, self.lower_lip, self.mouth_jaw]:
            tag_utils.tag_reference_geo(geo)
            tag_utils.create_component_tag(geo, component_name=self.component_name)

            # vis_attr = self.aggr + ".hide_reference_geo"
            # cmds.connectAttr(vis_attr, geo + ".v", f=True)


        # The slide mesh will be fit to the jaw
        self.slide_fit_to_mesh = self.mouth_jaw
        self.meshes_to_project= [self.upper_lip, self.lower_lip, self.mouth_jaw]
        self.up_lip_volume, dummy = nurbscurve.safe_create_curve(guide_elements.UP_LIP_VOLUME,
                                                                 guide_elements.UP_LIP_VOLUME["name"],
                                                                 parent=self.rig_geo,
                                                                 transform_suffix=None,
                                                                 shape_suffix=None

                                                                 )
        self.low_lip_volume, dummy = nurbscurve.safe_create_curve(guide_elements.LOW_LIP_VOLUME,
                                                                  guide_elements.LOW_LIP_VOLUME["name"],
                                                                  parent=self.rig_geo,
                                                                  transform_suffix=None,
                                                                  shape_suffix=None
                                                                  )
        [tag_utils.tag_lip_volume_curves(curve) for curve in [self.up_lip_volume, self.low_lip_volume]]
        [tag_utils.create_component_tag(curve, component_name=self.component_name) for curve in [self.up_lip_volume, self.low_lip_volume]]
                    

        self.up_lip_roll, dummy = nurbscurve.safe_create_curve(guide_elements.UP_LIP_ROLL,
                                                               guide_elements.UP_LIP_ROLL["name"],
                                                               parent=self.rig_geo,
                                                               transform_suffix=None,
                                                               shape_suffix=None

                                                               )
        self.low_lip_roll, dummy = nurbscurve.safe_create_curve(guide_elements.LOW_LIP_ROLL,
                                                                guide_elements.LOW_LIP_ROLL["name"],
                                                                parent=self.rig_geo,
                                                                transform_suffix=None,
                                                                shape_suffix=None
                                                                )
        [tag_utils.tag_lip_volume_curves(curve) for curve in [self.up_lip_roll, self.low_lip_roll]]
        [tag_utils.create_component_tag(curve, component_name=self.component_name) for curve in [self.up_lip_roll, self.low_lip_roll]]

        self.lattice_geo = [self.upper_lip, self.lower_lip, self.mouth_jaw, self.up_lip_volume, self.low_lip_volume,
                            self.up_lip_roll, self.low_lip_roll]
        self.geo_to_be_base += [self.up_lip_volume, self.low_lip_volume,
                            self.up_lip_roll, self.low_lip_roll]
    def create_mesh(self):
        self.projection_meshes = []
        for mesh in self.meshes_to_project:
            projection_mesh = get_projection_geo(mesh, self.rig_geo, self.projection_x_subdivisions, self.projection_y_subdivisions)
            tag_utils.tag_projection_mesh(projection_mesh)
            tag_utils.create_component_tag(projection_mesh, component_name=self.component_name)
            self.projection_meshes.append(projection_mesh)
        self.lattice_geo += self.projection_meshes
            
    def create_nurbs(self):
        self.slide_fit_to_mesh = self.mouth_jaw
        x, y, z, center = get_projection_dimensions(self.slide_fit_to_mesh)
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
            cmds.parent(self.slide_nurbs, self.rig_geo)
            
            cmds.move(center[0], center[1], center[2], self.slide_nurbs)
        
        self.lattice_geo.append(self.slide_nurbs)
        self.geo_to_be_base.append(self.slide_nurbs)
            


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
    if cmds.objExists(proj_name):
        return proj_name
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
    
    
    
    
    
    full_root_control_name = "{0}_{1}_CTL".format("C","{0}Root".format(component_name))
    if cmds.objExists(full_root_control_name):
        root_control = full_root_control_name
    else:
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
                                            is_ctrl_guide = True,
                                            numBuffer=1,
                                            )
        root_control.create()
        root_control=root_control.ctrl
    sides, range_names = name_utils.name_based_on_range(count=s_count, name=component_name + "Shaper",
                                                 suffixSeperator="",
                                                 suffix="",
                                                 side_name=False,
                                                 reverse_side=True,
                                                 do_return_side=True)
    controls = []
    clusters = []
    for s, t in itertools.product(range(s_count), range(t_count)):
        exists = False
        name = "{0}_{1}Handle".format(sides[s], range_names[s] + "Row{0:02}".format(t))
        if cmds.objExists(name):
            cluster = name
            exists = True
        else:
            cluster = cmds.cluster("{0}.pt[{1}][{2}][0:1]".format(lattice_name, s, t), n="{0}_{1}".format(sides[s], range_names[s] + "Row{0:02}".format(t)))[1]
        clusters.append(cluster)
        position = cmds.pointPosition("{0}.pt[{1}][{2}][1]".format(lattice_name, s, t), w=True)
        full_control_name = "{0}_{1}_CTL".format(sides[s],range_names[s] + "Row{0:02}".format(t))
        if cmds.objExists(full_control_name):
            control = full_control_name
            controls.append(full_control_name)
        else:
            control = simpleton.Component( side=sides[s],
                                        name=range_names[s] + "Row{0:02}".format(t), 
                                        parent=root_control,
                                        translate = position,
                                        rotate = [0,0,0],
                                        scale = [1,1,1],
                                        offset = [0,0,0],
                                        size=1,
                                        curveData = manip_elements.sphere_medium,
                                        component_name=component_name,
                                        null_transform = False,
                                        gimbal=False,
                                        is_ctrl_guide = True,
                                        numBuffer=1,
                                        )
            control.create()
            control = control.ctrl
            controls.append(control)
        if not exists:
            cmds.parentConstraint(control, cluster, mo=True)
            cmds.setAttr(cluster + ".v", 0)
    # After everything has been created make it dynamic symmetric
    for control in controls:
        if "L_" in control:
            mirror_utils.add_dynamic_mirror_connection([control])
    return root_control, controls, clusters


        
    
