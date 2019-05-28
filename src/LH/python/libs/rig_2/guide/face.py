import itertools
from maya import cmds, OpenMaya
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
from rig_2.manipulator import nurbscurve
reload(nurbscurve)


class Base(component_base.Subcomponent):
    def __init__(self,
                 s_divisions=5,
                 t_divisions=7,
                 local_influence=8,
                 projection_x_subdivisions=10,
                 projection_y_subdivisions=5,
                 slide_x_subdivisions=10,
                 slide_y_subdivisions=6,
                 helper_geo_dict=None,
                 **kw
                 ):
        super(Base, self).__init__(self, **kw)
        saved_args = locals()
        print saved_args
        
        # args
        self.s_divisions = s_divisions
        self.t_divisions = t_divisions
        self.helper_geo_dict = helper_geo_dict
        self.projection_x_subdivisions = projection_x_subdivisions
        self.projection_y_subdivisions = projection_y_subdivisions
        self.slide_x_subdivisions = slide_x_subdivisions
        self.slide_y_subdivisions = slide_y_subdivisions
        self.base_names=[]

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
    def create_nurbs(self):
        return
    
    def create_geo(self):
        return
    
    def create_mesh(self):
        return

    def create_lattice(self):
        return
    
    def create_controls(self):
        return

    def create(self):
        super(Base, self).create()
        self.create_geo()
        self.create_mesh()
        self.create_nurbs()
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
                
                 up_lip_complex=False,
                 low_lip_complex=False,
                 slide_patch_x_overshoot=0,
                 slide_patch_y_overshoot=0,
                 **kw
                 ):
        self.component_name="lipsMouthJaw"
        
        self.mouth_jaw_component_name="mouthJaw"
        self.lips_component_name="lips"
        super(Lips_Mouth_Jaw, self).__init__(self, **kw)
        self.component_name="lipsMouthJaw"
        
        self.mouth_jaw_component_name="mouthJaw"
        self.lips_component_name="lips"
        saved_args = locals()
        print saved_args
        
        # args
        self.up_lip_complex = up_lip_complex
        self.low_lip_complex = low_lip_complex
        self.slide_patch_x_overshoot = slide_patch_x_overshoot
        self.slide_patch_x_overshoot = slide_patch_x_overshoot
        # vars
        self.upper_lip = None
        self.lower_lip = None
        self.mouth_jaw = None
        
        
        
        
        self.curves_list = []
        self.base_names=[]

    def initialize(self):
        super(Lips_Mouth_Jaw, self).initialize()
        self.geo_rig = "C_{0}_GRP".format(self.component_name)
        if not cmds.objExists(self.geo_rig):
            self.geo_rig = cmds.createNode("transform", n=self.geo_rig, parent=self.geo)

    
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
        dummy=None
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
        print self.up_lip_volume
        
    def create_mesh(self):
        self.projection_meshes = []
        for mesh in self.meshes_to_project:
            self.projection_meshes.append(get_projection_geo(mesh, self.geo_rig, self.projection_x_subdivisions, self.projection_y_subdivisions))
            
    def create_nurbs(self):
        self.slide_fit_to_mesh = self.mouth_jaw
        x, y, z, center = get_projection_dimensions(self.slide_fit_to_mesh)
        slide_name= "C_{0}_SLDE".format(self.component_name)
        self.slide_nurbs = cmds.nurbsPlane(name=slide_name,
                                           ax=[0,0,1],
                                           width = x,
                                           lengthRatio=y/x,
                                           patchesU=self.slide_x_subdivisions,
                                           patchesV=self.slide_y_subdivisions)
        cmds.parent(self.slide_nurbs, self.geo_rig)
        
        cmds.move(center[0], center[1], center[2], self.slide_nurbs)

    def create_lattice(self):
        return
    
    def create_controls(self):
        return



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
    return plane


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
    print x, y, z
    return abs(x), abs(y), abs(z), center

def cluster_lattice_sheet(lattice_name, s_count, t_count):
    return_clusters = []
    for s, t in itertools.product(range(s_count), range(t_count)):
        return_clusters.append(cmds.cluster(
            "ffd2Lattice.pt[{0}][{1}][0:1]".format(s, t))[0])
