from maya import cmds, OpenMaya

from rig_2.component import face_guide
reload(face_guide)
from rig.rigComponents import lidTest
reload(lidTest)
from rig.rigComponents import browTest
reload(browTest)
from rig_2.component import face_guide
reload(face_guide)

from rig_2.export import utils as export_utils
reload(export_utils)
from rig.rigComponents import mouthJaw
reload(mouthJaw)

from rig_2.component import lip, mouth
reload(mouth)
reload(lip)

from rig_2.filepath import utils as filepath_utils
reload(filepath_utils)



def build(asset_name="oldMan", reload_plugins=True, asset_filepath="C:/Users/harri/Desktop/dev/rotoslang/src/scenes/assets/oldMan/oldMan.ma"):
    
    guide_file = filepath_utils.get_file_by_asset_name(asset_name, file="guides")
    get_file(asset_filepath, asset_name)
    
    
    # Create Guides First
    mouth_jaw_guides = face_guide.Mouth_Guide(hide_on_build=True)
    mouth_jaw_guides.create()
    
    # lid_guides = face_guide.Lid_Guide()
    # lid_guides.create()
    # l_lid_guides_ffd = lid_guides.l_ffd_deformer
    # r_lid_guides_ffd = lid_guides.r_ffd_deformer

    # brow_guides = face_guide.Brow_Guide()
    # brow_guides.create()
    # brow_guides_ffd = brow_guides.ffd_deformer
    
    # Import guides for the guide components.
    # They need to be placed in the proper location before the rigs build to make thing simpler
    # Because we have built the guide components in the file, we will not want to build components on import
    export_utils.import_all(filename=guide_file, build_components=False)

    build_lip(mouth_jaw_guides)
    build_mouth(mouth_jaw_guides)
                
    '''
    build_mouth(mouth_jaw_guides)
    build_lids(lid_guides)
    build_brows(brow_guides)
    '''
    # # import the guides again, this time for all of the non guide components
    export_utils.import_all(filename=guide_file, build_components=False)


    cmds.select("C_bodyBind_GEO")
    cmds.viewFit()


def get_file(asset_filepath, asset_name,  reload_plugins=True):
    cmds.file( new=True, f=True )

    if reload_plugins:
        cmds.unloadPlugin("LHDeformerNodes")
        cmds.loadPlugin("C:/Users/harri/Desktop/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/src/Debug/LHDeformerNodes")

    cmds.file( asset_filepath, i=True, f=True )


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
    MouthJawClass = mouth.Mouth(control_rivet_mesh="C_bodyBind_GEO")
    MouthJawClass.create() 
    # MouthJawClass = mouthJaw.MouthJaw(
    #              nameMouth="mouth",
    #              nameJaw="jaw",
    #              deformMesh="jawMouth",
    #              baseGeoToDeform="jawMouthBase",
                 
    #              slidePatch="C_mouthGuide_SLDE",
    #              slidePatchBase="C_mouthGuide_SLDEBASE",
    #              projectionMesh="C_mouthJawPkg_PRJ",
    #              characterName = "character",
    #              controlParent="C_control_GRP",
    #              rigParent="C_rig_GRP",
    #              ctrlAutoPositionThreshold=.09,
    # )
    # MouthJawClass.create() 
    # cmds.select(MouthJawClass.mat_def_translate.controls)
    # cmds.viewFit()

def build_lids(lid_guides):
    lidTest.test(auto_load=False, old_man=True)

def build_brow(brow_guides):
    browTest.test(auto_load=False, old_man=True)
