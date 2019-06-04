from maya import cmds, OpenMaya

from rig_2.component import face_guide
# from rig.rigComponents import lidTest
# from rig.rigComponents import browTest
# from rig_2.component import face_guide
# from rig_2.export import utils as export_utils
# from rig.rigComponents import mouthJaw
# from rig_2.component import lip

# reload(lip)
# reload(lidTest)
# reload(browTest)
reload(face_guide)
# reload(export_utils)
# reload(mouthJaw)

# reload(mouth_guide)

# reload(lid_guide)

def build(asset_name="oldMan"):
    
    guide_file = r"C:\Users\harri\Desktop\dev\rotoslang\src\LH\python\libs\builders\oldMan\guides.py"

    cmds.file( new=True, f=True )
    # cmds.unloadPlugin("LHDeformerNodes")
    # cmds.loadPlugin("C:/Users/harri/Desktop/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/src/Debug/LHDeformerNodes")


    # asset="C:/Users/harri/Desktop/dev/rotoslang/src/scenes/assets/oldMan/oldMan.ma"
    # cmds.file( asset, i=True, f=True )
    
    
    
    
    
    
    

    mouth_jaw_guides = face_guide.Mouth_Guide()
    mouth_jaw_guides.create()
    
    lid_guides = face_guide.Lid_Guide()
    lid_guides.create()
    

    
    # lid_guides = lid_guide.Component()
    # lid_guides.create()







    # mouth_jaw_guides = mouth_guide.Component()
    # mouth_jaw_guides.create()
    

    # lid_guides = lid_guide.Component()
    # lid_guides.create()

    # mouth_jaw_guides = face_guide.Mouth_Guide()
    # mouth_jaw_guides.create()
    
    
    
    # order_before_deformer = mouth_jaw_guides.ffd_deformer
    # # Don't build guide_components
    # export_utils.import_all(filename=guide_file, build_components=False)

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

    # export_utils.import_all(filename=guide_file, build_components=False)
    
    
    # lip.build(order_before_deformer=order_before_deformer)
    
    
    
    # lidTest.test(auto_load=False, old_man=True)
    # browTest.test(auto_load=False, old_man=True)
