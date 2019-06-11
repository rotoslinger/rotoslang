from maya import cmds, OpenMaya
from rig_2 import decorator

from rig_2.filepath import utils as filepath_utils
reload(filepath_utils)
from rig_2.export import utils as export_utils
reload(export_utils)
from rig_2.guide import utils as guide_utils
reload(guide_utils)


from rig_2.component import face_guide
reload(face_guide)
from rig_2.component import lid
reload(lid)

from rig.rigComponents import mouthJaw
reload(mouthJaw)

from rig_2.component import lip, mouth, brow, face
reload(mouth)
reload(lip)
reload(brow)
reload(face)

DEBUG = False

@decorator.suppress_warnings
def build(asset_name="oldMan",
          reload_plugins=True,
          asset_filepath="C:/Users/harri/Desktop/dev/rotoslang/src/scenes/assets/oldMan/oldManBodyRig.ma",
          attach_to="head_output"):

    guide_file = filepath_utils.get_file_by_asset_name(asset_name, file="guides")
    get_file(asset_filepath, asset_name)
    
    
    # Create Guides First
    mouth_jaw_guides = face_guide.Mouth_Guide(hide_on_build=True)
    mouth_jaw_guides.create()
    
    lid_guides = face_guide.Lid_Guide(hide_on_build=True)
    lid_guides.create()

    brow_guides = face_guide.Brow_Guide(hide_on_build=True)
    brow_guides.create()
    
    # Import guides for the guide components.
    # They need to be placed in the proper location before the rigs build to make thing simpler
    # Because we have built the guide components in the file, we will not want to build components on import
    export_utils.import_all(filename=guide_file, build_components=False)

    lip_class = build_lip(mouth_jaw_guides)
    # mouth_class = build_mouth(mouth_jaw_guides) 
    # l_lids_class, r_lids_class = build_lids(lid_guides)
    # brow_class = build_brow(brow_guides)

    # The face class will be used to wire everything together... it contains the face_anchor
    face_class = face.Face(face_driver="head_output")
    face_class.create()
    
    # # import the guides again, this time for all of the non guide components
    export_utils.import_all(filename=guide_file, build_components=False)


    ### FINALIZE ### 
    # be sure to comment this out if you need to fit your guides!!!!!!!!!!!!!
    guide_utils.bake_all_guides()

    # cmds.select("C_bodyBind_GEO")
    # cmds.viewFit()
    
def build_brow(brow_guides):
    brow_class = brow.Brow(guide_class=brow_guides,
                            leftBrowMesh = "C_brow_GEO",
                            leftBrowBaseMesh = "C_browBase_GEO",
                            rightBrowMesh = "C_brow_GEO",
                            rightBrowBaseMesh = "C_browBase_GEO",
                            slidePatch="C_browGuide_SLDE",
                            slidePatchBase="C_browGuide_SLDEBASE",
                            L_projectionMesh="L_brow_REF_PRJ",
                            R_projectionMesh="R_brow_REF_PRJ",
                            )
    brow_class.create()
    return brow_class

def build_lids(lid_guides):
    l_lid_class = lid.Lid(guide_class=lid_guides,
                          component_name="lLids",
                          tierCounts=[1,3,5],
                          side="L",
                          upperLipMesh="L_upperLid",
                          upperLipBaseMesh="L_upperLidBase",
                          lowerLidMesh="L_lowerLid",
                          lowerLidBaseMesh="L_lowerLidBase",
                          slidePatch="L_lidGuide_SLDE",
                          slidePatchBase="L_lidGuide_SLDEBASE",
                          projectionMeshUpper="L_upperLid_REF_PRJ",
                          projectionMeshLower="L_lowerLid_REF_PRJ",
                          rivet_orient_patch = "L_lidGuide_RivetOrientPatch",
                          )
    
    l_lid_class.create()
    r_lid_class = lid.Lid(guide_class=lid_guides,
                          component_name="rLids",
                          tierCounts=[1,3,5],
                          side="R",
                          upperLipMesh="R_upperLid",
                          upperLipBaseMesh="R_upperLidBase",
                          lowerLidMesh="R_lowerLid",
                          lowerLidBaseMesh="R_lowerLidBase",
                          slidePatch="R_lidGuide_SLDE",
                          slidePatchBase="R_lidGuide_SLDEBASE",
                          projectionMeshUpper="R_upperLid_REF_PRJ",
                          projectionMeshLower="R_lowerLid_REF_PRJ",
                          rivet_orient_patch = "R_lidGuide_RivetOrientPatch",
                          )
    r_lid_class.create()
    return l_lid_class, r_lid_class

def build_lip(mouth_jaw_guides):

    lip_class = lip.Lip(
                 lip_guide_class=mouth_jaw_guides,
                 tierCount1=1,
                 tierCount2=3,
                 tierCount3=5,    
                 upper_remove_point_indicies=[11, 12, 29, 32, 40, 44, 45, 48, 71, 75, 76, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 123, 125, 133, 148, 161, 164, 172, 176, 177, 180, 203, 207, 208, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 255, 257, 265, 280],
                 lower_remove_point_indicies=[8, 10, 15, 16, 17, 39, 44, 45, 70, 71, 78, 79, 80, 82, 84, 85, 86, 90, 92, 93, 94, 95, 96, 97, 98, 99, 106, 107, 116, 124, 125, 133, 134, 135, 157, 162, 163, 188, 189, 196, 197, 198, 200, 202, 203, 204, 208, 210, 211, 212, 213, 214, 215, 216, 217, 224, 225, 234, 242, 243],
                 control_rivet_mesh="C_bodyBind_GEO",
                 )
    
    lip_class.create()

def build_mouth(mouth_jaw_guides):
    MouthJawClass = mouth.Mouth(control_rivet_mesh="C_bodyBind_GEO",
                                component_name = "Mouth"
                                )
    MouthJawClass.create() 
    
    
def get_file(asset_filepath, asset_name,  reload_plugins=True):
    cmds.file( new=True, f=True )

    if reload_plugins:
        cmds.unloadPlugin("LHDeformerNodes")
        cmds.loadPlugin("C:/Users/harri/Desktop/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/src/Debug/LHDeformerNodes")

    cmds.file( asset_filepath, i=True, f=True )



