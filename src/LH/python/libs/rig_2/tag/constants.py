ARG_UI_FILTER = ["COMPONENT_ARG_NODE", "COMPONENT_MEMBERSHIP"]
TAG_VIS_SEL_PANEL_IGNORE = ["WEIGHT_CURVE", "FALLOFF_WEIGHT_CURVE", "NO_EXPORT", "EXPORT_OVERRIDE", "GUIDE_CACHEABLE"]









WILDCARD_____ = "Rigging wildcard tags.  These are for getting common rig items."
# Commonly Used Wildcard
WILDCARD______ROOT_SKEL_JOINT = "ROOT_SKEL_JOINT"
WILDCARD______GIMBAL = "GIMBAL"
WILDCARD______CONTROL = "CONTROL"
WILDCARD______BUFFER = "BUFFER"
WILDCARD______BUFFER_SHAPE = "BUFFER_SHAPE"
WILDCARD______CONTROL_SHAPE = "CONTROL_SHAPE"
WILDCARD______GUIDE = "GUIDE"
WILDCARD______DELETE_ME = "DELETE_ME"

### RIG HIERARCHY TAGS
### These will be used for doing rig cleanup and locking before a publish
### They will also make it extremely easy to unlock the rig and work on it
### GEO_GROUP will have overrides turned on and will be set to reference
HIER_____ = "Rig hierarchy tags.  These are places to put things, and where to do general rig cleanup."
HIER_____ROOT_GRP = "ROOT_GRP"
HIER_____ROOT_GRP = "ROOT_GRP"
HIER_____MAINTENANCE_GRP = "MAINTENANCE_GRP"
HIER_____RIG_GRP = "RIG_GRP"
HIER_____RIG_CONTROL_GRP = "RIG_CONTROL_GRP"
HIER_____RIG_CONTROL_SIZE_GRP = "RIG_CONTROL_SIZE_GRP"

HIER_____SKELETON_GRP = "SKELETON_GRP"
HIER_____BIND_JOINT_GRP = "BIND_JOINT_GRP"
HIER_____HELPER_JOINT_GRP = "HELPER_JOINT_GRP"
HIER_____GEO_GRP = "GEO_GRP"
HIER_____GUIDE_SHAPE = "GUIDE_SHAPE"
HIER_____BIND = "BIND"


# ################# FACE RIG ################# #
FACE_____= "Face rig tags.  These all have to do with the creation of the face rig."
FACE_____SLIDE_GEO="SLIDE_GEO"
FACE_____BASE_GEO="BASE_GEO"
FACE_____GUIDE_CURVES="GUIDE_CURVES"
FACE_____LID_CURVES="LID_CURVES"
FACE_____BROW_CURVES="BROW_CURVES"
FACE_____LIP_VOLUME_CURVES="LIP_VOLUME_CURVES"
FACE_____LIP_ROLL_CURVES="LIP_ROLL_CURVES"
FACE_____PROJECTION_MESH="PROJECTION_MESH"
FACE_____REFERENCE_GEO="REFERENCE_GEO"
FACE_____GUIDE_GEO="GUIDE_GEO"
FACE_____EXPORT_OVERRIDE="EXPORT_OVERRIDE"
FACE_____RIVET_ORIENT_PATCH="RIVET_ORIENT_PATCH"
FACE_____GUIDE_CACHEABLE="GUIDE_CACHEABLE"
FACE_____DYNAMIC_MIRRORED="DYNAMIC_MIRRORED"
FACE_____WEIGHT_CURVE="WEIGHT_CURVE"
FACE_____FALLOFF_WEIGHT_CURVE="FALLOFF_WEIGHT_CURVE"

#################################################
LIB_DA = "These are tags without a category."
LIB_D_WEIGHTED_MESH = "WEIGHTED_MESH",
LIB_D_GUIDE_CLASS = "GUIDE_CLASS",
LIB_D_COMPONENT_ARG_NODE = "COMPONENT_ARG_NODE",
LIB_D_RIVET_MESH="RIVET_MESH",



TAG_LIBRARY = { "misc":
                        [
                        "WEIGHTED_MESH",
                        "GUIDE_CLASS",
                        "COMPONENT_ARG_NODE",
                        "RIVET_MESH",
                        ],
                # ################# FACE GUIDES ################# #
                "face_guide":
                            [
                            "SLIDE_GEO",
                            "BASE_GEO",
                            "GUIDE_CURVES",
                            "LID_CURVES",
                            "BROW_CURVES",
                            "LIP_VOLUME_CURVES",
                            "LIP_ROLL_CURVES",
                            "PROJECTION_MESH",
                            "REFERENCE_GEO",
                            "GUIDE_GEO",
                            "EXPORT_OVERRIDE",
                            "RIVET_ORIENT_PATCH",
                            "GUIDE_CACHEABLE",
                            ],
                #################################################

                ### RIG HIERARCHY TAGS
                ### These will be used for doing rig cleanup and locking before a publish
                ### They will also make it extremely easy to unlock the rig and work on it
                ### GEO_GROUP will have overrides turned on and will be set to reference
                "rig_hierarchy":
                                [
                                "ROOT_GRP",
                                "CONTROL_GRP",
                                "MAINTENANCE_GRP",
                                "RIG_GRP",
                                "CONTROL_RIG_GRP",
                                "SKELETON_GRP",
                                "BIND_JOINT_GRP",
                                "ROOT_SKEL_JOINT",
                                "HELPER_JOINT_GRP",
                                "GEO_GRP",
                                "GIMBAL",
                                "CONTROL",
                                "BUFFER",
                                "BUFFER_SHAPE",
                                "CONTROL_SHAPE",
                                "GUIDE",
                                "DELETE_ME",
                                "GUIDE_SHAPE",
                                "BIND",
                                "WEIGHT_CURVE",
                                "FALLOFF_WEIGHT_CURVE",
                                "DYNAMIC_MIRRORED",
                                ]

}