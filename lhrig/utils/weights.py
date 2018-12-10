import sys
linux = '/corp/projects/eng/lharrison/workspace/levi_harrison_test'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)


# import math, sys
# import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

def rename_skin_clusters():
    skins = cmds.ls(type = "skinCluster")
    if skins:
        for i in skins:
            geom = cmds.skinCluster(i,q=True, g = True)
            name = geom[0].split("_")
            name = name[0]+"_"+name[1]+"_SKN"
            cmds.rename(i,name)
#############################################
#---example
# rename_skin_clusters()
#############################################



def skin_to_bind_jnts(geoms):
    test_jnts = cmds.ls(type = "joint")
    if test_jnts:
        bind_jnts = [x for x in test_jnts if cmds.objExists(x + ".BIND")]
        if bind_jnts:
            for i in range(len(geoms)):
                #skin, name skin cluster name of geometry with "SKN" suffix
                #select bind joints, skin to them
                name = geoms[i].split("_")
                name = name[0]+"_"+name[1]+"_SKN"
#                 cmds.makeIdentity(geoms[i], 
#                                   apply = True,
#                                   t = 1, r = 1, s = 1)
                
                cmds.skinCluster(bind_jnts,
                                 geoms[i],
                                 tsb = True,
#                                  ignoreSelected = True,
                                 name = name,
                                 )
def skin_to_weight_jnts(geoms, max_influences = 0):
    test_jnts = cmds.ls(type = "joint")
    if test_jnts:
        bind_jnts = [x for x in test_jnts if cmds.objExists(x + ".SKIN")]
        if bind_jnts:
            for i in range(len(geoms)):
                #skin, name skin cluster name of geometry with "SKN" suffix
                #select bind joints, skin to them
                name = geoms[i].split("_")
                name = name[0]+"_"+name[1]+"_SKN"
#                 cmds.makeIdentity(geoms[i], 
#                                   apply = True,
#                                   t = 1, r = 1, s = 1)
                if max_influences <= 0:
                    cmds.skinCluster(bind_jnts,
                                     geoms[i],
                                     tsb = True,
                                     name = name,
                                     )
                else:
                    cmds.skinCluster(bind_jnts,
                                     geoms[i],
                                     tsb = True,
                                     obeyMaxInfluences = True,
                                     maximumInfluences = max_influences,
                                     name = name,
                                     )
                
#############################################
#---example
# skin_to_bind_jnts(["C_body_GEO", 
#                    'L_holster00plane_PLY',
#                    'L_holster01plane_PLY',
#                    'L_holster02plane_PLY',
#                    'L_holster03plane_PLY',
#                    'L_holster04plane_PLY',
#                    'L_holster05plane_PLY',
#                    'L_holster06plane_PLY',
#                    'R_holster00plane_PLY',
#                    'R_holster01plane_PLY',
#                    'R_holster02plane_PLY',
#                    'R_holster03plane_PLY',
#                    'R_holster04plane_PLY',
#                    'R_holster05plane_PLY'])
##############################################



def skin_to_bind_sec_jnts(geoms):
    test_jnts = cmds.ls(type = "joint")
    if test_jnts:
        sec_jnts = [x for x in test_jnts if cmds.objExists(x + ".SEC_BIND")]
        bind_jnts = [x for x in test_jnts if cmds.objExists(x + ".BIND")]
        all_jnts = sec_jnts + bind_jnts
        if all_jnts:
            for i in range(len(geoms)):
                #skin, name skin cluster name of geometry with "SKN" suffix
                #select bind joints, skin to them
                name = geoms[i].split("_")
                name = name[0]+"_"+name[1]+"_SKN"
                cmds.skinCluster(all_jnts,
                                 geoms[i],
                                 tsb = True,
                                 name = name,
                                 )
def skin_to_sec_skin_jnts(geoms):
    test_jnts = cmds.ls(type = "joint")
    if test_jnts:
        sec_jnts = [x for x in test_jnts if cmds.objExists(x + ".SEC_SKIN")]
        bind_jnts = [x for x in test_jnts if cmds.objExists(x + ".SKIN")]
        all_jnts = sec_jnts + bind_jnts
        if all_jnts:
            for i in range(len(geoms)):
                #skin, name skin cluster name of geometry with "SKN" suffix
                #select bind joints, skin to them
                name = geoms[i].split("_")
                name = name[0]+"_"+name[1]+"_SKN"
                cmds.skinCluster(all_jnts,
                                 geoms[i],
                                 tsb = True,
                                 name = name,
                                 )
#############################################
#example
# skin_to_bind_sec_jnts(["C_holster_GEO"])
#############################################



def export_skins(path):
    # get all skin clusters in the scene and export them to xml files
    skins = cmds.ls(type = "skinCluster")
    for i in skins:
#         geom = cmds.skinCluster(q=True, g = True)
#         print geom
#         cmds.skinPercent(i,normalize = True)
        cmds.deformerWeights(i + ".xml",
                             export = True, 
                             deformer=i,
                             path = path)
#############################################
#---example
weights_path = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig/insomniacWeights"
export_skins(weights_path)
#############################################



def import_skins(path):
    # if a skin cluster exists try to import to it
    skins = cmds.ls(type = "skinCluster")
    if skins:

        for i in skins:
            #print "something"

    #         geom = cmds.skinCluster(q=True, g = True)
    #         print geom
            cmds.deformerWeights(i + ".xml",
                             im = True,
                             method = "index",
                             deformer=i,
                             path = path)

#             try:
#                 cmds.deformerWeights(i + ".xml",
#                                      im = True,
#                                      method = "index",
#                                      deformer=i,
#                                      path = path)
#             except:
#                 pass
#             geom = cmds.skinCluster(i,q=True, g = True)
#             cmds.skinPercent(i,geom,normalize = True)
            cmds.skinCluster(i , e = True, forceNormalizeWeights = True);
#############################################
#---example
# path = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig/insomniacWeights"
# import_skins(path)
#############################################


