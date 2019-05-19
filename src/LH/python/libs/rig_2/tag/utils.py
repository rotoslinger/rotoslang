from rig.utils import misc
from maya import cmds

def get_tag_dict(tag_filter=["NO_EXPORT"]):
    tag_dict = {}
    for tag in tag_filter:
        for node in get_all_with_tag(tag):
            # Instantiate empty list if the key does not yet exist
            if node not in tag_dict.keys():
                tag_dict[node] = []
            tag_dict[node].append(tag)
    return tag_dict

# Temp, for testing, REMOVE ME
TAG_DICT = {u'C_upperLipPrimaryGimbal_CTL': ['NO_EXPORT'], u'C_upperLipPrimary01_BUF': ['NO_EXPORT'], u'C_upperLipPrimary_CTL': ['NO_EXPORT'], u'C_upperLipPrimary_GUIDE': ['NO_EXPORT']}

def set_tags_from_dict(tag_dict = TAG_DICT):
    for node in tag_dict.keys():
        for tag in tag_dict[node]:
            create_tag(node, tag)

def create_tag(node_to_tag, tag_name="TAG", warn=True):
    if cmds.objExists(node_to_tag + "." + tag_name):
        if warn:
            cmds.warning( "The node {0} already has the tag {1}, not adding tag.".format(node_to_tag, tag_name) )
        return
    if not cmds.objExists(node_to_tag):
        if warn:
            cmds.warning( "The node {0} does not exist, not adding tag {1}.".format(node_to_tag, tag_name) )
        return
    cmds.addAttr(node_to_tag, ln = tag_name,
                    at = "bool",)
    cmds.setAttr(node_to_tag +"." + tag_name,
                    l = True,
                    k=False)

def remove_tag(tagged_node, tag_name="TAG"):
    attr_full_name = tagged_node + "." + tag_name
    if not cmds.objExists(attr_full_name):
        return
    cmds.setAttr(tagged_node + "." + tag_name,
                l = False)
    cmds.deleteAttr(attr_full_name)


def tag_no_export(node_to_tag):
    if not node_to_tag:
        return
    if type(node_to_tag) != list:
        node_to_tag = [node_to_tag]
    for node in node_to_tag:
        create_tag(node, "NO_EXPORT")


def remove_tag_no_export(tagged_node):
    if not tagged_node:
        return
    if type(tagged_node) != list:
        tagged_node = [tagged_node]
    for node in tagged_node:
        remove_tag(node, "NO_EXPORT")


def tag_gimbal(node_to_tag):
    create_tag(node_to_tag, "GIMBAL")


def tag_control(node_to_tag):
    create_tag(node_to_tag, "CONTROL")


def tag_guide(node_to_tag):
    create_tag(node_to_tag, "GUIDE")

def tag_guide_shape(node_to_tag):
    create_tag(node_to_tag, "GUIDE_SHAPE")


def tag_bind_joint(node_to_tag):
    create_tag(node_to_tag, "BIND")


def tag_weight_curve(node_to_tag):
    create_tag(node_to_tag, "WEIGHT_CURVE")


def get_all_with_tag(tag):
    return [x for x in cmds.ls() if cmds.objExists(x + "." + tag)]


def get_all_shape_with_tag(tag):
    return [x for x in cmds.ls(shapes=True) if cmds.objExists(x + "." + tag)]


def vis_all_with_tag(tag, vis=True):
    nodes = get_all_with_tag(tag)
    for node in nodes:
        cmds.setAttr(node + ".v", vis)


def vis_all_shape_with_tag(tag, vis=True):
    nodes = get_all_shape_with_tag(tag)
    for node in nodes:
        cmds.setAttr(node + ".v", vis)


def get_all_gimbals():
    return get_all_with_tag("GIMBAL")


def get_all_guides():
    return get_all_with_tag("GUIDE")


def get_all_controls():
    return get_all_with_tag("CONTROL")


def select_all_with_tag(tag):
    cmds.select(get_all_with_tag(tag))


def get_transform_all_with_tag(tag):
    ret_transforms = []
    nodes = get_all_with_tag(tag)
    for node in nodes:
        # if the object's world location, rotation, scale can be queried, add it to the transforms
        if cmds.objectType(node) == "transform" or cmds.objectType(node) == "joint":
            ret_transforms.append(node)
            continue
        # If not it probably is a shape, so find the parent and add that
        ret_transforms.append(misc.getParent(node))
    return ret_transforms

def select_all_guides():
    select_all_with_tag("GUIDE")


def vis_all_guides():
    vis_all_shape_with_tag("GUIDE", True)
    vis_all_shape_with_tag("GUIDE_SHAPE", True)


def hide_all_guides():
    vis_all_shape_with_tag("GUIDE", False)
    vis_all_shape_with_tag("GUIDE_SHAPE", False)


def select_guide_from_selected():
    guides = []
    for sel in cmds.ls(sl=True):
        if not cmds.objExists(sel + ".guide"):
            continue
        guides.append(cmds.listConnections(sel + ".guide")[0])
    cmds.select(guides)